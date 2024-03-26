

import glob
import os
import numpy as np
import pandas as pd
import re
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
pd.options.mode.chained_assignment = None  # default='warn'

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def get_normalization(mydf):
    tmp_df = mydf.copy()
    for col in tmp_df.columns:
        tmp_df[col] = (tmp_df[col]-tmp_df[col].mean()) / tmp_df[col].std()
    return tmp_df

def get_binarization(mydf):
    tmp_df = pd.get_dummies(mydf).iloc[:,1]
    return tmp_df

def preprocess_df(mydf, target_f):
    tmp_df = mydf.copy()
    tmp_df = pd.get_dummies(data=tmp_df, columns=['Ethnicity'])
    #tmp_df.columns = tmp_df.columns.tolist()[:7] + ['Ethnicity_Others', 'Ethnicity_White', 'Ethnicity_Asian', 'Ethnicity_Black']
    # normalize if it is not binarized variable
    if len(tmp_df[target_f].value_counts()) > 2:
        tmp_df[target_f] = get_normalization(tmp_df[[target_f]])
        # remove missing values (row manipulation)
        tmp_df.dropna(axis=0, inplace=True)
    elif len(tmp_df[target_f].value_counts()) == 2:
        # remove missing values (row manipulation)
        tmp_df.dropna(axis=0, inplace=True)
        tmp_df[target_f] = get_binarization(tmp_df[target_f])
    # remove without information (levels < 2) (column manipulation)
    rm_cols = [col for col in tmp_df.columns if len(tmp_df[col].value_counts()) <= 1]
    tmp_df.drop(rm_cols, axis = 1, inplace = True)
    return tmp_df

def read_preprocessed_df(file_path):
    mydf = pd.read_csv(file_path)
    mydf[['Age', 'Education', 'TDI']] = get_normalization(mydf[['Age', 'Education', 'TDI']])
    return mydf

dpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/VD_Analysis/Partition_NA80/'
outpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Results/VD_Analysis/'
f_df = pd.read_csv('/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/PhenoData/Feature_Dict.csv')
f_category = pd.read_csv('/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/PhenoData/feat_catorgy.csv')
f_category = f_category[['FieldID_full', 'Feature_Category']]

out_file_multi = outpath + 'S0_Results.csv'
my_files = sorted(glob.glob(dpath + '*.csv'), key=numericalSort)
tmp = read_preprocessed_df(my_files[0])
all_result_df_multi = pd.DataFrame({'FieldID_full':tmp.columns[8:]})


for file in my_files:
    mydf = read_preprocessed_df(file)
    suffix = os.path.basename(file).split('_')[1].split('.')[0]
    my_f = mydf.columns.tolist()[8:]
    result_df_uni, result_df_multi = pd.DataFrame(), pd.DataFrame()
    for f in my_f:
        try:
            tmp_df = mydf[[f] + ['case_control', 'BL2VD_yrs', 'Age', 'Gender', 'Education', 'TDI', 'Ethnicity']]
            tmp_df = preprocess_df(tmp_df, target_f = f)
            Y = tmp_df['case_control']
            X_multi = tmp_df[[f] + tmp_df.columns.tolist()[2:]]
            mod_multi = sm.Logit(Y, sm.add_constant(X_multi)).fit()
            coef_multi, coef_p_multi = np.round(np.exp(mod_multi.params[1]),3), mod_multi.pvalues[1]
            ci_multi = mod_multi.conf_int(alpha=0.05)
            lci_multi, uci_multi = np.round(np.exp(ci_multi.iloc[1, 0]),3), np.round(np.exp(ci_multi.iloc[1, 1]),3)
            OR_multi = [f, coef_multi, coef_p_multi, lci_multi, uci_multi]
            result_df_multi = pd.concat((result_df_multi, pd.DataFrame(OR_multi).T), axis = 0)
        except:
            pass
    result_df_multi.columns = ['FieldID_full', 'OR_'+ suffix, 'p_'+ suffix, 'lci_'+ suffix, 'uci_'+ suffix]
    all_result_df_multi = pd.merge(all_result_df_multi, result_df_multi, how = 'left', on = ['FieldID_full'])
    print('done' + os.path.basename(file))


all_result_df_multi['FieldID'] = pd.DataFrame([int(ele.split('-')[0]) for ele in all_result_df_multi['FieldID_full'][:398]])
all_result_df_multi = pd.merge(all_result_df_multi, f_category, how = 'left', on = ['FieldID_full'])
all_result_df_multi = pd.merge(all_result_df_multi, f_df, how = 'left', on = ['FieldID'])

all_result_df_multi.to_csv(out_file_multi, index=False)

