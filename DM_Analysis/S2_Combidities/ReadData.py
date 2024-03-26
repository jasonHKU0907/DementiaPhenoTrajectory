

import glob
import os
import numpy as np
import pandas as pd
import re

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

dpath1 = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Data/Combidity/'
dpath2 = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Data/DM_Analysis/DM_Prior/'

'''
fo_df = pd.read_csv(dpath1 + 'Death_FirstOccurrences.csv')
info_df = pd.read_csv(dpath2 + 'DM_Target_matched.csv')
info_df = info_df[['eid', '53-0.0', 'DM', 'DM_date', 'BL2DM_yrs', 'AD', 'AD_date', 'BL2AD_yrs']]
mydf = pd.merge(info_df, fo_df, how = 'left', on = ['eid'])
mydf.to_csv(dpath1 + 'Death_FirstOccurrences_matched.csv', index=False)
'''

fo_df = pd.read_csv(dpath1 + 'Death_FirstOccurrences_matched.csv')
fo_diseases = fo_df.columns.tolist()[8:]
bl2disease_df = fo_df[['eid', '53-0.0', 'DM',  'DM_date', 'BL2DM_yrs', 'AD', 'AD_date', 'BL2AD_yrs']]
target_date_f = '53-0.0'

for disease in fo_diseases:
    bl2disease_df[disease] = get_days_intervel(target_date_f, disease, fo_df)

bl2disease_df.to_csv(dpath1 + 'BL2FO_yrs_matched.csv', index=False)


bl2disease_df.iloc[:,8:] = bl2disease_df.iloc[:,8:] < 0
bl2disease_df.iloc[:,8:] = bl2disease_df.iloc[:,8:].astype('int')
bl2disease_df.to_csv(dpath1 + 'BL2FO_binary_matched.csv', index=False)



