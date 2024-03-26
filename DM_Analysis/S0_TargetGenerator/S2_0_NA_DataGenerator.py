

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
outpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/DM_Analysis/'
feature_df = pd.read_csv(dpath + 'UKB_FieldID_Subset.csv')
eid_df = pd.read_csv(dpath + 'UKB_eid.csv')
# age, gender, centers, TDI, Ethnicity,

target_FieldID = ['20019-0.0', '20021-0.0',
                  '4232-0.1', '4243-0.1', '4803-0.0',
                  '5078-0.0', '5079-0.0',
                  '4123-0.0', '4124-0.0', '4104-0.0', '4105-0.0',
                  '23409-0.0', '23439-0.0', '23499-0.0',
                  '23532-0.0', '23556-0.0', '23470-0.0']

mydf = read_data(target_FieldID, feature_df, eid_df)

mydf.to_csv(outpath + 'S20_NA_TMP_Data.csv', index = False)

