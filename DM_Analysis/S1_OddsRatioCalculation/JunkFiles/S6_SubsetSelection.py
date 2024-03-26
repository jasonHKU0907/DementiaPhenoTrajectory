
import glob
import os
import numpy as np
import pandas as pd
import re
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
import pymannkendall as mk
from Utility.Mann_Kendall_test import test as mkt
import statsmodels.api as sm
from statsmodels.stats.multitest import fdrcorrection

dpath = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Results/DM_Analysis/DM_Prior/Matched_Analysis/NA85/'
mydf = pd.read_csv(dpath + 'p_values_NA85_inter.csv')

start_lst = [0, 3, 5, 6, 7, 8, 9,  10, 11, 12]
end_lst   = [3, 5, 6, 7, 8, 9, 10, 11, 12, 15]

nb_ivs = len(start_lst)
or_cols = ['FieldID_full'] + ['OR_' + str(start_lst[i]) + 'to' + str(end_lst[i]) + 'yrs' for i in range(nb_ivs)]
pv_cols = ['FieldID_full'] + ['p_' + str(start_lst[i]) + 'to' + str(end_lst[i]) + 'yrs' for i in range(nb_ivs)]

or_df = mydf[or_cols]
pv_df = mydf[pv_cols]

iv_lst = np.sort(list(set(start_lst + end_lst)))
iv_yrs = [(iv_lst[i] + iv_lst[i+1])/2 for i in range(nb_ivs)]
x = sm.add_constant(iv_yrs)

p_trend_lst = []
for i in range(len(mydf)):
    tmp_ods = np.array(or_df.iloc[i,1:]).astype('float')
    model = sm.OLS(tmp_ods, x).fit()
    p_trend = model.pvalues[1]
    p_trend_lst.append(p_trend)

p_trend_lst = pd.DataFrame(p_trend_lst)
p_trend_lst.fillna(1, inplace=True)
p_trend_lst = p_trend_lst.iloc[:,0].tolist()
reject2_trend, p_trend_fdr = fdrcorrection(p_trend_lst)

trend_df = pd.DataFrame({'FieldID_full':mydf['FieldID_full'], 'p_trend':p_trend_lst, 'p_trend_fdr':p_trend_fdr})
mydf = pd.merge(trend_df, mydf, how = 'left', on = ['FieldID_full'])

check_df = mydf.loc[(mydf.p_case_bfi>0.05) & (mydf.p_inter_fdr<0.05)]
check_df.to_csv(dpath + 'check_df.csv')
#myout_df.to_csv(dpath + 'Trend_test_results.csv', index = False)



dpath = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Results/DM_Analysis/DM_Prior/Matched_Analysis/NA85/'
mydf = pd.read_csv(dpath + 'p_values_NA85_raw_pp1.csv')
mydf_sub = mydf.loc[(mydf.p_0to3yrs<0.05) | (mydf.p_3to5yrs<0.05)]
len(mydf_sub)
mydf_sub.to_csv(dpath + 'p_values_NA85_raw_pp2.csv')
mydf_sub = mydf.loc[(mydf.p_0to3yrs<0.05)]
len(mydf_sub)
mydf_sub.to_csv(dpath + 'p_values_NA85_raw_pp3.csv')
mydf_sub = mydf.loc[(mydf.p_0to3yrs>0.05) & (mydf.p_3to5yrs>0.05)]
len(mydf_sub)
mydf_sub.to_csv(dpath + 'p_values_NA85_raw_pp4.csv')
mydf_sub = mydf.loc[(mydf.p_0to3yrs<0.05) & (mydf.p_3to5yrs<0.05)]
len(mydf_sub)
mydf_sub.to_csv(dpath + 'p_values_NA85_raw_pp5.csv')




dpath = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Results/DM_Analysis/DM_Prior/Matched_Analysis/NA85/'
mydf = pd.read_csv(dpath + 'p_values_NA85_raw_plot.csv')
mask_matrix = mydf[['p_0to3yrs_mask', 'p_3to5yrs_mask', 'p_5to6yrs_mask', 'p_6to7yrs_mask', 'p_7to8yrs_mask',
                    'p_8to9yrs_mask','p_9to10yrs_mask', 'p_10to11yrs_mask', 'p_11to12yrs_mask', 'p_12to15yrs_mask']]
last_digit = []
for i in range(len(mask_matrix)):
    mask_row = mask_matrix.iloc[i,]
    last_digit.append(np.sum(mask_row))

df = pd.DataFrame({'Sig_yrs': last_digit})
df['Sig_yrs'].replace([1,2,3,4,5,6,7,8,9,10], [3, 5, 6, 7, 8, 9, 10, 11, 12, 15], inplace = True)

mydf = pd.concat((mydf, df), axis = 1)
mydf.to_csv(dpath + 'p_values_NA85_raw_plot1.csv')




