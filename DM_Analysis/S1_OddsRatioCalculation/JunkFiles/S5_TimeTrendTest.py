
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
mydf = pd.read_csv(dpath + 'p_values_NA85_raw.csv')

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
myout_df = pd.merge(trend_df, mydf, how = 'left', on = ['FieldID_full'])

myout_df.to_csv(dpath + 'Trend_test_results.csv', index = False)
