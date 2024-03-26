


import glob
import os
import numpy as np
import pandas as pd
import re

def read_data(FieldID_lst, feature_df, eid_df, dpath):
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

dpath0 = '/Volumes/JasonWork/Dataset/UKB_Tabular_merged_10/'
dpath1 = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Data/Combidity/'
dpath2 = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Data/DM_Analysis/DM_Prior/'

feature_df = pd.read_csv(dpath0 + 'UKB_FieldID_Subset.csv')
eid_df = pd.read_csv(dpath0 + 'UKB_eid.csv')
mydf0 = read_data(['131213-0.0'], feature_df, eid_df, dpath0)

com_dates_df = pd.read_csv(dpath1 + 'Death_FirstOccurrences_matched.csv')
com_dates_df = pd.merge(com_dates_df, mydf0, how = 'left', on = ['eid'])

com_ids_df = pd.read_csv(dpath1 + 'CombidityIDs.csv')
com_fo_df = com_dates_df[['eid', '53-0.0', 'DM',  'DM_date', 'BL2DM_yrs', 'AD', 'AD_date', 'BL2AD_yrs']]
diseases_lst = com_ids_df.columns.tolist()

for disease in diseases_lst:
    fo_ids = com_ids_df[disease].dropna().tolist()
    fo_ids = [str(int(ele)) + '-0.0' for ele in fo_ids]
    dis_df = com_dates_df[fo_ids]
    dis_df.replace(['1900-01-01', '1901-01-01', '1902-02-02', '1903-03-03', '2037-07-07'], np.nan, inplace = True)
    com_fo_df[disease] = pd.DataFrame([pd.to_datetime(dis_df.iloc[i,:], dayfirst=True).min() for i in range(len(dis_df))])


fo_diseases = com_fo_df.columns.tolist()[8:]
bl2disease_df = com_fo_df[['eid', '53-0.0', 'DM',  'DM_date', 'BL2DM_yrs', 'AD', 'AD_date', 'BL2AD_yrs']]
target_date_f = '53-0.0'

for disease in fo_diseases:
    bl2disease_df[disease] = get_days_intervel(target_date_f, disease, com_fo_df)

bl2disease_df.iloc[:,8:] = bl2disease_df.iloc[:,8:] < 0
bl2disease_df.iloc[:,8:] = bl2disease_df.iloc[:,8:].astype('int')
bl2disease_df.to_csv(dpath1 + 'Combidity_matched.csv', index=False)

bl2disease_df = pd.read_csv(dpath1 + 'Combidity_matched.csv')
case_df = bl2disease_df.loc[bl2disease_df.DM == 1].iloc[:, 8:]
control_df = bl2disease_df.loc[bl2disease_df.DM == 0].iloc[:, 8:]

round(case_df.sum(axis = 0)/7627*100)
round(control_df.sum(axis = 0)/76270*100)



