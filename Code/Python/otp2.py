#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 12:55:08 2017

@author: yuchenli
@content: otp2 merge with PROC1_PROCMOD_mode
"""

import pandas as pd
import csv

# Convert cpt_table to dictionary
CPT_dict = dict()
cpt_table = open("/Users/yuchenli/Box Sync/Yuchen_project/"
                 'MarketScan_update_Mark_Goodhart/Data/cpt_table',
                 encoding = "ISO-8859-1")
reader4 = csv.reader(cpt_table)
for row in reader4:
    key = "b:" + str(row[0])
    value_list = list()
    value = str(row[1])
    
    if key in CPT_dict:
        trash1 = CPT_dict[key]
        trash1.append(value)
        CPT_dict[key] = trash1
    else:
        value_list.append(value)
        CPT_dict[key] = value_list 
        
        
# Read PROC1_PROCTYP
PROC1_PROCTYP = dict()
snippet2 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/PROC1_PROCTYP.csv',
               encoding = 'utf-8')
reader2 = csv.reader(snippet2)
for row in reader2:
    proctyp = row[1][2:3]
    if (proctyp == '1'):
        PROC1_PROCTYP[row[0]] = 'CPT'
    if (proctyp == '7'):
        PROC1_PROCTYP[row[0]] = 'HCPCS'
    if (proctyp == '8'):
        PROC1_PROCTYP[row[0]] = 'ADA'
        
        
# Read PROC1_PROCMOD_mode
PROC1_PROCMOD_mode = dict()
snippet5 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/PROC1_PROCMOD_mode.csv',
               encoding = 'utf-8')
reader5 = csv.reader(snippet5)
for row in reader5:
    trash_dict = dict()
    trash_dict['PROCMOD_mode'] = row[1]
    trash_dict['PROCMOD_mode_count'] = row[2]
    PROC1_PROCMOD_mode[row[0]] = trash_dict
    
    
# Combine otp2 with PROC_PROCMOD_frequency
otp2 = pd.read_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                    'MarketScan_update_Mark_Goodhart/Data/otp2.csv')

PROC1_b = list()
PROC1_b_PROCMOD_mode = list()
PROC1_b_PROCMOD_mode_count = list()
PROC1_b_Description = list()
PROC1_b_PROCTYP = list()


# The grand merge
for i in range(len(otp2)):
    proc1 = "b:" + otp2.loc[i,'PROC1']
    PROC1_b.append(proc1)
    PROC1_b_PROCTYP.append(PROC1_PROCTYP[proc1])
    if (proc1 in PROC1_PROCMOD_mode):
        PROC1_b_PROCMOD_mode.append(PROC1_PROCMOD_mode[proc1]['PROCMOD_mode'])
        PROC1_b_PROCMOD_mode_count.append(PROC1_PROCMOD_mode[proc1]['PROCMOD_mode_count'])
    else:
        PROC1_b_PROCMOD_mode.append("NA")
        PROC1_b_PROCMOD_mode_count.append("NA")  
    if (proc1 in CPT_dict):
        PROC1_b_Description.append(CPT_dict[proc1])
    else:
        PROC1_b_Description.append("NA")
        
otp2['PROC1_b'] = PROC1_b
otp2['PROC1_b_PROCMOD_mode'] = PROC1_b_PROCMOD_mode
otp2['PROC1_b_PROCMOD_mode_count'] = PROC1_b_PROCMOD_mode_count
otp2['PROC1_b_Description'] = PROC1_b_Description
otp2['PROC1_b_PROCTYP'] = PROC1_b_PROCTYP

otp2.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
            'MarketScan_update_Mark_Goodhart/Data/otp2_1.csv',
            encoding = 'utf-8')
    