
import glob
import os
import numpy as np
import pandas as pd
import re
import random

dpath1 = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/DM_Analysis/'
dpath2 = '/Volumes/JasonWork/Projects/UKB_DM_Trajectories/Data/AD_Analysis/'
ca_cl_df = pd.read_csv(dpath1 + 'S21_case_control_eid_df_matched.csv')
ad_df = pd.read_csv(dpath2 + 'S0_AD_Target.csv')

ad_eid = ad_df['eid'].loc[ad_df.AD == 1]
len(ad_eid)
ad_ca_cl_df = pd.merge(ad_eid, ca_cl_df, how = 'inner', left_on=['eid'], right_on=['case_id'])
ad_ca_cl_df.drop(['eid'], axis = 1, inplace = True)
ad_ca_cl_df.to_csv(dpath2 + 'S21_case_control_eid_df_matched.csv', index = False)

myeid = []
for i in range(len(ad_ca_cl_df)):
    myeid += ad_ca_cl_df.iloc[i,:].tolist()

myeid = pd.DataFrame({'eid': myeid})
subject_info_subdf = pd.merge(myeid, ad_df, how = 'inner', on = ['eid'])

subject_info_subdf.to_csv(dpath2 + 'S22_AD_Target_matched.csv', index = False)

