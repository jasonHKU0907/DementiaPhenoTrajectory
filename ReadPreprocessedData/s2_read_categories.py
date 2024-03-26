
import glob
import os
import numpy as np
import pandas as pd
import re

def get_remove_cols(mydf, na_prop = 0.8):
    rm_cols1, rm_cols2 = [], []
    for col in mydf.columns:
        if mydf[col].isnull().sum() / len(mydf) >= na_prop:
            rm_cols1.append(col)
        if len(mydf[col].value_counts()) <= 1:
            rm_cols2.append(col)
    rm_cols = rm_cols1 + rm_cols2
    return rm_cols



dpath = '/Volumes/JasonWork/Dataset/UKB_Preprocessed_221009/'
outpath = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Data0/Analysis_Data/'

mydf = pd.read_csv(dpath + 'Biological-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'Biological-data.csv', index = False)


mydf = pd.read_csv(dpath + 'CognitivFunction-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'CognitivFunction-data.csv', index = False)
print(mydf.shape)


mydf = pd.read_csv(dpath + 'EnvironmentalFactors-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'EnvironmentalFactors-data.csv', index = False)
print(mydf.shape)



mydf = pd.read_csv(dpath + 'SocialDemographics-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'SocialDemographics-data.csv', index = False)
print(mydf.shape)


mydf = pd.read_csv(dpath + 'LifeStyle_HealthInfo-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'LifeStyle_HealthInfo-data.csv', index = False)
print(mydf.shape)


mydf = pd.read_csv(dpath + 'Medical_Medication-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'Medical_Medication-data.csv', index = False)
print(mydf.shape)


mydf = pd.read_csv(dpath + 'PhysicalMeasurements-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'PhysicalMeasurements-data.csv', index = False)
print(mydf.shape)


mydf = pd.read_csv(dpath + 'PsychosocialFactors-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'PsychosocialFactors-data.csv', index = False)
print(mydf.shape)


mydf = pd.read_csv(dpath + 'EarlyLife_Family-data.csv')
rm_cols = get_remove_cols(mydf, na_prop = 0.8)
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
mydf.to_csv(outpath + 'EarlyLife_Family-data.csv', index = False)
print(mydf.shape)


mydf1 = pd.read_csv(outpath + 'Biological-data.csv')
mydf2 = pd.read_csv(outpath + 'CognitivFunction-data.csv')
mydf3 = pd.read_csv(outpath + 'EnvironmentalFactors-data.csv')
mydf4 = pd.read_csv(outpath + 'SocialDemographics-data.csv')
mydf5 = pd.read_csv(outpath + 'LifeStyle_HealthInfo-data.csv')
mydf6 = pd.read_csv(outpath + 'Medical_Medication-data.csv')
mydf7 = pd.read_csv(outpath + 'PhysicalMeasurements-data.csv')
mydf8 = pd.read_csv(outpath + 'PsychosocialFactors-data.csv')
mydf9 = pd.read_csv(outpath + 'EarlyLife_Family-data.csv')

mydf = pd.merge(mydf1, mydf2, how = 'inner', on = ['eid'])
#mydf = pd.merge(mydf, mydf3, how = 'inner', on = ['eid'])
#mydf = pd.merge(mydf, mydf4, how = 'inner', on = ['eid'])
mydf = pd.merge(mydf, mydf5, how = 'inner', on = ['eid'])
mydf = pd.merge(mydf, mydf6, how = 'inner', on = ['eid'])
mydf = pd.merge(mydf, mydf7, how = 'inner', on = ['eid'])
mydf = pd.merge(mydf, mydf8, how = 'inner', on = ['eid'])
mydf = pd.merge(mydf, mydf9, how = 'inner', on = ['eid'])
print('done')

mydf.shape
mydf.to_csv(outpath + 'UKB_pheno.csv', index = False)

field_id_lst = mydf1.columns.tolist()[1:] + mydf2.columns.tolist()[1:] + \
               mydf5.columns.tolist()[1:] + mydf6.columns.tolist()[1:] +\
               mydf7.columns.tolist()[1:] + mydf8.columns.tolist()[1:] + mydf9.columns.tolist()[1:]
categories = ['Biological']*(mydf1.shape[1]-1) + ['CognitivFunction']*(mydf2.shape[1]-1) + \
             ['LifeStyle_HealthInfo']*(mydf5.shape[1]-1) + ['Medical_Medication']*(mydf6.shape[1]-1) + \
             ['PhysicalMeasurements']*(mydf7.shape[1]-1) + ['PsychosocialFactors']*(mydf8.shape[1]-1) + \
             ['EarlyLife_Family']*(mydf9.shape[1]-1)

field_id_pure = [int(ele.split('-')[0]) for ele in field_id_lst]

feat_catorgy = pd.DataFrame({'FieldID':field_id_pure,
                             'FieldID_full':field_id_lst,
                             'Category':categories})

feat_catorgy.to_csv(outpath + 'feat_catorgy.csv', index = False)


