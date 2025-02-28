from setuptools import setup, find_packages

setup(
    name='ADFWI-Torch',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.0',
        'scipy>=1.10.0',
        'matplotlib>=3.7.0',
        'torch>=2.0.0',
        'disba>=0.6.0',
        'torchinfo',
        'segyio',
        'ncg_optimizer',
        'pysdtw',
        'geomloss',
        'h5py',
        'obspy',
        'tqdm'
    ],
    author='Feng Liu',
    author_email='liufeng2317@sjtu.edu.cn',
    description='ADFWI: A framework for high-resolution subsurface parameter estimation using Full Waveform Inversion',
    long_description=open('README_PIP.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/liufeng2317/ADFWI',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
