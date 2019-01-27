from optparse import OptionParser

def CommandLineParser():
    
    parser=OptionParser()

    print '''
        =====================================================================
        DeepHLApan is a deep learning approach used for predicting high-confidence 
        neoantigens by considering both the presentation possibilities of 
        mutant peptides and the potential immunogenicity of pMHC.

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
    return parser.parse_args()
