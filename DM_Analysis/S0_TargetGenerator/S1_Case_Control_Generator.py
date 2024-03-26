


import glob
import os
import numpy as np
import pandas as pd
import re
from joblib import Parallel, delayed
import multiprocessing
import time

t = time.time()

def get_days_intervel(start_date_var, end_date_var, df):
    start_date = pd.to_datetime(df[start_date_var], dayfirst=True)
    end_date = pd.to_datetime(df[end_date_var], dayfirst=True)
    nb_of_dates = start_date.shape[0]
    days = [(end_date[i] - start_date[i]).days for i in range(nb_of_dates)]
    my_yrs = [ele/365 for ele in days]
    return pd.DataFrame(my_yrs)


dpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/DM_Analysis/'
outpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/DM_Analysis/'
mydf = pd.read_csv(dpath + 'S0_DM_Target.csv')

case_df = mydf.loc[mydf['DM'] == 1]
case_df.reset_index(inplace = True)
case_df.drop(['index'], axis = 1, inplace = True)
control_df = mydf.loc[mydf['DM'] == 0]
control_df.reset_index(inplace = True)
control_df.drop(['index'], axis = 1, inplace = True)


def get_match_subject(case_id, case_df, control_df):
    tmp_case = case_df[case_df['eid'] == case_id]
    tmp_case_flyrs = float(tmp_case['BL2Now_yrs'])
    tmp_case_adyrs = float(tmp_case['BL2DM_yrs'])
    tmp_case_age = float(tmp_case['21022-0.0'])
    tmp_case_gender = int(tmp_case['31-0.0'])
    tmp_case_ethnicity = int(tmp_case['21000-0.0'])
    tmp_case_education = int(tmp_case['Education'])
    tmp_case_TDI = int(tmp_case['189-0.0'])
    tmp_control_f = control_df.loc[control_df['BL2Now_yrs'] >= tmp_case_flyrs]
    tmp_control_fa = tmp_control_f.loc[((pd.isna(tmp_control_f['40000-0.0'])) | (tmp_control_f['BL2Death_yrs'] >= tmp_case_adyrs))]
    tmp_control_faa = tmp_control_fa.loc[((tmp_control_fa['21022-0.0'] >= tmp_case_age - 2) & (tmp_control_fa['21022-0.0'] <= tmp_case_age + 2))]
    tmp_control_faag = tmp_control_faa.loc[tmp_control_faa['31-0.0'] == tmp_case_gender]
    tmp_control_faage = tmp_control_faag.loc[tmp_control_faag['21000-0.0'] == tmp_case_ethnicity]
    tmp_control_faagee = tmp_control_faage.loc[((tmp_control_faage['Education'] >= tmp_case_education - 1) & (tmp_control_faage['Education'] <= tmp_case_education + 1))]
    tmp_control_faageet = tmp_control_faagee.loc[((tmp_control_faagee['189-0.0'] >= tmp_case_TDI - 0.5) & (tmp_control_faagee['189-0.0'] <= tmp_case_TDI + 0.5))]
    if len(tmp_control_faageet) < 10:
        tmp_control_faageet = tmp_control_faagee
    if len(tmp_control_faagee) < 30:
        tmp_control_faageet = tmp_control_faage
    if len(tmp_control_faage) < 30:
        tmp_control_faageet = tmp_control_faag
    return tmp_control_faageet['eid'].tolist()


def get_match_population(case_df, control_df):
    results = []
    case_eid = case_df['eid'].tolist()
    i = 0
    for eid in case_eid:
        control_eids = get_match_subject(eid, case_df, control_df)
        results.append([len(control_eids)] + [eid] + control_eids)
        i+=1
        if i % 250 == 0:
            print(i)
    return results

case_control_eid = get_match_population(case_df, control_df)
case_control_eid_df = pd.DataFrame(case_control_eid)

case_control_eid_df.columns = ['nb_available_controls', 'case_ids'] + \
                              [str(ele) for ele in range(1, case_control_eid_df.shape[1]-1)]

case_control_eid_df.sort_values(by=['nb_available_controls'], ascending= True, inplace= True)
rm_idx = case_control_eid_df.index[case_control_eid_df['nb_available_controls'] < 10]
case_control_eid_df.drop(rm_idx, axis = 0, inplace = True)
case_control_eid_df.reset_index(inplace = True)
case_control_eid_df.drop(['index'], axis = 1, inplace = True)

case_control_eid_df.to_csv(outpath + 'S1_case_control_eid_df.csv', index = False)

print(time.time() - t)

print('finished')


