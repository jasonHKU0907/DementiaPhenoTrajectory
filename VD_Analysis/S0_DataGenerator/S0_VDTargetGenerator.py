

import glob
import os
import numpy as np
import pandas as pd
import re

def read_data(FieldID_lst, feature_df, eid_df):
    subset_df = feature_df[feature_df['Field_ID'].isin(FieldID_lst)]
    subset_dict = {k: ['eid'] + g['Field_ID'].tolist() for k, g in subset_df.groupby('Subset_ID')}
    subset_lst = list(subset_dict.keys())
    my_df = eid_df
    for subset_id in subset_lst:
        tmp_dir = dpath + 'UKB_subset_' + str(subset_id) + '.csv'
        tmp_f = subset_dict[subset_id]
        tmp_df = pd.read_csv(tmp_dir, usecols=tmp_f)
        my_df = pd.merge(my_df, tmp_df, how='inner', on=['eid'])
    return my_df

def get_days_intervel(start_date_var, end_date_var, df):
    start_date = pd.to_datetime(df[start_date_var], dayfirst=True)
    end_date = pd.to_datetime(df[end_date_var], dayfirst=True)
    nb_of_dates = start_date.shape[0]
    days = [(end_date[i] - start_date[i]).days for i in range(nb_of_dates)]
    my_yrs = [ele/365 for ele in days]
    return pd.DataFrame(my_yrs)

def get_binary(var_source, df):
    tmp_binary = df[var_source].copy()
    tmp_binary.loc[tmp_binary >= -1] = 1
    tmp_binary.replace(np.nan, 0, inplace=True)
    return tmp_binary


dpath = '/Volumes/JasonWork/Dataset/UKB_Tabular_merged_10/'
outpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/VD_Analysis/'
feature_df = pd.read_csv(dpath + 'UKB_FieldID_Subset.csv')
eid_df = pd.read_csv(dpath + 'UKB_eid.csv')
# age, gender, centers, TDI, Ethnicity,

target_FieldID = ['53-0.0', '190-0.0',
                  '21022-0.0', '31-0.0', '54-0.0',
                  '189-0.0', '21000-0.0', '6138-0.0', '845-0.0',
                  '40000-0.0',
                  '130838-0.0', '130839-0.0', '42022-0.0', '42023-0.0']

mydf = read_data(target_FieldID, feature_df, eid_df)
mydf1 = pd.read_csv('/Volumes/JasonWork/Dataset/UKB_PreCalculation/Qualifications/education1.csv')
mydf1['Education'].replace(np.nan, 8, inplace = True)
mydf = pd.merge(mydf, mydf1, how = 'inner', on = ['eid'])

mydf['21000-0.0'].replace([1002, 1003, 3002, 3003, 5,    3004, 4002, 4003, 4,    1,    2001, 2002, 2003, 2004, 3,  2, -1, -3, np.nan],
                          [1001, 1001, 3001, 3001, 3001, 3001, 4001, 4001, 4001, 1001, 6,    6,    6,    6,    6,  6,  6,  6, 6], inplace = True)
mydf['21000-0.0'].value_counts()
# 1001: white; 3001: Asian; 4001: black; 6: Mixed & Others & Unknown

mydf['Education'].replace(np.nan, 8, inplace = True)
mydf['189-0.0'].replace(np.nan, np.mean(mydf['189-0.0']), inplace = True)


mydf['130838-0.0'].replace(['1900-01-01', '1901-01-01', '1902-02-02', '1903-03-03', '2037-07-07'], np.nan, inplace = True)
mydf['42022-0.0'].replace(['1900-01-01', '1901-01-01', '1902-02-02', '1903-03-03', '2037-07-07'], np.nan, inplace = True)
mydf['130839-0.0_binary'] = get_binary('130839-0.0', mydf)
mydf['42023-0.0_binary'] = get_binary('42023-0.0', mydf)


mydf['VD'] = mydf['130839-0.0_binary'] + mydf['42023-0.0_binary']
mydf['VD'].loc[mydf['VD']>1] = 1
vd_date_df = mydf[['130838-0.0', '42022-0.0']].copy()
mydf['VD_date'] = pd.DataFrame([pd.to_datetime(vd_date_df.iloc[i,:], dayfirst=True).min() for i in range(len(vd_date_df))])

mydf['DateAcquire'] = '2022-07-15'
mydf['BL2Now_yrs'] = get_days_intervel('53-0.0', 'DateAcquire', mydf)
mydf['BL2Death_yrs'] = get_days_intervel('53-0.0', '40000-0.0', mydf)
mydf['BL2VD_yrs'] = get_days_intervel('53-0.0', 'VD_date', mydf)
mydf['VD2Now_yrs'] = get_days_intervel('VD_date', 'DateAcquire', mydf)
mydf['VD2Death_yrs'] = get_days_intervel('VD_date', '40000-0.0', mydf)


rm_idx1 = mydf.index[mydf['190-0.0'] >=0]
# remove participants diagnosed Dementia upon death registry
# rm_idx2 = mydf.index[mydf['BL2Death_yrs'] <= mydf['BL2AD_yrs']]
# remove participants diagnosed Dementia over 15 years (largely)
rm_idx3 = mydf.index[mydf['BL2VD_yrs'] > 15]
# remove participants diagnosed Dementia before the baseline visit
rm_idx4 = mydf.index[mydf['BL2VD_yrs'] <=0]

rm_idx = list(set(rm_idx1.tolist() + rm_idx3.tolist() + rm_idx4.tolist()))
len(rm_idx)
mydf.drop(rm_idx, axis = 0, inplace = True)
mydf.reset_index(inplace = True)
mydf.drop(['index'], axis = 1, inplace = True)
print(mydf['VD'].value_counts())

mydf.to_csv(outpath + 'S0_VD_Target.csv', index = False)

