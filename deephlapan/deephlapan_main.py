import numpy as np
import pandas as pd
import sys, time, os, io, csv, math, datetime, csv, re

from sklearn.utils import shuffle
from sklearn.metrics import roc_auc_score, roc_curve, auc
from scipy import stats

from keras import initializers
from keras.models import load_model
from keras.utils.generic_utils import CustomObjectScope
from attention import Attention

curDir=os.path.dirname(os.path.realpath(__file__))+'/'
HLA_seq=pd.read_csv(curDir+ 'model/MHC_pseudo.dat',sep = '\t')
seqs={}
seq={}
for i in range(len(HLA_seq)):
	seqs[HLA_seq.HLA[i]]=HLA_seq.sequence[i]

aa_idx = {'A':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14, 'R':15, 'S':16, 'T':17, 'V':18, 'W':19, 'Y':20, 'X':21}

def read_and_prepare(file):
	data=pd.read_csv(file)
	complex=np.full((len(data), 49),21, int)
	for j in range(len(data)):
		combined=seqs[data.HLA[j]] + data.peptide[j]
		seq=[aa_idx[x] for x in combined]
		for i in range(len(seq)):
			complex[j,i]=seq[i]
	return complex
	
def read_and_prepare_single(peptide,hla):
	complex=np.full((1, 49),21, int)
	seq=[aa_idx[x] for x in list(seqs[hla] + peptide)]
	for i in range(len(seq)):
		complex[0,i]=seq[i]
	return complex

def deephlapan_main(opt):
	i = datetime.datetime.now()
	print (str(i) + ' Prediction starting.....\n')
	peptide=opt.sequence
	hla=opt.hla
	WD=opt.WD
	if len(WD)==0:
		WD='.'
	
	fname=peptide+'_'+hla
	if (opt.file):
		fname=opt.file.split('/')[-1]
		fname=fname.split('.')[0]
		df=pd.read_csv(opt.file)
		X_test = read_and_prepare(opt.file)
	else:
		X_test = read_and_prepare_single(peptide,hla)
	
	predScores1 = np.zeros((5, len(X_test)))
	predScores = np.zeros((5, len(X_test)))
	for i in range(5):
		with CustomObjectScope({'Attention': Attention}):
			model=load_model(curDir+ 'model/binding_model' + str(i+1)+ '.hdf5')
			model1=load_model(curDir+ 'model/immunogenicity_model' + str(i+1)+ '.hdf5')
			predScores[i,:] =np.squeeze(model.predict_proba(X_test))
			predScores1[i,:] =np.squeeze(model1.predict_proba(X_test))
	result = np.average(predScores, axis=0)
	result1 = np.average(predScores1, axis=0)
				
	with open(WD + '/' + fname + '_predicted_result.csv','w') as f:
		f.write('Annotation,HLA,Peptide,binding score,immunogenic score\n')
		if (opt.file):
			for i in range(len(result)):
				f.write(str(df.Annotation[i]) + ',' + str(df.HLA[i]) + ',' + str(df.peptide[i]) + ',' + str(result[i]) + ',' + str(result1[i]) + '\n')
		else:
			f.write('single peptide,' + str(hla) + ',' + str(peptide) + ',' + str(result[0]) + ',' + str(result1[0]) + '\n')
	f.close()
	if (opt.file):
		command = 'perl ' + curDir + '/model/rank.pl ' + WD + '/' + fname + '_predicted_result.csv'
		os.system(command)
	j = datetime.datetime.now()
	print (str(j) + ' Prediction end\n')

