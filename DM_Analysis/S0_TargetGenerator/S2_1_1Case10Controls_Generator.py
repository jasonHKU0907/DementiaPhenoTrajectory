


import glob
import os
import numpy as np
import pandas as pd
import re
import random

def sort_by_na(eid_lst, df):
    tmpdf = pd.DataFrame({'eid': eid_lst})
    tmpdf = pd.merge(tmpdf, df, how = 'left', on = ['eid'])
    tmpdf['NA_prop'] = tmpdf.isnull().sum(axis=1)
    tmpdf.sort_values(by = ['NA_prop'], ascending= True)
    return tmpdf.eid.tolist()

dpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/DM_Analysis/'
ca_cl_df = pd.read_csv(dpath + 'S1_case_control_eid_df.csv')
na_tmpdf = pd.read_csv(dpath + 'S20_NA_TMP_Data.csv')

id_pool = []
for i in range(len(ca_cl_df)):
    tmp_id_lst = ca_cl_df.iloc[i, 2:].dropna().tolist()
    id_pool = id_pool + tmp_id_lst
    if i%100 == 0:
        print(i)

id_pool = list(set(id_pool))

myout, unmatched_case = [], []
j = 1
for i in range(len(ca_cl_df)):
    tmp_case_id = ca_cl_df['case_ids'][i]
    tmp_control_ids_full = ca_cl_df.iloc[i, 2:].dropna().tolist()
    tmp_control_ids_avaiable = list(set(id_pool).intersection(tmp_control_ids_full))
    tmp_control_ids_avaiable = sort_by_na(tmp_control_ids_avaiable, na_tmpdf)
    if len(tmp_control_ids_avaiable) >=10:
        tmp_control_ids_select = tmp_control_ids_avaiable[:10]
        tmpp = [id_pool.remove(ele) for ele in tmp_control_ids_select]
        myout.append([tmp_case_id] + tmp_control_ids_select)
    else:
        print((j, len(tmp_control_ids_avaiable), i))
        j += 1
        unmatched_case.append(tmp_case_id)
    if i%100 == 0:
        print(i)

myout = pd.DataFrame(myout)
myout.columns = ['case_id',
                 'control_id1', 'control_id2', 'control_id3', 'control_id4', 'control_id5',
                 'control_id6', 'control_id7', 'control_id8', 'control_id9', 'control_id10']
myout.to_csv(dpath + 'S21_case_control_eid_df_matched.csv', index = False)

subject_info_df = pd.read_csv(dpath + 'S0_DM_Target.csv')
myeid = []
for i in range(len(myout)):
    myeid += myout.iloc[i,:].tolist()

myeid = pd.DataFrame({'eid': myeid})
subject_info_subdf = pd.merge(myeid, subject_info_df, how = 'inner', on = ['eid'])

subject_info_subdf.to_csv(dpath + 'S22_DM_Target_matched.csv', index = False)



