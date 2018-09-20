# DeepHLApan

   DeepHLApan is a deep learning approach used for predicting binding affinity and level between peptides and HLA alleles. Based on the predcited results,researchers could identify potential neoantigens for tumor immunotherapy.


## Download

Download the latest version of DeepHLApan from https://github.com/jiujiezz/deephlapan
    
    git clone https://github.com/jiujiezz/deephlapan.git

## Installation

Unzip the source code and go into the directory by using the following command:

    tar xvzf deephlapan-*.tar.gz

    cd deephlapan

Invoke the setup script:

    sudo python setup.py install


## General usage

Single peptide and HLA:

    deephlapan -P LNIMNKLNI -H HLA-A02:01 

List of peptides and HLA alleles in a file:

    deephlapan -F [file] -O [output directory]  

## Input files

DeepHLApan takes csv files as input with head of "Annotation,HLA,peptide" (requisite).

For example (demo/1.csv):
    
    Annotation,HLA,peptide
    1,HLA-B15:02,FPYGTTVTY
    2,HLA-B15:02,APPPPPPGH
    3,HLA-B15:02,APPPPPPPP
    4,HLA-B15:02,SQFGGGSQY
    5,HLA-B15:02,YLYGQTTTY
    6,HLA-B15:02,EQYEQILAF
    7,HLA-B15:02,SLFVSNHAY
    8,HLA-B15:02,NVIRDAVTY
    9,HLA-B15:02,FVPPPPPPP
    10,HLA-B15:02,FLFDGSPTY
    11,HLA-B15:02,ELWKNPTAF
    12,HLA-B15:02,TILDSSSSF
    13,HLA-B15:02,QLGPVGGVF
    14,HLA-B15:02,SVKPASSSF
 
 The content in Annotation can be defined as users.
 
