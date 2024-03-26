

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
outpath = dpath + 'Partition_NA80/'
mydf = pd.read_csv(dpath + 'S51_case_control_ukb_pheno_NA80.csv')


start_lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 3, 6, 9, 12, 0, 3, 12, 5, 10, 0]
end_lst =   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 3, 6, 9, 12,15, 5, 5, 15, 10,15, 15]


for i in range(len(start_lst)):
    start, end = int(start_lst[i]), int(end_lst[i])
    outfile = 'PriorVD_' + str(start) + 'to' + str(end) + 'yrs.csv'
    my_idx = mydf.index[(mydf['BL2VD_yrs'] > start) & (mydf['BL2VD_yrs'] <= end)]
    tmpdf = mydf.copy()
    tmpdf = tmpdf.iloc[my_idx]
    tmpdf.reset_index(inplace = True)
    tmpdf.drop(['index'], axis = 1, inplace = True)
    tmpdf.to_csv(outpath + outfile, index = False)

