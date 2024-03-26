

import glob
import os
import numpy as np
import pandas as pd
import re
dpath = '/Volumes/JasonWork/UKB_Data/'
f_dict = pd.read_csv(dpath + 'Feature_Dict.csv')
mydf0 = pd.read_csv(dpath + 'subset_data0.csv', nrows = 100)
mydf1 = pd.read_csv(dpath + 'subset_data1.csv', nrows = 100)
mydf2 = pd.read_csv(dpath + 'subset_data2.csv', nrows = 100)
mydf3 = pd.read_csv(dpath + 'subset_data3.csv', nrows = 100)
mydf4 = pd.read_csv(dpath + 'subset_data4.csv', nrows = 100)

mydf0_f = mydf0.columns.tolist()[2:]
mydf1_f = mydf1.columns.tolist()[2:]
mydf2_f = mydf2.columns.tolist()[2:]
mydf3_f = mydf3.columns.tolist()[2:]
mydf4_f = mydf4.columns.tolist()[2:]

mydf0_f_fieldID = [int(ele.split('_')[0][1:]) for ele in mydf0_f]
mydf0_f_fieldID = pd.DataFrame({'FieldID': list(set(mydf0_f_fieldID))})
mydf0_dict = pd.merge(mydf0_f_fieldID, f_dict, how = 'left', on = ['FieldID'])
#mydf0_dict.to_csv(dpath + 'subset_data0_dict.csv', index = False)

mydf1_f_fieldID = [int(ele.split('.')[0][1:]) for ele in mydf1_f]
mydf1_f_fieldID = pd.DataFrame({'FieldID': list(set(mydf1_f_fieldID))})
mydf1_dict = pd.merge(mydf1_f_fieldID, f_dict, how = 'left', on = ['FieldID'])
#mydf1_dict.to_csv(dpath + 'subset_data1_dict.csv', index = False)

mydf2_f_fieldID = [int(ele.split('.')[0][1:]) for ele in mydf2_f]
mydf2_f_fieldID = pd.DataFrame({'FieldID': list(set(mydf2_f_fieldID))})
mydf2_dict = pd.merge(mydf2_f_fieldID, f_dict, how = 'left', on = ['FieldID'])
#mydf2_dict.to_csv(dpath + 'subset_data2_dict.csv', index = False)

mydf3_f_fieldID = [int(ele.split('.')[0][1:]) for ele in mydf3_f]
mydf3_f_fieldID = pd.DataFrame({'FieldID': list(set(mydf3_f_fieldID))})
mydf3_dict = pd.merge(mydf3_f_fieldID, f_dict, how = 'left', on = ['FieldID'])
#mydf3_dict.to_csv(dpath + 'subset_data3_dict.csv', index = False)

mydf4_f_fieldID = [int(ele.split('.')[0][1:]) for ele in mydf4_f]
mydf4_f_fieldID = pd.DataFrame({'FieldID': list(set(mydf4_f_fieldID))})
mydf4_dict = pd.merge(mydf4_f_fieldID, f_dict, how = 'left', on = ['FieldID'])
#mydf4_dict.to_csv(dpath + 'subset_data4_dict.csv', index = False)

my_f0 = pd.DataFrame({'FieldID': mydf0_dict['FieldID'], 'Subset': np.zeros(len(mydf0_dict))})
my_f1 = pd.DataFrame({'FieldID': mydf1_dict['FieldID'], 'Subset': np.ones(len(mydf1_dict))*1})
my_f2 = pd.DataFrame({'FieldID': mydf2_dict['FieldID'], 'Subset': np.ones(len(mydf2_dict))*2})
my_f3 = pd.DataFrame({'FieldID': mydf3_dict['FieldID'], 'Subset': np.ones(len(mydf3_dict))*3})
my_f4 = pd.DataFrame({'FieldID': mydf4_dict['FieldID'], 'Subset': np.ones(len(mydf4_dict))*4})

my_f_df = pd.concat((my_f0, my_f1, my_f2, my_f3, my_f4), axis = 0)
my_f_df.to_csv(dpath + 'FieldID_table_raw.csv', index = False)

my_f_df['Subset'].value_counts()



my_f0 = pd.DataFrame({'FieldID': mydf0_f, 'Subset': np.zeros(len(mydf0_f))})
my_f1 = pd.DataFrame({'FieldID': mydf1_f, 'Subset': np.ones(len(mydf1_f))*1})
my_f2 = pd.DataFrame({'FieldID': mydf2_f, 'Subset': np.ones(len(mydf2_f))*2})
my_f3 = pd.DataFrame({'FieldID': mydf3_f, 'Subset': np.ones(len(mydf3_f))*3})
my_f4 = pd.DataFrame({'FieldID': mydf4_f, 'Subset': np.ones(len(mydf4_f))*4})

my_f_df = pd.concat((my_f0, my_f1, my_f2, my_f3, my_f4), axis = 0)
my_f_df.to_csv(dpath + 'FieldID_table_full.csv', index = False)

my_f_df['Subset'].value_counts()

