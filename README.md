# DeepHLApan

   DeepHLApan is a deep learning approach used for predicting high-confidence neoantigens by considering both the presentation possibilities of mutant peptides and the potential immunogenicity of pMHC.
   
   Contact: zhanzhou@zju.edu.cn

# Download and installation

There are two ways to install the DeepHLApan.

## 1.Docker (Recommend)

The Installation of Docker (v18.09) can be seen in https://docs.docker.com/

Pull the image of deephlapan from dockerhub:

      sudo docker pull biopharm/deephlapan:v1.1  

run the image in bash mode:

      sudo docker run -it --rm biopharm/deephlapan:v1.1 bash

## 2.Git (All the dependencies should be properly installed)

### System
Linux

### Dependencies
perl    
python    
[cuda 9](https://developer.nvidia.com/cuda-90-download-archive)  
[cudnn 7](https://developer.nvidia.com/rdp/cudnn-archive)

### Steps

Download the latest version of DeepHLApan from https://github.com/jiujiezz/deephlapan
    
    git clone https://github.com/jiujiezz/deephlapan.git
    
Unzip the source code and go into the directory by using the following command:

    tar xvzf deephlapan-*.tar.gz

    cd deephlapan

Invoke the setup script:

    sudo python setup.py install


# General usage

Single peptide and HLA:

    deephlapan -P LNIMNKLNI -H HLA-A02:01 

List of peptides and HLA alleles in a file:

    deephlapan -F [file] -O [output directory]  

# Input files

DeepHLApan takes **csv** files as input with head of **"Annotation,HLA,peptide"** (requisite).    
It supports to rank the HLA-peptide pairs if all the mutant peptides belong to one sample. 

For example (demo/1.csv):
    
      Annotation,HLA,peptide
      NCI-3784,HLA-A01:01,MKRFVQWL
      NCI-3784,HLA-A03:01,MKRFVQWL
      NCI-3784,HLA-B07:02,MKRFVQWL
      NCI-3784,HLA-B07:02,MKRFVQWL
      NCI-3784,HLA-C07:02,MKRFVQWL
      NCI-3784,HLA-C07:02,MKRFVQWL
      NCI-3784,HLA-A01:01,KRFVQWLK
      NCI-3784,HLA-A03:01,KRFVQWLK
      NCI-3784,HLA-B07:02,KRFVQWLK
      NCI-3784,HLA-B07:02,KRFVQWLK
      NCI-3784,HLA-C07:02,KRFVQWLK
      NCI-3784,HLA-C07:02,KRFVQWLK
 
 The content in Annotation can be changed as users wanted.
 
 
 # Update log
 ## 2019.12
 V1.1.1    
 Improve the prediction speed
 ## 2019.03
 V1.1    
 Add the function of immunogeneicity prediction
 
 ## 2018.07
 V1.0    
 Test the suitabilty of different RNN variants (GRU,LSTM,BGRU,BLSTM,att-BGRU and att-BLSTM) on the binding prediction and select the best (att-BGRU) one for model construction.
 
