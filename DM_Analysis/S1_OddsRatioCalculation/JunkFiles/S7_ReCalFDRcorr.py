

import glob
import os
import numpy as np
import pandas as pd
import re
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.formula.api import logit
from statsmodels.miscmodels.ordinal_model import OrderedModel
from statsmodels.stats.multitest import fdrcorrection
from statsmodels.stats.multitest import multipletests
from mne.stats import bonferroni_correction
pd.options.mode.chained_assignment = None  # default='warn'

dpath = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Results/DM_Analysis/DM_Prior/Matched_Analysis/NA80/Plots/'
mydf = pd.read_csv(dpath + 'SigData.csv')
mydf = mydf.loc[mydf.Figure2>=0]
mydf.reset_index(inplace = True)
mydf.drop(['index'], axis =1, inplace = True)

p_case_lst = mydf.p_case_lst
reject1_case, p_case_bfi = bonferroni_correction(p_case_lst, alpha=0.05)
reject2_case, p_case_fdr = fdrcorrection(p_case_lst)

p_0to5yrs_lst = mydf.p_0to5yrs
reject_case, p_0to5yrs_fdr = fdrcorrection(p_0to5yrs_lst.fillna(1))

p_0to3yrs_lst = mydf.p_0to3yrs
reject_case, p_0to3yrs_fdr = fdrcorrection(p_0to3yrs_lst.fillna(1))

p_3to5yrs_lst = mydf.p_3to5yrs
reject_case, p_3to5yrs_fdr = fdrcorrection(p_3to5yrs_lst.fillna(1))

p_5to6yrs_lst = mydf.p_5to6yrs
reject_case, p_5to6yrs_fdr = fdrcorrection(p_5to6yrs_lst.fillna(1))

p_5to7yrs_lst = mydf.p_5to7yrs
reject_case, p_5to7yrs_fdr = fdrcorrection(p_5to7yrs_lst.fillna(1))

p_6to7yrs_lst = mydf.p_6to7yrs
reject_case, p_6to7yrs_fdr = fdrcorrection(p_6to7yrs_lst.fillna(1))

p_7to8yrs_lst = mydf.p_7to8yrs
reject_case, p_7to8yrs_fdr = fdrcorrection(p_7to8yrs_lst.fillna(1))

p_8to9yrs_lst = mydf.p_8to9yrs
reject_case, p_8to9yrs_fdr = fdrcorrection(p_8to9yrs_lst.fillna(1))

p_9to10yrs_lst = mydf.p_9to10yrs
reject_case, p_9to10yrs_fdr = fdrcorrection(p_9to10yrs_lst.fillna(1))

p_10to11yrs_lst = mydf.p_10to11yrs
reject_case, p_10to11yrs_fdr = fdrcorrection(p_10to11yrs_lst.fillna(1))

p_11to12yrs_lst = mydf.p_11to12yrs
reject_case, p_11to12yrs_fdr = fdrcorrection(p_11to12yrs_lst.fillna(1))

p_12to15yrs_lst = mydf.p_12to15yrs
reject_case, p_12to15yrs_fdr = fdrcorrection(p_12to15yrs_lst.fillna(1))

mydf['p_case_fdr1'] = pd.DataFrame(p_case_fdr)
mydf['p_case_bfi1'] = pd.DataFrame(p_case_bfi)

mydf['p_0to5yrs_fdr1'] = pd.DataFrame(p_0to5yrs_fdr)
mydf['p_0to3yrs_fdr1'] = pd.DataFrame(p_0to3yrs_fdr)
mydf['p_3to5yrs_fdr1'] = pd.DataFrame(p_3to5yrs_fdr)
mydf['p_5to6yrs_fdr1'] = pd.DataFrame(p_5to6yrs_fdr)
mydf['p_5to7yrs_fdr1'] = pd.DataFrame(p_5to7yrs_fdr)
mydf['p_6to7yrs_fdr1'] = pd.DataFrame(p_6to7yrs_fdr)
mydf['p_7to8yrs_fdr1'] = pd.DataFrame(p_7to8yrs_fdr)
mydf['p_8to9yrs_fdr1'] = pd.DataFrame(p_8to9yrs_fdr)
mydf['p_9to10yrs_fdr1'] = pd.DataFrame(p_9to10yrs_fdr)
mydf['p_10to11yrs_fdr1'] = pd.DataFrame(p_10to11yrs_fdr)
mydf['p_11to12yrs_fdr1'] = pd.DataFrame(p_11to12yrs_fdr)
mydf['p_12to15yrs_fdr1'] = pd.DataFrame(p_12to15yrs_fdr)

mydf.to_csv(dpath + 'SigData1.csv', index = False)

