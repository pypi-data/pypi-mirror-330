<!--
 * @Author: LiuFeng(USTC) : 
   * liufeng2317@mail.ustc.edu.cn
   * liufeng1@pjlab.org.cn
 * @Date: 2023-07-03 11:16:43
 * @LastEditors: LiuFeng
 * @LastEditTime: 2024-01-02 13:16:52
 * @FilePath: /ADFWI/README.md
 * @Description: 
 * Copyright (c) 2024 by liufeng2317 email: liufeng1@pjlab.org.cn, All Rights Reserved.
-->

# Automatic Differentiation-Based Full Waveform Inversion

---

## 👩‍💻 Introduction
**ADFWI** is an open-source framework for high-resolution subsurface parameter estimation by minimizing discrepancies between observed and simulated seismic data. Utilizing automatic differentiation (AD), ADFWI **simplifies the derivation and implementation of Full Waveform Inversion (FWI)**, enhancing the design and evaluation of methodologies. It supports wave propagation in various media, including isotropic acoustic, isotropic elastic, and both vertical transverse isotropy (VTI) and tilted transverse isotropy (TTI) models.

In addition, **ADFWI** provides a comprehensive collection of Objective functions, regularization techniques, optimization algorithms, and deep neural networks. This rich set of tools facilitates researchers in conducting experiments and comparisons, enabling them to explore innovative approaches and refine their methodologies effectively.


---

## ⚡️ Installation

To install the Automatic Differentiation-Based Full Waveform Inversion (ADFWI) framework, please follow these steps:

1. **Ensure Prerequisites**  
   Before you begin, make sure you have the following software installed on your system:  
   - **Python 3.8 or higher**: Download Python from the official website: [Python Downloads](https://www.python.org/downloads/).
   - **pip** (Python package installer).

2. **Create a Virtual Environment (Optional but Recommended)**
   It is recommended to create a virtual environment to manage your project dependencies. You can use either `venv` or `conda`. 
   For example, using `conda`:
   ```bash
   conda create --name adfwi-env python=3.8
   conda activate adfwi-env
   ```

3. **Install Required Packages**
- Method 1: **Clone the github Repository**
  This method provides the latest version, which may be more suitable for your research:
    ```bash
    git clone https://github.com/liufeng2317/ADFWI.git
    cd ADFWI
    ```
    Then, install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```
- Method 2: Install via pip
  Alternatively, you can directly install ADFWI from PyPI:
  ```bash
    pip install ADFWI-Torch
  ```

4. **Verify the Installation**
  To ensure that ADFWI is installed correctly, run any examples located in the examples folder.

5. **Troubleshooting**
   If you encounter any issues during installation, please check the Issues section of the GitHub repository for potential solutions or to report a new issue.

---

## 👾 Examples

For examples and usage instructions, please check the GitHub repository: [ADFWI GitHub Repository](https://github.com/liufeng2317/ADFWI). There, you will find various examples that demonstrate how to utilize the ADFWI framework effectively.

---

## 📝 Features
- **Multi-Wave Equation**:
  - Iso-Acoustic
  - Iso-Elastic
  - VTI-Elastic
  - TTI-Elastic
- **Various Objective Functions**
  - L1-norm
  - L2-norm
  - Smooth-L1 norm
  - Envelope
  - Global Correlation
  - T-Distribution (StudentT)
  - Soft Dynamic Time Wrapping (SoftDTW)
  - Wasserstein Distance-based with Sinkhorn (Wassrestein)
- **Various Optimization Methods**
  - SGD
  - ASGD
  - RMSProp
  - Adagrad
  - Adam
  - AdamW
  - NAdam
  - RAdam
- **Deep Neural Network Integration**
  - DNNs reparameterize the Earth Model for learnable regularization
  - Droupout for access the inversion uncertainty
- **Resource Management**
  - Mini-batch
  - Checkpointing
- **Robustness and Portability**
  - Each of the method has proposed a code for testing.

---

## ⚖️ LICENSE

The **Automatic Differentiation-Based Full Waveform Inversion (ADFWI)** framework is licensed under the [MIT License](https://opensource.org/licenses/MIT). This license allows you to:

- **Use**: You can use the software for personal, academic, or commercial purposes.
- **Modify**: You can modify the software to suit your needs.
- **Distribute**: You can distribute the original or modified software to others.
- **Private Use**: You can use the software privately without any restrictions.

---
## 🔰 Contact

**Liu Feng**  
Shanghai Artificial Intelligence Laboratory & Shanghai Jiao Tong University  
Email: liufeng2317@mail.sjtu.edu.cn or liufeng1@pjlab.org.cn  

```bibtex
@software{LiuFeng2317,
  author       = {Feng Liu, GuangYuan Zou, \& Haipeng Li},
  title        = {ADFWI},
  month        = July,
  year         = 2024,
  version      = {v1.1},
}
```