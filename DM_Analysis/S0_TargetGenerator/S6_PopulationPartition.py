

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

dpath = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/DM_Analysis/'
outpath = dpath + 'Partition_NA80/'
case_id_df = pd.read_csv(dpath + 'S21_case_control_eid_df_matched.csv')
subject_info_df = pd.read_csv(dpath + 'S22_DM_Target_matched.csv', usecols=['eid', 'BL2DM_yrs'])
case_control_id_df = pd.merge(case_id_df, subject_info_df, how = 'left', left_on=['case_id'], right_on= ['eid'])
control_lst = ['control_id1', 'control_id2', 'control_id3', 'control_id4', 'control_id5',
               'control_id6', 'control_id7', 'control_id8', 'control_id9', 'control_id10']
mydf = pd.read_csv(dpath + 'S51_case_control_ukb_pheno_NA80.csv')


start_lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 3, 6, 9, 12, 0, 3, 12, 5, 10]
end_lst =   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 3, 6, 9, 12,15, 5, 5, 15, 10,15]


for i in range(len(start_lst)):
    start, end = int(start_lst[i]), int(end_lst[i])
    outfile = 'PriorDM_' + str(start) + 'to' + str(end) + 'yrs.csv'
    my_idx = mydf.index[(mydf['BL2DM_yrs'] > start) & (mydf['BL2DM_yrs'] <= end)]
    tmpdf = mydf.copy()
    tmpdf = tmpdf.iloc[my_idx]
    tmpdf.reset_index(inplace = True)
    tmpdf.drop(['index'], axis = 1, inplace = True)
    tmpdf.to_csv(outpath + outfile, index = False)

