from optparse import OptionParser

def CommandLineParser():
    
    parser=OptionParser()

    print '''
        =====================================================================
        DeepHLApan is a deep learning approach used for predicting binding 
        affinity and level between peptides and HLA alleles. Based on the 
        predcited results,researchers could identify potential neoantigens 
        for tumor immunotherapy.

        Usage:

        Single peptide and HLA:

            deephlapan -P LNIMNKLNI -H HLA-A02:01 

        List of peptides and HLA alleles in a file:

            deephlapan -F [file] -O [output directory]  

            (see 1.csv in demo/ for the detailed format of input file)
        =====================================================================
        '''

    parser.add_option("-P","--peptide",dest="sequence",help="single peptide for prediction",default="")
    parser.add_option("-H","--HLA allele",dest="hla",help="single hla for prediction, used with -P",default="")
    parser.add_option("-F","--file",dest="file",help="Input file with peptides and HLA alleles : if given, overwrite -P, -H option",default="")
    parser.add_option('-O','--OutputDirectory',dest="WD",default="",help="Directory to store predicted results. User must have write privilege. If omitted, the current directory will be applied.")
    parser.add_option("--Ms","--Model selection",dest="model_select",help="model selection for binding affinity or level prediction, a indicates att_BGRU, g indicates GRU",default="g")
    parser.add_option("--Mt","--Model type selection",dest="model_type",help="r indicates regression (provide both binding affinity and level),  c indicates classification (provide possibility of bind and binding level),",default="r")
    parser.add_option("--Mc","--select the best model in five-fold corss-validation or whole models",dest="model_complete",help="w indicates whole models, b indicates best model",default="b")
    return parser.parse_args()
