
import glob
import os
import numpy as np
import pandas as pd
import re

def rename_cols(mydf):
    col_names_old_lst = mydf.columns.tolist()[1:]
    col_name_new_lst = []
    for col_name_old in col_names_old_lst:
        col_name_old = col_name_old[1:]
        if '_' in col_name_old:
            split0, split1 = col_name_old.split('_')
            col_name_new = split0 + '-0.0_' + split1
        if '.' in col_name_old:
            split0, split1, split2 = col_name_old.split('.')
            col_name_new = split0 + '-' + split1 + '.' + split2
        col_name_new_lst.append(col_name_new)
    my_cols = ['eid'] + col_name_new_lst
    return my_cols

def read_data(dpath, FieldID_lst, f_dict_raw, f_dict_full, eid_df):
    subset_df = f_dict_raw[f_dict_raw['FieldID'].isin(FieldID_lst)]
    subset_dict = {k: g['FieldID'].tolist() for k, g in subset_df.groupby('Subset')}
    subset_lst = list(subset_dict.keys())
    my_df = eid_df
    for subset_id in subset_lst:
        tmp_dir = dpath + 'subset_data' + str(int(subset_id)) + '.csv'
        tmp_id = subset_dict[subset_id]
        field_lst_full = f_dict_full['FieldID'].loc[f_dict_full['Subset'] == subset_id].tolist()
        if subset_id == 0:
            tmp_f = [ele for ele in field_lst_full if int(ele[1:].split('_')[0]) in tmp_id]
        elif subset_id != 0:
            tmp_f = [ele for ele in field_lst_full if int(ele[1:].split('.')[0]) in tmp_id]
        try:
            tmp_df = pd.read_csv(tmp_dir, usecols=['eid'] + tmp_f)
        except:
            tmp_df = pd.read_csv(tmp_dir, usecols=['eid'] + tmp_f, encoding='unicode_escape')
        my_df = pd.merge(my_df, tmp_df, how='inner', on=['eid'])
    new_col_names = rename_cols(my_df)
    my_df.columns = new_col_names
    print('Finished Reading Data')
    return my_df


dpath = '/Volumes/JasonWork/UKB_Data/Preprocessed/'
eid_df = pd.read_csv(dpath + 'UKB_eid.csv')
f_dict_raw = pd.read_csv(dpath + 'FieldID_table_raw.csv')
f_dict_full = pd.read_csv(dpath + 'FieldID_table_full.csv')
B_f = pd.read_csv(dpath + 'Biological.csv')['FieldID'].tolist()
CF_f = pd.read_csv(dpath + 'CognitivFunction.csv')['FieldID'].tolist()
EF_f = pd.read_csv(dpath + 'EnvironmentalFactors.csv')['FieldID'].tolist()
SD_f = pd.read_csv(dpath + 'SocialDemographics.csv')['FieldID'].tolist()
LSHI_f = pd.read_csv(dpath + 'LifeStyle_HealthInfo.csv')['FieldID'].tolist()
MM_f = pd.read_csv(dpath + 'Medical_Medication.csv')['FieldID'].tolist()
PM_f = pd.read_csv(dpath + 'PhysicalMeasurements.csv')['FieldID'].tolist()
PSF_f = pd.read_csv(dpath + 'PsychosocialFactors.csv')['FieldID'].tolist()
ELF_f = pd.read_csv(dpath + 'EarlyLife_Family.csv')['FieldID'].tolist()

myf_lst = B_f
print(len(myf_lst))
mydf = read_data(dpath, myf_lst, f_dict_raw, f_dict_full, eid_df)
print(mydf.shape)


rm_cols = [ele for ele in mydf.columns[1:] if int(ele.split('-')[1][0]) > 0]
print(len(rm_cols))
mydf.drop(rm_cols, axis = 1, inplace = True)
col_f = mydf.describe().columns.tolist()
print(len(col_f))
mydf = mydf[col_f]

mydf.to_csv(dpath + 'EarlyLife_Family-data.csv', index = False)
print('done')





