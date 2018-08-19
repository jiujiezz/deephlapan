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
            # if 'n' in (str(seqs[data.HLA[j]]) + str(data.peptide[j])):
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
	model_select=opt.model_select
	model_type=opt.model_type
	model_complete=opt.model_complete
	model_name='GRU'
	model_type_name='regression'
	model_complete_name='best_model'
	if model_select =='a':
		model_name='att_BGRU'
	if model_type=='c':
		model_type_name='classification'
	if model_complete=='w':
		model_complete_name='whole_model'
	if len(WD)==0:
		WD='.'
	
	fname=peptide+'_'+hla
	if (opt.file):
		fname=opt.file.split('/')[-1]
		df=pd.read_csv(opt.file)
		X_test = read_and_prepare(opt.file)
	else:
		X_test = read_and_prepare_single(peptide,hla)
	
	if model_type_name =='regression':
		if model_complete_name == 'whole_model':
			predScores1 = np.zeros((5, len(X_test)))
			predScores2 = np.zeros((5, len(X_test)))
			for i in range(5):
				with CustomObjectScope({'Attention': Attention}):
					model1=load_model(curDir+ 'model/classification_'+ str(model_name) + '_' + str(i)+ '.hdf5')
					model2=load_model(curDir+ 'model/regression_' + str(model_name) + '_'+ str(i)+ '.hdf5')
					predScores1[i,:] =np.squeeze(model1.predict_proba(X_test))
					predScores2[i,:] =np.squeeze(model2.predict_proba(X_test))
					model=load_model(curDir+ 'model/combine_model_'+ str(model_name) + '.hdf5')
			Y_pred1 = np.average(predScores1, axis=0)
			Y_pred2 = np.average(predScores2, axis=0)
			Y_pred=np.zeros((len(Y_pred1),2))
			for j in range(len(Y_pred1)):
				Y_pred[j,0]=Y_pred1[j]
				Y_pred[j,1]=Y_pred2[j]
			result=model.predict_proba(Y_pred)
			result=[math.exp((1-value)*math.log(50000))for value in result]
			predicted_labels = [1 if score <= 500 else 0 for score in result]
		elif model_complete_name == 'best_model':
			predScores1 = np.zeros((1, len(X_test)))
			predScores2 = np.zeros((1, len(X_test)))
			with CustomObjectScope({'Attention': Attention}):
				model1=load_model(curDir+ 'model/classification_'+ str(model_name) + '_2.hdf5')
				model2=load_model(curDir+ 'model/regression_' + str(model_name) + '_2.hdf5')
				predScores1[0,:] =np.squeeze(model1.predict_proba(X_test))
				predScores2[0,:] =np.squeeze(model2.predict_proba(X_test))
				model=load_model(curDir+ 'model/combine_model_'+ str(model_name) + '.hdf5')
			Y_pred1 = np.average(predScores1, axis=0)
			Y_pred2 = np.average(predScores2, axis=0)
			Y_pred=np.zeros((len(Y_pred1),2))
			for j in range(len(Y_pred1)):
				Y_pred[j,0]=Y_pred1[j]
				Y_pred[j,1]=Y_pred2[j]
			result=model.predict_proba(Y_pred)
			result=[math.exp((1-value)*math.log(50000))for value in result]
			predicted_labels = [1 if score <= 500 else 0 for score in result]
	elif model_type_name =='classification':
		if model_complete_name == 'whole_model':
			predScores = np.zeros((5, len(X_test)))
			for i in range(5):
				with CustomObjectScope({'Attention': Attention}):
					model=load_model(curDir+ 'model/classification_'+ str(model_name) + '_' + str(i)+ '.hdf5')
					predScores[i,:] =np.squeeze(model.predict_proba(X_test))
			result = np.average(predScores, axis=0)
			predicted_labels = [1 if score >=0.5 else 0 for score in result]
		elif model_complete_name == 'best_model':
			predScores = np.zeros((1, len(X_test)))
			with CustomObjectScope({'Attention': Attention}):
				model=load_model(curDir+ 'model/classification_'+ str(model_name) + '_3.hdf5')
				predScores[0,:] =np.squeeze(model.predict_proba(X_test))
			result = np.average(predScores, axis=0)
			predicted_labels = [1 if score >=0.5 else 0 for score in result]
				
	with open(WD + '/' + fname + '_' + str(model_type_name) + '_' + str(model_name) + '_' + str(model_complete_name) + '_predcited_result.txt','w') as f:
		f.write('Annotation\tHLA\tPeptide\tAffinity\tBinding level\n')
		if (opt.file):
			for i in range(len(result)):
				f.write(str(df.Annotation[i]) + '\t' + str(df.HLA[i]) + '\t' + str(df.peptide[i]) + '\t' + str(result[i]) + '\t' + str(predicted_labels[i]) + '\n')
		else:
			f.write('single peptide\t' + str(hla) + '\t' + str(peptide) + '\t' + str(result[0]) + '\t' + str(predicted_labels[0]) + '\n')
	f.close()
	
	j = datetime.datetime.now()
	print (str(j) + ' Prediction end\n')

