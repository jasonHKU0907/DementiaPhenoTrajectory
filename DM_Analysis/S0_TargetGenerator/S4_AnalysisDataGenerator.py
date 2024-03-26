

import glob
import os
import numpy as np
import pandas as pd
import re

def read_data_numeric(FieldID_lst, feature_df, eid_df):
    subset_df = feature_df[feature_df['Field_ID'].isin(FieldID_lst)]
    subset_dict = {k: ['eid'] + g['Field_ID'].tolist() for k, g in subset_df.groupby('Subset_ID')}
    subset_lst = list(subset_dict.keys())
    my_df = eid_df
    for subset_id in subset_lst:
        tmp_dir = dpath + 'UKB_subset_' + str(subset_id) + '.csv'
        tmp_f = subset_dict[subset_id]
        tmp_df = pd.read_csv(tmp_dir, usecols=tmp_f)
        tmp_f = tmp_df.describe().columns.tolist()
        tmp_df = tmp_df[tmp_f]
        my_df = pd.merge(my_df, tmp_df, how='inner', on=['eid'])
    return my_df

def get_binary(var_source, df):
    tmp_binary = df[var_source].copy()
    tmp_binary.loc[tmp_binary >= -1] = 1
    tmp_binary.replace(np.nan, 0, inplace=True)
    return tmp_binary

def strech_df(df):
    my_lst = []
    for i in range(len(df)):
        my_lst += df.iloc[i,:].tolist()
    return list(set(my_lst))

def get_remove_cols(mydf, na_prop = 0.8):
    rm_cols1, rm_cols2 = [], []
    for col in mydf.columns:
        if mydf[col].isnull().sum() / len(mydf) >= na_prop:
            rm_cols1.append(col)
        if len(mydf[col].value_counts()) <= 1:
            rm_cols2.append(col)
    rm_cols = rm_cols1 + rm_cols2
    return rm_cols

dpath = '/Volumes/JasonWork/Dataset/UKB_Tabular_merged_10/'
dpath1 = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/DM_Analysis/'
dpath2 = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/PhenoData/'

case_id_df = pd.read_csv(dpath1 + 'S21_case_control_eid_df_matched.csv')
subject_info_matched = pd.read_csv(dpath1 + 'S22_DM_Target_matched.csv')
adjust_covariates = subject_info_matched[['eid', '21022-0.0', '31-0.0', 'Education', '189-0.0', '21000-0.0']]
adjust_covariates.columns = ['eid', 'Age', 'Gender', 'Education', 'TDI', 'Ethnicity']

mydf = pd.read_csv(dpath2 + 'S3_UKB_pheno.csv')
mydf_matched = pd.merge(adjust_covariates, mydf, how = 'inner', on = ['eid'])
mydf_matched.to_csv(dpath1 + 'S40_UKB_pheno_matched.csv', index = False)


my_f = mydf_matched.columns.tolist()
rm_cols1 = get_remove_cols(mydf_matched, na_prop = 0.80)
rm_cols2 = [f for f in my_f[8:] if int(f.split('.')[1])>1]
rm_f = list(set(rm_cols1 + rm_cols2))
added_back = ['20019-0.0', '20021-0.0', '20016-0.0', '20018-0.0', '20128-0.0', '4294-0.0', '4290-0.0',
              '4717-0.0', '4728-0.0', '4792-0.0', '4803-0.0', '4232-0.1',
              '4234-0.1', '4235-0.1', '4237-0.1', '4239-0.1', '4243-0.1', '4245-0.1',
              '4246-0.1', '4247-0.1', '4249-0.1', '4269-0.0', '4270-0.0', '4272-0.0',
              '4276-0.0', '4277-0.0', '4279-0.0',
              '4104-0.0', '4105-0.0', '4106-0.0', '4123-0.0', '4124-0.0', '4125-0.0']
rm_f = [f for f in rm_f if f not in added_back]
clean_f = [f for f in my_f if f not in rm_f]

mydf_matched = mydf_matched[clean_f]
mydf_matched.to_csv(dpath1 + 'S41_UKB_pheno_matched_NA80.csv', index = False)

tmp = pd.DataFrame({'FieldID_full': rm_f})
tmp1 = pd.read_csv(dpath2 + 'feat_catorgy.csv')
tmp2 = pd.read_csv(dpath2 + 'Feature_Dict.csv')
tmp = pd.merge(tmp, tmp1, how = 'left', on = ['FieldID_full'])
tmp = pd.merge(tmp, tmp2, how = 'left', on = ['FieldID'])
len(tmp)
tmp.to_csv(dpath2 + 'rm_catorgy80.csv')


combidity_matched = pd.read_csv(dpath2 + 'Combidity_matched.csv')
combidity_matched = combidity_matched[["eid", "Diabetes", "Coronary heart disease", "Stroke",
                                       "Chronic obstructive pulmonary disease", "Depression",
                                       "Arthritis", "Parkinson's Disease", "Hypertension", "Hearing loss",
                                       "Obesity", "Vision impairment"]]

mydf_matched = pd.read_csv(dpath1 + 'S40_UKB_pheno_matched.csv')
mydf_matched = pd.merge(mydf_matched, combidity_matched, how = 'left', on = ['eid'])
mydf_matched.to_csv(dpath1 + 'S40_UKB_pheno_matched.csv', index = False)


mydf_matched = pd.read_csv(dpath1 + 'S41_UKB_pheno_matched_NA80.csv')
mydf_matched = pd.merge(mydf_matched, combidity_matched, how = 'left', on = ['eid'])
mydf_matched.drop(['6145-0.0_1', '6145-0.0_2', '6160-0.0_1'], axis = 1, inplace = True)
mydf_matched['1170-0.0'].replace([1,2,3,4], [0, 0, 1, 1], inplace = True)
mydf_matched['1180-0.0'].replace([1,2,3,4], [1, 1, 0, 0], inplace = True)
mydf_matched['1190-0.0'].replace([1,2,3], [0, 1, 1], inplace = True)
mydf_matched['1200-0.0'].replace([1,2,3], [0, 1, 1], inplace = True)
#mydf_matched['1220-0.0'].replace([0,1,2,3], [0, 0, 1, 1], inplace = True)
mydf_matched['20018-0.0'].replace([0, 1, 2], [0, 2, 1], inplace = True)
mydf_matched['2050-0.0'].replace([1,2,3,4], [0, 1, 1, 1], inplace = True)
mydf_matched['2060-0.0'].replace([1,2,3,4], [0, 1, 1, 1], inplace = True)
mydf_matched['2070-0.0'].replace([1,2,3,4], [0, 1, 1, 1], inplace = True)
mydf_matched['2080-0.0'].replace([1,2,3,4], [0, 1, 1, 1], inplace = True)
mydf_matched['22032-0.0'].replace([0, 1,2], [0, 0, 1], inplace = True)
mydf_matched['2247-0.0'].replace([0, 1, 99], [0, 1, 1], inplace = True)
mydf_matched['2296-0.0'].replace([1,2,3], [0, 1, 1], inplace = True)
mydf_matched['2306-0.0'].replace([0, 2, 3], [1, 2, 0], inplace = True)
mydf_matched['3082-0.0'].replace([0, 1, 2], [0, 1, 0], inplace = True)
mydf_matched['4232-0.1'].replace([0, 1, 9], [0, 1, 0], inplace = True)
mydf_matched['4243-0.1'].replace([0, 1, 9], [0, 1, 0], inplace = True)
mydf_matched['4294-0.0'].replace([0, 1, 9], [0, 1, 0], inplace = True)
mydf_matched['4803-0.0'].replace([0, 11, 12, 13, 14], [0, 1, 1, 1, 0], inplace = True)
mydf_matched['924-0.0'].replace([1,2,3], [0, 1, 2], inplace = True)
mydf_matched.to_csv(dpath1 + 'S41_UKB_pheno_matched_NA80.csv', index = False)





