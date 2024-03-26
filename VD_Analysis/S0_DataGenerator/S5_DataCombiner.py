

import glob
import os
import numpy as np
import pandas as pd
import re

def strech_df(df):
    my_lst = []
    for i in range(len(df)):
        my_lst += df.iloc[i,:].tolist()
    return list(set(my_lst))

dpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/VD_Analysis/'
case_id_df = pd.read_csv(dpath + 'S21_case_control_eid_df_matched.csv')
mydata_df = pd.read_csv(dpath + 'S41_UKB_pheno_matched_NA80.csv')
subject_info_df = pd.read_csv(dpath + 'S22_VD_Target_matched.csv', usecols=['eid', 'BL2VD_yrs'])
case_control_id_df = pd.merge(case_id_df, subject_info_df, how = 'left', left_on=['case_id'], right_on= ['eid'])

outdf = pd.DataFrame()

for i in range(len(case_control_id_df)):
    tmpdf = pd.DataFrame({'eid': case_control_id_df.iloc[i,:11]})
    tmpdf.reset_index(inplace=True)
    tmpdf.drop(['index'], axis = 1, inplace = True)
    tmpdf['BL2VD_yrs'] = case_control_id_df['BL2VD_yrs'].iloc[i]
    tmpdf['case_control'] = pd.DataFrame([1] + [0]*10)
    outdf = pd.concat((outdf, tmpdf), axis = 0)

outdf['eid'] = outdf['eid'].astype(int)
mydata_df = pd.merge(outdf, mydata_df, how = 'left', on= ['eid'])
mydata_df['eid'] = mydata_df['eid'].astype(int)

outdf.to_csv(dpath + 'S50_case_control_eid_df_matched_NA80.csv', index = False)
mydata_df.to_csv(dpath + 'S51_case_control_ukb_pheno_NA80.csv', index = False)

