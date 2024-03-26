
import glob
import os
import numpy as np
import pandas as pd
import re
import random

dpath1 = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/DM_Analysis/'
dpath2 = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/VD_Analysis/'
ca_cl_df = pd.read_csv(dpath1 + 'S21_case_control_eid_df_matched.csv')
vd_df = pd.read_csv(dpath2 + 'S0_VD_Target.csv')

vd_eid = vd_df['eid'].loc[vd_df.VD == 1]
len(vd_eid)
vd_ca_cl_df = pd.merge(vd_eid, ca_cl_df, how = 'inner', left_on=['eid'], right_on=['case_id'])
vd_ca_cl_df.drop(['eid'], axis = 1, inplace = True)
vd_ca_cl_df.to_csv(dpath2 + 'S21_case_control_eid_df_matched.csv', index = False)

myeid = []
for i in range(len(vd_ca_cl_df)):
    myeid += vd_ca_cl_df.iloc[i,:].tolist()

myeid = pd.DataFrame({'eid': myeid})
subject_info_subdf = pd.merge(myeid, vd_df, how = 'inner', on = ['eid'])

subject_info_subdf.to_csv(dpath2 + 'S22_VD_Target_matched.csv', index = False)

