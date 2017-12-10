#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 14:38:56 2017

@author: yuchenli

@content: tabulate expenditures by PROC1
"""

# Most prevalent PROCMOD for each PROC1
import pandas as pd

# Read proc1_procmod
#==============================================================================
# procmod = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
#                       'MarketScan_update_Mark_Goodhart/Data/PROCMOD_2015_'
#                       'frequency.csv', sep = ",", encoding = 'utf-8')
# 
# proc1_procmod_frequency = dict()        
# for i in range(len(procmod)):
#     proc1 = procmod.loc[i,'PROC1']
#     procmod_1 = str(procmod.loc[i,'PROCMOD'])
#     if (procmod_1 == 'nan'):
#         continue
#         
#     count = int(procmod.loc[i,'count'])
#     
#     list_trash1 = [procmod_1,count]
#     
#     if (proc1 in proc1_procmod_frequency):
#         count_existing = proc1_procmod_frequency[proc1][1]
#         if count_existing < count:
#             proc1_procmod_frequency[proc1] = list_trash1            
#     else:
#         proc1_procmod_frequency[proc1] = list_trash1
#==============================================================================
        

# Read sas7bdat
#otp1 = pd.read_sas('/Users/yuchenli/Box Sync/Yuchen_project/'
#                   'MarketScan_update_Mark_Goodhart/Data/otp1.sas7bdat')
otp2 = pd.read_sas('/Users/yuchenli/Box Sync/Yuchen_project/'
                   'MarketScan_update_Mark_Goodhart/Data/otp2.sas7bdat')
otp3 = pd.read_sas('/Users/yuchenli/Box Sync/Yuchen_project/'
                   'MarketScan_update_Mark_Goodhart/Data/otp3.sas7bdat')

#otp1.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
#            'MarketScan_update_Mark_Goodhart/Data/otp1.csv', sep = ',',
#            encoding = 'utf-8')

otp2.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
            'MarketScan_update_Mark_Goodhart/Data/otp2.csv', sep = ',',
            encoding = 'utf-8')

otp3.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
            'MarketScan_update_Mark_Goodhart/Data/otp3.csv', sep = ',',
            encoding = 'utf-8')

# Join tables: otp2_1 and proc1_procmod_frequency
otp2_1 = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                      'MarketScan_update_Mark_Goodhart/Data/otp2_1.csv',
                      sep = ",", encoding = 'utf-8')

#==============================================================================
# overlap = set(otp2_1.PROC1) & set(proc1_procmod_frequency.keys())
# len(overlap)
# len(otp2_1.PROC1)
# 
# trash1 = list()
# trash2 = list()
# for i in range(len(otp2_1)):
#     if (otp2_1.loc[i,'PROC1'] in proc1_procmod_frequency):
#         trash1.append(list(proc1_procmod_frequency[otp2_1.loc[i,'PROC1']])[0])
#         trash2.append(list(proc1_procmod_frequency[otp2_1.loc[i,'PROC1']])[1])
#     else:
#         trash1.append('NA')
#         trash2.append('NA')
# 
# otp2_1['PROCMOD_Mode'] = trash1
# otp2_1['PROCMOD_Mode_Count'] = trash2
# 
# otp2_1.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
#             'MarketScan_update_Mark_Goodhart/Data/otp2_2.csv', sep = ',',
#             encoding = 'utf-8')
#==============================================================================
