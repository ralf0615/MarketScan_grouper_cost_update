#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 13:16:05 2017

@author: yuchenli
@content: the grand merge
"""

import math
import statistics
import csv
import time
import pandas as pd

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
        
# Read PROC1_frequency
PROC1_frequency = dict()
snippet1 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/PROC1_frequency.csv',
               encoding = 'utf-8')
reader1 = csv.reader(snippet1)
for row in reader1:
    PROC1_frequency[row[0]] = row[1]
    

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
        
    

# Read FLAG_count
FLAG_count = dict()
snippet3 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/FLAG_count.csv',
               encoding = 'utf-8')
reader3 = csv.reader(snippet3)
for row in reader3:
    trash_dict = dict()
    trash_dict['ofc'] = row[1]
    trash_dict['otp'] = row[2]
    trash_dict['asc'] = row[3]
    FLAG_count[row[0]] = trash_dict


# Read payment stats
PROC1_PHYSPAY_TOTPAY_stat = dict()
snippet4 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/PROC1_PHYSPAY_TOTPAY_stat.csv',
               encoding = 'utf-8')
reader4 = csv.reader(snippet4)
for row in reader4:
    trash_dict = dict()
    trash_dict['PHYSPAY_mean'] = row[1]
    trash_dict['PHYSPAY_cv'] = row[2]
    trash_dict['TOTPAY_mean'] = row[3]
    trash_dict['TOTPAY_cv'] = row[4]
    trash_dict['PHYSPAY_total'] = row[5]
    PROC1_PHYSPAY_TOTPAY_stat[row[0]] = trash_dict
 
    
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
    


# Write to csv
import csv
with open('/Users/yuchenli/Box Sync/Yuchen_project/MarketScan_update_'
          'Mark_Goodhart/Data/result_1.csv', "w") as csvfile:
    fieldnames = ['proc1','PROCTYP', 'count', 'proc1_description', 
                  "PROCMOD_mode", "PROCMOD_mode_count", 'OFC',
                  'OTP', 'ASC', 'PHYSPAY_mean', 'PHYSPAY_cv',
                  'TOTPAY_mean', 'TOTPAY_cv', 'PHYSPAY_total']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in PROC1_frequency.items():
        try:
            if (key in PROC1_PROCMOD_mode):
                PROCMOD_mode = PROC1_PROCMOD_mode[key]['PROCMOD_mode']
                PROCMOD_mode_count = PROC1_PROCMOD_mode[key]['PROCMOD_mode_count']
            else:
                PROCMOD_mode = "NA"
                PROCMOD_mode_count = "NA"  
                
            writer.writerow({'proc1': key, 
                             'PROCTYP': PROC1_PROCTYP[key],
                             "count": value, 
                             "proc1_description": CPT_dict[key],
                             "PROCMOD_mode": PROCMOD_mode,
                             "PROCMOD_mode_count": PROCMOD_mode_count,                             
                             'OFC': int(FLAG_count[key]['ofc'])/int(value),
                             'OTP': int(FLAG_count[key]['otp'])/int(value),
                             'ASC': int(FLAG_count[key]['asc'])/int(value), 
                             'PHYSPAY_mean': PROC1_PHYSPAY_TOTPAY_stat[key]['PHYSPAY_mean'], 
                             'PHYSPAY_cv': PROC1_PHYSPAY_TOTPAY_stat[key]['PHYSPAY_cv'],
                             'TOTPAY_mean': PROC1_PHYSPAY_TOTPAY_stat[key]['TOTPAY_mean'], 
                             'TOTPAY_cv': PROC1_PHYSPAY_TOTPAY_stat[key]['TOTPAY_cv'], 
                             'PHYSPAY_total': PROC1_PHYSPAY_TOTPAY_stat[key]['PHYSPAY_total']})
        except:
            pass
