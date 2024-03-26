

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

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def get_normalization(mydf):
    tmp_df = mydf.copy()
    for col in tmp_df.columns:
        tmp_df[col] = (tmp_df[col]-tmp_df[col].mean()) / tmp_df[col].std()
    return tmp_df

def get_binarization(mydf):
    tmp_df = pd.get_dummies(mydf).iloc[:,1]
    return tmp_df

def preprocess_df(mydf, f):
    tmpdf = mydf[[f] + ['case_control', 'BL2DM_yrs', 'Age', 'Gender', 'Education', 'TDI', 'Ethnicity']]
    tmpdf.rename(columns={f: 'Y'}, inplace=True)
    tmpdf.dropna(axis=0, inplace=True)
    tmpdf.reset_index(inplace=True)
    rm_cols = ['index'] + [col for col in tmpdf.columns if len(tmpdf[col].value_counts()) <= 1]
    tmpdf.drop(rm_cols, axis=1, inplace=True)
    tmpdf[['BL2DM_yrs', 'Age', 'Education', 'TDI']] = get_normalization(tmpdf[['BL2DM_yrs', 'Age', 'Education', 'TDI']])
    return tmpdf

def read_preprocessed_df(file_path):
    mydf = pd.read_csv(file_path)
    mydf['TDI'].replace(np.nan, mydf['TDI'].median(), inplace=True)
    mydf[['Age', 'Education', 'TDI']] = get_normalization(mydf[['Age', 'Education', 'TDI']])
    return mydf

dpath = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Data/DM_Analysis/DM_Prior/Matched_Analysis/'
outpath = '/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Results/DM_Analysis/DM_Prior/Matched_Analysis/'
f_df = pd.read_csv('/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Data/PhenoData/Feature_Dict.csv')
f_category = pd.read_csv('/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Data/PhenoData/feat_catorgy.csv')
f_category = f_category[['FieldID_full', 'Feature_Category']]

mydf = pd.read_csv(dpath + 'ZscoreMethods/case_control_ukb_pheno_NA80.csv')
my_f = mydf.columns.tolist()[8:]

varType_lst, f_lst = [], []
p_case_lst = []

for f in my_f:
    try:
        tmpdf = preprocess_df(mydf, f)
        nb_levels = len(tmpdf.Y.value_counts())
        formula = 'Y ~ C(case_control) + BL2DM_yrs + Age + Gender + Education + TDI + C(Ethnicity)'
        p_case = 1
        if nb_levels == 2:
            varType = 'Binary'
            tmpdf.Y = get_binarization(tmpdf.Y)
            lm = logit(formula, tmpdf).fit()
            p_case = lm.pvalues[1]
        elif (nb_levels > 2) & (nb_levels <= 5):
            varType = 'Ordinal'
            lm = OrderedModel.from_formula(formula, tmpdf, distr='logit').fit(method='bfgs')
            p_case = lm.pvalues[0]
        elif nb_levels >= 6:
            varType = 'Continuous'
            tmpdf.Y = (tmpdf.Y - tmpdf.Y.mean()) / tmpdf.Y.std()
            lm = ols(formula, tmpdf).fit()
            p_case = lm.pvalues[1]
        else:
            pass
        varType_lst.append(varType)
        p_case_lst.append(p_case)
        f_lst.append(f)
    except:
        pass

reject1_case, p_case_bfi = bonferroni_correction(p_case_lst, alpha=0.05)
reject2_case, p_case_fdr = fdrcorrection(p_case_lst)

myout_df = pd.DataFrame({'FieldID_full': f_lst, 'varType': varType_lst,
                         'p_case_lst': p_case_lst, 'p_case_fdr': p_case_fdr, 'p_case_bfi': p_case_bfi})

myout_df['FieldID'] = pd.DataFrame([int(ele.split('-')[0]) for ele in myout_df['FieldID_full'][:394]])
myout_df = pd.merge(myout_df, f_category, how = 'left', on = ['FieldID_full'])
myout_df = pd.merge(myout_df, f_df, how = 'left', on = ['FieldID'])

or_df = pd.read_csv(outpath + 'ALL/Multivariate.csv')
or_df = or_df[['FieldID_full',
               'OR_0to5yrs', 'OR_0to3yrs', 'OR_3to5yrs', 'OR_5to6yrs', 'OR_5to7yrs', 'OR_6to7yrs', 'OR_7to8yrs',
               'OR_8to9yrs', 'OR_9to10yrs', 'OR_10to11yrs', 'OR_11to12yrs', 'OR_12to15yrs',
               'p_0to5yrs', 'p_0to3yrs', 'p_3to5yrs', 'p_5to6yrs', 'p_5to7yrs', 'p_6to7yrs', 'p_7to8yrs',
               'p_8to9yrs', 'p_9to10yrs', 'p_10to11yrs', 'p_11to12yrs', 'p_12to15yrs']]
myout_df = myout_df[['FieldID_full', 'varType',
                      'p_case_lst', 'p_case_fdr', 'p_case_bfi',
                      'FieldID', 'Feature_Category', 'Path', 'Category', 'Field',
                      'Participants', 'Items', 'Units', 'Sexed', 'Notes']]
myout_df = pd.merge(myout_df, or_df, how = 'left', on = ['FieldID_full'])

reject_case, p_case_fdr0 = fdrcorrection(myout_df.p_0to5yrs.fillna(1))
reject_case, p_case_fdr1 = fdrcorrection(myout_df.p_0to3yrs.fillna(1))
reject_case, p_case_fdr2 = fdrcorrection(myout_df.p_3to5yrs.fillna(1))
reject_case, p_case_fdr3 = fdrcorrection(myout_df.p_5to6yrs.fillna(1))
reject_case, p_case_fdr4 = fdrcorrection(myout_df.p_6to7yrs.fillna(1))
reject_case, p_case_fdr5 = fdrcorrection(myout_df.p_7to8yrs.fillna(1))
reject_case, p_case_fdr6 = fdrcorrection(myout_df.p_8to9yrs.fillna(1))
reject_case, p_case_fdr7 = fdrcorrection(myout_df.p_9to10yrs.fillna(1))
reject_case, p_case_fdr8 = fdrcorrection(myout_df.p_10to11yrs.fillna(1))
reject_case, p_case_fdr9 = fdrcorrection(myout_df.p_11to12yrs.fillna(1))
reject_case, p_case_fdr10 = fdrcorrection(myout_df.p_12to15yrs.fillna(1))

myout_df['p_0to5yrs_fdr'] = pd.DataFrame(p_case_fdr0)
myout_df['p_0to3yrs_fdr'] = pd.DataFrame(p_case_fdr1)
myout_df['p_3to5yrs_fdr'] = pd.DataFrame(p_case_fdr2)
myout_df['p_5to6yrs_fdr'] = pd.DataFrame(p_case_fdr3)
myout_df['p_6to7yrs_fdr'] = pd.DataFrame(p_case_fdr4)
myout_df['p_7to8yrs_fdr'] = pd.DataFrame(p_case_fdr5)
myout_df['p_8to9yrs_fdr'] = pd.DataFrame(p_case_fdr6)
myout_df['p_9to10yrs_fdr'] = pd.DataFrame(p_case_fdr7)
myout_df['p_10to11yrs_fdr'] = pd.DataFrame(p_case_fdr8)
myout_df['p_11to12yrs_fdr'] = pd.DataFrame(p_case_fdr9)
myout_df['p_12to15yrs_fdr'] = pd.DataFrame(p_case_fdr10)

myout_df.to_csv(outpath + 'NA80/p_values_NA80_raw.csv', index=False)

info_df = pd.read_csv('/Volumes/JasonWork/Projects/UKB_NEUR_PRODROME/Results1/DM_Analysis/DM_Prior/Matched_Analysis/NA80/p_values_NA80_sig1.csv')
info_df = info_df[['FieldID_full', 'Feature_Category_sub', 'Feature_Category', 'WHF-Field', 'Field', 'Feature_Category_sub1', 'Feature_Category1', 'Figure2', 'Figure3']]
myout_df = pd.merge(myout_df, info_df, how = 'left', on=['FieldID_full'])
myout_df.to_csv(outpath + 'NA80/p_values_NA80_raw.csv', index=False)

myout_df = pd.read_csv(outpath + 'NA80/p_values_NA80_raw.csv')
rm_df = myout_df.loc[(myout_df.p_0to5yrs_fdr>0.05)]
rm_df.to_csv(outpath + 'NA80/p_values_NA80_unsig.csv', index=False)

my_df = myout_df.loc[(myout_df.p_0to5yrs_fdr<0.05) | (myout_df.p_0to3yrs_fdr<0.05) | (myout_df.p_3to5yrs_fdr<0.05)]
my_df.to_csv(outpath + 'NA80/p_values_NA80_sig.csv', index=False)

