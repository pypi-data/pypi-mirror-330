'''
* Author: LiuFeng(SJTU) : liufeng2317@sjtu.edu.cn
* Date: 2024-04-26 19:42:24
* LastEditors: LiuFeng
* LastEditTime: 2024-05-13 23:16:49
* Description: 
* Copyright (c) 2024 by liufeng, Email: liufeng2317@sjtu.edu.cn, All Rights Reserved.
'''
from typing import Optional,Union,List
import os
import math
import torch
import numpy as np
from tqdm import tqdm
from ADFWI.model       import AbstractModel
from ADFWI.dip.dip_vti_model import DIP_VTIModel
from ADFWI.dip.dip_vti_model_o4a import DIP_VTIModel_o4a
from ADFWI.propagator  import ElasticPropagator,GradProcessor
from ADFWI.survey      import SeismicData
from ADFWI.fwi.misfit  import Misfit,Misfit_NIM
from ADFWI.fwi.regularization import Regularization
from ADFWI.utils       import numpy2tensor
from ADFWI.view        import plot_vp_vs_rho,plot_model,plot_eps_delta_gamma
from ADFWI.fwi.multiScaleProcessing import lpass

class DIP_ElasticFWI(torch.nn.Module):
    """Elastic Full waveform inversion class
    """
    def __init__(self,propagator:ElasticPropagator,model:AbstractModel,
                 loss_fn:Union[Misfit,torch.autograd.Function],
                 obs_data:SeismicData,
                 optimizer:Union[torch.optim.Optimizer,List[torch.optim.Optimizer]]      = None,
                 scheduler:torch.optim.lr_scheduler                                      = None,
                 gradient_processor: Union[GradProcessor,List[GradProcessor]]            = None,
                 regularization_fn:Optional[Regularization]                              = None,
                 regularization_weights_x:Optional[List[Union[float]]]                   = [0,0,0,0,0,0],       # vp/vs/rho epsilon/delta/gamma
                 regularization_weights_z:Optional[List[Union[float]]]                   = [0,0,0,0,0,0],       # vp/vs/rho epsilon/delta/gamma
                 waveform_normalize:Optional[bool]                                       = True,
                 cache_result:Optional[bool]                                             = True,
                 save_fig_epoch:Optional[int]                                            = -1,
                 save_fig_path:Optional[str]                                             = "",
                 inversion_component:Optional[np.array]                                   = ["pressure"],
                ):
        """
        Parameters:
        --------------
        propagator (ElasticPropagator)                                          : The propagator used for simulating elastic wave propagation.
        model (AbstractModel)                                                   : The model class representing the velocity structure.
        loss_fn (Union[Misfit, torch.autograd.Function])                        : The loss function used to compute the misfit between observed and predicted data.
        obs_data (SeismicData)                                                  : The observed seismic data.
        optimizer (Union[torch.optim.Optimizer, List[torch.optim.Optimizer]])   : The optimizer or list of optimizers for model parameters. Default is None.
        scheduler (Optional[torch.optim.lr_scheduler])                          : The learning rate scheduler for optimizing the model parameters. Default is None.
        gradient_processor (Union[GradProcessor, List[GradProcessor]])          : Processor(s) for handling gradients (e.g., vp/vs/rho, epsilon/delta/gamma). Default is None.
        regularization_fn (Optional[Regularization])                            : Regularization function(s) applied to parameters like vp/vs/rho/epsilon/delta/gamma. Default is None.
        regularization_weights_x (Optional[List[Union[float]]])                 : Regularization weights for the x-axis. Default is [0, 0, 0, 0, 0, 0].
        regularization_weights_z (Optional[List[Union[float]]])                 : Regularization weights for the z-axis. Default is [0, 0, 0, 0, 0, 0].
        waveform_normalize (Optional[bool])                                     : Whether to normalize the waveforms during inversion. Default is True.
        cache_result (Optional[bool])                                           : Whether to save intermediate results during the inversion. Default is True.
        cache_gradient (Optional[bool])                                         : Whether to save model variations (not gradients) during inversion. Default is False.
        save_fig_epoch (Optional[int])                                          : The interval (in epochs) at which to save the inversion result figure. Default is -1 (no figure saved).
        save_fig_path (Optional[str])                                           : The path where to save the inversion result figure. Default is an empty string (no save path).
        inversion_component (Optional[np.array])                                : The components of the inversion (e.g., ["pressure"]). Default is ["pressure"].
        """
        super().__init__()
        self.propagator                 = propagator
        self.model                      = model
        self.optimizer                  = optimizer
        self.scheduler                  = scheduler
        self.loss_fn                    = loss_fn
        self.regularization_fn          = regularization_fn
        self.regularization_weights_x   = regularization_weights_x
        self.regularization_weights_z   = regularization_weights_z
        self.obs_data                   = obs_data
        self.gradient_processor         = gradient_processor
        self.device                     = self.propagator.device
        self.dtype                      = self.propagator.dtype 
        
        # receiver masks
        receiver_masks = self.propagator.receiver_masks
        if receiver_masks is None:
            receiver_masks = np.ones((self.propagator.src_n,self.propagator.rcv_n))
        receiver_masks = numpy2tensor(receiver_masks).to(self.device)
        self.receiver_masks = receiver_masks.unsqueeze(1).expand(-1, self.propagator.nt, -1)  # [shot, time, rcv]

        # observed data
        self.waveform_normalize = waveform_normalize
        obs_p   = -(self.obs_data.data["txx"]+self.obs_data.data["tzz"])
        obs_p   = (numpy2tensor(obs_p,self.dtype).to(self.device))*self.receiver_masks
        obs_vx  = (numpy2tensor(self.obs_data.data["vx"],self.dtype).to(self.device))*self.receiver_masks
        obs_vz  = (numpy2tensor(self.obs_data.data["vz"],self.dtype).to(self.device))*self.receiver_masks
        if self.waveform_normalize:
            obs_p  = self._normalize(obs_p)
            obs_vx = self._normalize(obs_vx)
            obs_vz = self._normalize(obs_vz)
        self.obs_p = obs_p
        self.obs_vx = obs_vx
        self.obs_vz = obs_vz
        
        # save result
        self.cache_result   = cache_result
        self.iter_vp,self.iter_vs,self.iter_rho = [],[],[]       
        self.iter_eps,self.iter_delta,self.iter_gamma = [],[],[]
        self.iter_loss      = []
        
        # optimizer
        if not isinstance(self.optimizer, list):
            self.optimizer = [self.optimizer]
        
        if not isinstance(self.scheduler, list):
            self.scheduler = [self.scheduler]
            
        
        # save figure
        self.save_fig_epoch = save_fig_epoch
        self.save_fig_path  = save_fig_path
        
        # inversion component
        self.inversion_component = inversion_component

    def _normalize(self,data):
        mask    = torch.sum(torch.abs(data),axis=1,keepdim=True) == 0
        max_val = torch.max(torch.abs(data),axis=1,keepdim=True).values
        max_val = max_val.masked_fill(mask, 1)
        data = data/max_val
        return data
    
    # misfits calculation
    def calculate_loss(self, synthetic_waveform, observed_waveform, normalization, loss_fn, cutoff_freq=None, propagator_dt=None):
        """
        Generalized function to calculate misfit loss for a given component.
        """
        if normalization:
            synthetic_waveform = synthetic_waveform / (torch.max(torch.abs(synthetic_waveform), axis=1, keepdim=True).values)
        # Apply low-pass filter if cutoff frequency is provided
        if cutoff_freq is not None:
            synthetic_waveform, observed_waveform = lpass(synthetic_waveform, observed_waveform, cutoff_freq, int(1 / propagator_dt))
        if isinstance(loss_fn, Misfit):
            return loss_fn.forward(synthetic_waveform, observed_waveform)
        else:
            return loss_fn.apply(synthetic_waveform, observed_waveform)
    
    # regularization calculation
    def calculate_regularization_loss(self, model_param, weight_x, weight_z, regularization_fn):
        """
        Generalized function to calculate regularization loss for a given parameter.
        """
        regularization_loss = torch.tensor(0.0, device=model_param.device)
        # Check if the parameter requires gradient
        if model_param.requires_grad:
            # Set the regularization weights for x and z directions
            regularization_fn.alphax = weight_x
            regularization_fn.alphaz = weight_z
            # Calculate regularization loss if any weight is greater than zero
            if regularization_fn.alphax > 0 or regularization_fn.alphaz > 0:
                regularization_loss = regularization_fn.forward(model_param)
        return regularization_loss
    
        # gradient precondition
    def process_gradient(self, parameter,forw,idx=None):
        with torch.no_grad():
            grads = parameter.grad.cpu().detach().numpy()
            vmax = np.max(parameter.cpu().detach().numpy())
            # Apply gradient processor
            if isinstance(self.gradient_processor, GradProcessor):
                grads = self.gradient_processor.forward(nz=self.model.nz, nx=self.model.nx, vmax=vmax, grad=grads, forw=forw)
            else:
                grads = self.gradient_processor[idx].forward(nz=self.model.nz, nx=self.model.nx, vmax=vmax, grad=grads, forw=forw)
            # Convert grads back to tensor and assign
            grads_tensor = numpy2tensor(grads, dtype=self.propagator.dtype).to(self.propagator.device)
            parameter.grad = grads_tensor
    
    def save_vp_vs_rho_fig(self,epoch_id,vp,vs,rho):
        vp_bound    =  self.model.get_bound("vp")
        vs_bound    =  self.model.get_bound("vs")
        rho_bound   =  self.model.get_bound("rho")
        if vp_bound[0] is None and vp_bound[1] is None:
            self.vp_min = self.model.get_model("vp").min() - 500
            self.vp_max = self.model.get_model("vp").max() + 500
        else: 
            self.vp_min = vp_bound[0]
            self.vp_max = vp_bound[1]
            if self.model.water_layer_mask is not None:
                self.vp_min = 1500
        if vs_bound[0] is None and vs_bound[1] is None:
            self.vs_min = self.model.get_model("vs").min() - 500
            self.vs_max = self.model.get_model("vs").max() + 500
        else: 
            self.vs_min = vs_bound[0]
            self.vs_max = vs_bound[1]
            if self.model.water_layer_mask is not None:
                self.vs_min = 0        
        if rho_bound[0] is None and rho_bound[1] is None:
            self.rho_min = self.model.get_model("rho").min() - 200
            self.rho_max = self.model.get_model("rho").max() + 200
        else: 
            self.rho_min = rho_bound[0]
            self.rho_max = rho_bound[1]
            if self.model.water_layer_mask is not None:
                self.rho_min = 1000
        
        if self.save_fig_epoch == -1:
            pass
        elif epoch_id%self.save_fig_epoch == 0:
            if os.path.exists(self.save_fig_path):
                plot_vp_vs_rho(
                    vp=vp,vs=vs,rho=rho,
                    # title=f"Iteration {i}",
                    figsize=(12,5),wspace=0.2,cbar_pad_fraction=0.18,cbar_height=0.04,
                    dx=self.model.dx,dz=self.model.dz,
                    vp_min=self.vp_min,vp_max=self.vp_max,
                    vs_min=self.vs_min,vs_max=self.vs_max,
                    rho_min=self.rho_min,rho_max=self.rho_max,
                    save_path=os.path.join(self.save_fig_path,f"model_{epoch_id}.png"),
                    show=False
                    )
        return

    def save_eps_delta_gamma_fig(self,epoch_id,eps,delta,gamma):
            eps_bound    =  self.model.get_bound("eps")
            delta_bound    =  self.model.get_bound("delta")
            gamma_bound   =  self.model.get_bound("gamma")
            if eps_bound[0] is None and eps_bound[1] is None:
                self.vp_min = self.model.get_model("eps").min() - 0.01
                self.vp_max = self.model.get_model("eps").max() + 0.01
            else: 
                self.vp_min = eps_bound[0]
                self.vp_max = eps_bound[1]
            
            if delta_bound[0] is None and delta_bound[1] is None:
                self.delta_min = self.model.get_model("delta").min() - 0.01
                self.delta_max = self.model.get_model("delta").max() + 0.01
            else: 
                self.vs_min = delta_bound[0]
                self.vs_max = delta_bound[1]
            
            if gamma_bound[0] is None and gamma_bound[1] is None:
                self.gamma_min = self.model.get_model("gamma").min() - 0.01
                self.gamma_max = self.model.get_model("gamma").max() + 0.01
            else: 
                self.rho_min = gamma_bound[0]
                self.rho_max = gamma_bound[1]
        
            if self.save_fig_epoch == -1:
                pass
            elif epoch_id%self.save_fig_epoch == 0:
                if os.path.exists(self.save_fig_path):
                    plot_eps_delta_gamma(
                        eps=eps,delta=delta,gamma=gamma,
                        # title=f"Iteration {i}",
                        figsize=(12,5),wspace=0.3,cbar_pad_fraction=0.01,cbar_height=0.04,
                        dx=self.model.dx,dz=self.model.dz,
                        save_path=os.path.join(self.save_fig_path,f"anisotropic_model_{epoch_id}.png"),
                        show=False
                        )
            return
    
    def save_model(self,epoch_id,loss_epoch):
        """
            Save model parameters and gradients if caching is enabled.
        """
        # Save the loss
        self.iter_loss.append(loss_epoch)

        # Save the model parameters
        param_names = ["vp", "vs", "rho"]
        anisotropic_params = ["eps", "delta", "gamma"] if isinstance(self.model, (DIP_VTIModel,DIP_VTIModel_o4a)) else []
        for name in param_names + anisotropic_params:
            param = getattr(self.model, name, None)
            if param is not None:
                temp_param = param.cpu().detach().numpy()
                getattr(self, f"iter_{name}").append(temp_param)
        
        # save the figure
        self.save_vp_vs_rho_fig(epoch_id,self.model.vp.cpu().detach().numpy(),
                                         self.model.vs.cpu().detach().numpy(),
                                         self.model.rho.cpu().detach().numpy())
        if isinstance(self.model,(DIP_VTIModel,DIP_VTIModel_o4a)):
            self.save_eps_delta_gamma_fig(epoch_id,
                                          self.model.eps.cpu().detach().numpy(),
                                          self.model.delta.cpu().detach().numpy(),
                                          self.model.gamma.cpu().detach().numpy())
        return

    def forward(self,
                iteration:int,
                fd_order:int                        = 4,
                batch_size:Optional[int]            = None,
                checkpoint_segments:Optional[int]   = 1 ,
                start_iter                          = 0,
                cutoff_freq                         = None,
                ):
        """
        Parameters:
        ------------
        iteration (int)                     : The maximum iteration number in the inversion process.
        fd_order (int)                      : The order of the finite difference scheme for wave propagation. Default is 4.
        batch_size (Optional[int])          : The number of shots (data samples) in each batch. Default is None, meaning use all available shots.
        checkpoint_segments (Optional[int]) : The number of segments into which the time series should be divided for memory efficiency. Default is 1, which means no segmentation.
        start_iter (int)                    : The starting iteration for the optimization process (e.g., for optimizers like Adam/AdamW, and learning rate schedulers like step_lr). Default is 0.
        cutoff_freq (Optional[float])       : The cutoff frequency for low-pass filtering, if specified. Default is None (no filtering applied).
        """
        n_shots = self.propagator.src_n
        if batch_size is None or batch_size > n_shots:
            batch_size = n_shots
        
        # epoch
        pbar_epoch = tqdm(range(start_iter,start_iter+iteration),position=0,leave=False,colour='green',ncols=80)
        for i in pbar_epoch:
            # batch
            for opt in self.optimizer:
                opt.zero_grad()
            loss_epoch = 0
            pbar_batch = tqdm(range(math.ceil(n_shots/batch_size)),position=1,leave=False,colour='red',ncols=80)
            for batch in pbar_batch:
                # forward simulation
                begin_index = 0  if batch==0 else batch*batch_size
                end_index   = n_shots if batch==math.ceil(n_shots/batch_size)-1 else (batch+1)*batch_size
                shot_index  = np.arange(begin_index,end_index)
                record_waveform = self.propagator.forward(fd_order=fd_order,shot_index=shot_index,checkpoint_segments=checkpoint_segments)
                rcv_txx,rcv_tzz,rcv_txz,rcv_vx,rcv_vz = record_waveform["txx"],record_waveform["tzz"],record_waveform["txz"],record_waveform["vx"],record_waveform["vz"]
                forward_wavefield_txx,forward_wavefield_tzz,forward_wavefield_txz,forward_wavefield_vx,forward_wavefield_vz = record_waveform["forward_wavefield_txx"],record_waveform["forward_wavefield_tzz"],record_waveform["forward_wavefield_txz"],record_waveform["forward_wavefield_vx"],record_waveform["forward_wavefield_vz"]
                
                # misfits
                loss_pressure, loss_vx, loss_vz = 0, 0, 0
                receiver_mask = self.receiver_masks[shot_index]
                if "pressure" in self.inversion_component:
                    if batch == 0:
                        forw  = -(forward_wavefield_txx + forward_wavefield_tzz).cpu().detach().numpy()
                    else:
                        forw += -(forward_wavefield_txx + forward_wavefield_tzz).cpu().detach().numpy()
                    syn_p = -(rcv_txx + rcv_tzz)
                    syn_p = syn_p*receiver_mask
                    loss_pressure = self.calculate_loss(syn_p, self.obs_p[shot_index], self.waveform_normalize, self.loss_fn, cutoff_freq, self.propagator.dt)
                if "vx" in self.inversion_component:
                    forw = forward_wavefield_vx.cpu().detach().numpy()
                    rcv_vx = rcv_vx*receiver_mask
                    loss_vx = self.calculate_loss(rcv_vx, self.obs_vx[shot_index],self.waveform_normalize, self.loss_fn, cutoff_freq, self.propagator.dt)
                if "vz" in self.inversion_component:
                    rcv_vz = rcv_vz*receiver_mask
                    forw = forward_wavefield_vz.cpu().detach().numpy()
                    loss_vz = self.calculate_loss(rcv_vz, self.obs_vz[shot_index],self.waveform_normalize, self.loss_fn, cutoff_freq, self.propagator.dt)
                data_loss = loss_pressure + loss_vx + loss_vz
                
                # regularization
                if self.regularization_fn is not None:
                    # Initialize regularization losses
                    regularization_loss_vp  = self.calculate_regularization_loss(self.model.vp , self.regularization_weights_x[0], self.regularization_weights_z[0], self.regularization_fn)
                    regularization_loss_vs  = self.calculate_regularization_loss(self.model.vs , self.regularization_weights_x[1], self.regularization_weights_z[1], self.regularization_fn)
                    regularization_loss_rho = self.calculate_regularization_loss(self.model.rho, self.regularization_weights_x[2], self.regularization_weights_z[2], self.regularization_fn)
                    # For anisotropic model parameters
                    regularization_loss_eps = regularization_loss_delta = regularization_loss_gamma = torch.tensor(0.0, device=self.device)
                    if isinstance(self.model, (DIP_VTIModel,DIP_VTIModel_o4a)):
                        regularization_loss_eps   = self.calculate_regularization_loss(self.model.eps  , self.regularization_weights_x[3], self.regularization_weights_z[3], self.regularization_fn)
                        regularization_loss_delta = self.calculate_regularization_loss(self.model.delta, self.regularization_weights_x[4], self.regularization_weights_z[4], self.regularization_fn)
                        regularization_loss_gamma = self.calculate_regularization_loss(self.model.gamma, self.regularization_weights_x[5], self.regularization_weights_z[5], self.regularization_fn)
                    # Summing all regularization losses
                    regularization_loss = (regularization_loss_vp + regularization_loss_vs + regularization_loss_rho +
                                        regularization_loss_eps + regularization_loss_delta + regularization_loss_gamma)
                    # Adding regularization loss to total loss
                    loss_epoch += data_loss.item() + regularization_loss.item()
                    loss = data_loss + regularization_loss
                else:
                    loss_epoch += data_loss.item()
                    loss = data_loss
                loss.backward()
                if math.ceil(n_shots/batch_size) == 1:
                    pbar_batch.set_description(f"Shot:{begin_index} to {end_index}")
            
            # gradient postprocess
            def grad_post_process(grads, parameter, forw=None, idx=None):
                grads = grads.cpu().detach().numpy()
                with torch.no_grad():
                    param = getattr(self.model, parameter).cpu().detach().numpy()
                    vmax = np.max(param)
                    # Apply gradient processor
                    if isinstance(self.gradient_processor, GradProcessor):
                        grads = self.gradient_processor.forward(nz=self.propagator.model.nz, nx=self.propagator.model.nx, vmax=vmax, grad=grads, forw=forw)
                    else:
                        grads = self.gradient_processor[idx].forward(nz=self.propagator.model.nz, nx=self.propagator.model.nx, vmax=vmax, grad=grads, forw=forw)
                    grads = numpy2tensor(grads, dtype=self.propagator.dtype).to(self.propagator.device)
                return grads

            # Register hooks for each model parameter
            if self.propagator.model.get_requires_grad("vp"):
                self.propagator.model.vp.register_hook(lambda grad: grad_post_process(grad, "vp", forw=forw, idx=0))
            if self.propagator.model.get_requires_grad("vs"):
                self.propagator.model.vs.register_hook(lambda grad: grad_post_process(grad, "vs", forw=forw, idx=1))
            if self.propagator.model.get_requires_grad("rho"):
                self.propagator.model.rho.register_hook(lambda grad: grad_post_process(grad, "rho", forw=forw, idx=2))
            if isinstance(self.model, (DIP_VTIModel,DIP_VTIModel_o4a)):
                if self.propagator.model.get_requires_grad("eps"):
                    self.propagator.model.eps.register_hook(lambda grad: grad_post_process(grad, "eps", forw=forw, idx=3))
                if self.propagator.model.get_requires_grad("delta"):
                    self.propagator.model.delta.register_hook(lambda grad: grad_post_process(grad, "delta", forw=forw, idx=4))
                if self.propagator.model.get_requires_grad("gamma"):
                    self.propagator.model.gamma.register_hook(lambda grad: grad_post_process(grad, "gamma", forw=forw, idx=5))
            
            for opt in self.optimizer:
                opt.step()
            
            for schdul in self.scheduler:
                schdul.step()
            
            # constrain the model parameters
            with torch.no_grad():
                self.propagator.model.forward()
            
            # cache results
            if self.cache_result:
                self.save_model(epoch_id=i,loss_epoch=loss_epoch)   
                
            pbar_epoch.set_description("Iter:{},Loss:{:.4}".format(i+1,loss_epoch))