#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 15:30:03 2017

@author: yuchenli
@content: explore otp1.csv
"""

import math
import statistics
import csv
import time
import pandas as pd

#==============================================================================
# # Convert cpt_table to csv
# with open('/Users/yuchenli/Box Sync/Yuchen_project/'
#           'MarketScan_update_Mark_Goodhart/Data/cpt_table',
#           encoding = 'utf-16') as infile:
#     with open('/Users/yuchenli/Box Sync/Yuchen_project/'
#               'MarketScan_update_Mark_Goodhart/Data/cpt_table.csv', "w",
#               encoding = 'utf-8') as outfile:
#         reader = csv.reader(infile)
#         fieldnames = next(reader)
#         writer = csv.writer(outfile, delimiter=',')
#         writer.writerow(fieldnames)
#         for row in reader:
#             writer.writerow(row)
#==============================================================================
    
   
# Snippet
snippet = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/otp1_subset.csv',
               encoding = 'utf-8')
reader = csv.reader(snippet)
next(reader)       


# Calculate PROC1_frequency, PROC1_PROCTYP
#PROCTYP_frequency

snippet1 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/otp1_subset.csv',
               encoding = 'utf-8')
reader1 = csv.reader(snippet1)

PROC1_frequency = dict()
#PROCTYP_frequency = dict()
PROC1_PROCTYP = dict()

start_time = time.time()
i=0
for row in reader1:
    if (i==0):
        i+=1
        continue
    i+=1
    trash1 = list()
    proc1 = str(row[0]) 
    proctyp = str(row[1])
        
    if (proc1 in PROC1_frequency):
        PROC1_frequency[proc1] += 1
    else:
        PROC1_frequency[proc1] = 1
        
#==============================================================================
#     if (proctyp in PROCTYP_frequency):
#         PROCTYP_frequency[proctyp] += 1
#     else:
#         PROCTYP_frequency[proctyp] = 1
#==============================================================================
        
    if (proc1 in PROC1_PROCTYP):
        if proctyp in PROC1_PROCTYP[proc1]:
            pass
        else:
            trash2 = PROC1_PROCTYP[proc1]
            trash2.append(proctyp)
            PROC1_PROCTYP[proc1] = trash2
    else:
        trash1.append(proctyp)
        PROC1_PROCTYP[proc1] = trash1
        
print("--- %s seconds ---" % (time.time() - start_time))       

import csv
with open('/Users/yuchenli/Box Sync/Yuchen_project/MarketScan_update_'
          'Mark_Goodhart/Data/PROC1_frequency.csv', "w") as csvfile:
    fieldnames = ['proc1', "frequency"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in PROC1_frequency.items():
        try:
            writer.writerow({'proc1': ("b:" + key), "frequency": value})
        except:
            pass
        
import csv
with open('/Users/yuchenli/Box Sync/Yuchen_project/MarketScan_update_'
          'Mark_Goodhart/Data/PROC1_PROCTYP.csv', "w") as csvfile:
    fieldnames = ['proc1', "PROCTYP"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in PROC1_PROCTYP.items():
        try:
            writer.writerow({'proc1': ("b:" + key), "PROCTYP": value})
        except:
            pass


# Generate FLAG count
snippet6 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/otp1.csv',
               encoding = 'utf-8')
reader7 = csv.reader(snippet6)
PROC1_FLAG = dict()
i = 0
for row in reader7:
    if (i == 0):
        i+=1
        continue
    i+=1
    ofc = row[6]
    otp = row[7]
    asc = row[8]
    proc1 = str(row[2]) 
    
    if (proc1 in PROC1_FLAG):
        if (ofc == '1'):
            PROC1_FLAG[proc1]['ofc'] +=1
        else:
            PROC1_FLAG[proc1]['zero'] +=1
        if (otp == '1'):
            PROC1_FLAG[proc1]['otp'] +=1
        else:
            PROC1_FLAG[proc1]['zero'] +=1
        if (asc == '1'):
            PROC1_FLAG[proc1]['asc'] +=1
        else:
            PROC1_FLAG[proc1]['zero'] +=1
        
    else:
        flag_trash = dict()
        flag_trash['zero'] = 0
        flag_trash['ofc'] = 0
        flag_trash['otp'] = 0
        flag_trash['asc'] = 0
        if (ofc == '1'):
            flag_trash['ofc'] +=1
        else:
            flag_trash['zero'] +=1
        if (otp == '1'):
            flag_trash['otp'] +=1
        else:         
            flag_trash['zero'] += 1
        if (asc == '1'):
            flag_trash['asc'] +=1  
        else:
            flag_trash['zero'] += 1
        PROC1_FLAG[proc1] = flag_trash
        
with open('/Users/yuchenli/Box Sync/Yuchen_project/MarketScan_update_'
          'Mark_Goodhart/Data/FLAG_count.csv', "w") as csvfile:
    fieldnames = ['proc1', "ofc", "otp", "asc", 'zero']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in PROC1_FLAG.items():
        try:
            writer.writerow({'proc1': ("b:" + key), 'ofc': value['ofc'],
                             "otp": value['otp'], 'asc': value['asc'],
                             "zero": value['zero']})
        except:
            pass
  
      
# Generate PHYSPAY and TOTPAY mean and cv (running algorithm)

#==============================================================================
# Let n ← 0, Sum ← 0, SumSq ← 0
# For each datum x:
#   n ← n + 1
#   Sum ← Sum + x
#   SumSq ← SumSq + x × x
# Var = (SumSq − (Sum × Sum) / n) / (n − 1)
#==============================================================================

PROC1_PHYSPAY_TOTPAY_stat = dict()

snippet5 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/otp1.csv',
               encoding = 'utf-8')
reader5 = csv.reader(snippet5)
n=0

start_time = time.time()
for row in reader5:
    if n == 0:
        n+=1
        continue
    n+=1  # count   
    print(n)
    proc1 = str(row[2])
    physpay = float(row[9])
    totpay = float(row[10])
    if (proc1 in PROC1_PHYSPAY_TOTPAY_stat):
        PROC1_PHYSPAY_TOTPAY_stat[proc1]['PHYSPAY_count'] +=1
        PROC1_PHYSPAY_TOTPAY_stat[proc1]['TOTPAY_count'] +=1
        PROC1_PHYSPAY_TOTPAY_stat[proc1]['PHYSPAY_sum'] += physpay
        PROC1_PHYSPAY_TOTPAY_stat[proc1]['TOTPAY_sum'] += totpay
        PROC1_PHYSPAY_TOTPAY_stat[proc1]['PHYSPAY_sumsq'] += (physpay * physpay)
        PROC1_PHYSPAY_TOTPAY_stat[proc1]['TOTPAY_sumsq'] += (totpay * totpay)
        
        count_trash = PROC1_PHYSPAY_TOTPAY_stat[proc1]['PHYSPAY_count']
        sum_trash = PROC1_PHYSPAY_TOTPAY_stat[proc1]['PHYSPAY_sum']
        sumsq_trash = PROC1_PHYSPAY_TOTPAY_stat[proc1]['PHYSPAY_sumsq']
        PROC1_PHYSPAY_TOTPAY_stat[proc1]['PHYSPAY_var'] = (sumsq_trash - \
        (sum_trash * sum_trash)/count_trash)/(count_trash - 1)
        
        count_trash = PROC1_PHYSPAY_TOTPAY_stat[proc1]['TOTPAY_count']
        sum_trash = PROC1_PHYSPAY_TOTPAY_stat[proc1]['TOTPAY_sum']
        sumsq_trash = PROC1_PHYSPAY_TOTPAY_stat[proc1]['TOTPAY_sumsq']
        PROC1_PHYSPAY_TOTPAY_stat[proc1]['TOTPAY_var'] = (sumsq_trash - \
        (sum_trash * sum_trash)/count_trash)/(count_trash - 1)        
        
    else:
        trash1 = dict()
        trash1['PHYSPAY_count'] = 1
        trash1['TOTPAY_count'] = 1
        trash1['PHYSPAY_sum'] = physpay
        trash1['PHYSPAY_sumsq'] = physpay * physpay
        trash1['TOTPAY_sum'] = totpay
        trash1['TOTPAY_sumsq'] = totpay * totpay
        trash1['PHYSPAY_var'] = 0
        trash1['TOTPAY_var'] = 0
        PROC1_PHYSPAY_TOTPAY_stat[proc1] = trash1
    
print("--- %s seconds ---" % (time.time() - start_time)) 

with open('/Users/yuchenli/Box Sync/Yuchen_project/MarketScan_update_'
          'Mark_Goodhart/Data/PROC1_PHYSPAY_TOTPAY_stat.csv', "w") as csvfile:
    fieldnames = ['proc1', "PHYSPAY_mean", "PHYSPAY_cv", "TOTPAY_mean",\
                  "TOTPAY_cv", "PHYSPAY_total"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in PROC1_PHYSPAY_TOTPAY_stat.items():
        try:
            writer.writerow({'proc1': ("b:" + key), 
                             'PHYSPAY_mean': value['PHYSPAY_sum']/value['PHYSPAY_count'],
                             'PHYSPAY_cv': math.sqrt(value['PHYSPAY_stdev'])/(value['PHYSPAY_sum']/value['PHYSPAY_count']),
                             'TOTPAY_mean': value['TOTPAY_sum']/value['TOTPAY_count'],
                             'TOTPAY_cv': math.sqrt(value['TOTPAY_stdev'])/(value['TOTPAY_sum']/value['TOTPAY_count']),
                             'PHYSPAY_total': value['PHYSPAY_sum']})
        except:
            pass      

        
#==============================================================================
# # Calculate mean and cv for PHYSPAY and TOTPAY
# PROC1_PHYSPAY_STATS = dict()
# PROC1_TOTPAY_STATS = dict()
# 
# start_time = time.time()
# for key1 in PROC1_PHYSPAY:
#     trash1 = dict()
#     trash1['mean'] = statistics.mean(PROC1_PHYSPAY[key1])
#     trash1['cv'] = statistics.stdev(PROC1_PHYSPAY[key1])/trash1['mean']
#     PROC1_PHYSPAY_STATS[key1] = trash1
# 
# for key2 in PROC1_TOTPAY:  
#     trash2 = dict()
#     trash2['mean'] = statistics.mean(PROC1_TOTPAY[key2])
#     trash1['cv'] = statistics.stdev(PROC1_TOTPAY[key2])/trash2['mean']
#     PROC1_TOTPAY_STATS[key2] = trash2   
# print("--- %s seconds ---" % (time.time() - start_time))         
# 
# with open('/Users/yuchenli/Box Sync/Yuchen_project/MarketScan_update_'
#           'Mark_Goodhart/Data/PROC1_PHYSPAY_STATS.csv', "w") as csvfile:
#     fieldnames = ['proc1', "PHYSPAY_mean", 'PHYSPAY_cv']
#     writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
#     writer.writeheader()
#     for key, value in PROC1_PHYSPAY_STATS.items():
#         try:
#             writer.writerow({'proc1': ("b:" + key), 
#                              'PHYSPAY_mean': value['mean'],
#                              'PHYSPAY_cv': value['cv']})
#         except:
#             pass
# 
# with open('/Users/yuchenli/Box Sync/Yuchen_project/MarketScan_update_'
#           'Mark_Goodhart/Data/PROC1_TOTPAY_STATS.csv', "w") as csvfile:
#     fieldnames = ['proc1', "TOTPAY_mean", 'TOTPAY_cv']
#     writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
#     writer.writeheader()
#     for key, value in PROC1_TOTPAY_STATS.items():
#         try:
#             writer.writerow({'proc1': ("b:" + key), 
#                              'TOTPAY_mean': value['mean'],
#                              'TOTPAY_cv': value['cv']})
#         except:
#             pass
#==============================================================================
 
    
# Calculate PROC1_PROCMOD_frequency
PROC1_PROCMOD_frequency = dict()

snippet2 = open("/Users/yuchenli/Box Sync/Yuchen_project/"
               'MarketScan_update_Mark_Goodhart/Data/otp1_subset.csv',
               encoding = 'utf-8')
reader2 = csv.reader(snippet2)
i=0
start_time = time.time()
for row in reader2:
    if (i==0):
        i+=1
        continue
    i+=1
    trash1 = dict()
    PROC1 = str(row[0])
    PROCMOD = str(row[2])
    if PROCMOD == '':
        continue
    else:
        if (PROC1 in PROC1_PROCMOD_frequency):
            if (PROCMOD in PROC1_PROCMOD_frequency[PROC1]):
                PROC1_PROCMOD_frequency[PROC1][PROCMOD] += 1
            else:
                PROC1_PROCMOD_frequency[PROC1][PROCMOD] = 1
        else:
            trash1[PROCMOD] = 1
            PROC1_PROCMOD_frequency[PROC1] = trash1
print("--- %s seconds ---" % (time.time() - start_time)) 

def keywithmaxval_key(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]
 
def keywithmaxval_value(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     return v[v.index(max(v))]
 
PROC1_PROCMOD_mode = dict()
for key in PROC1_PROCMOD_frequency:
    PROCMOD_list = PROC1_PROCMOD_frequency[key]
    PROCMOD = {'PROCMOD': keywithmaxval_key(PROCMOD_list),\
               'count': keywithmaxval_value(PROCMOD_list)}
    PROC1_PROCMOD_mode[key] = PROCMOD
    
with open('/Users/yuchenli/Box Sync/Yuchen_project/MarketScan_update_'
          'Mark_Goodhart/Data/PROC1_PROCMOD_mode.csv', "w") as csvfile:
    fieldnames = ['proc1', "PROCMOD", "count"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in PROC1_PROCMOD_mode.items():
        try:
            writer.writerow({'proc1': ("b:" + key),
                             "PROCMOD": 'b:' + value['PROCMOD'],
                             "count": value['count']})
        except:
            pass 

#==============================================================================
# start_time = time.time()
# temp = pd.read_csv("/Users/yuchenli/Box Sync/Yuchen_project/"
#                    'MarketScan_update_Mark_Goodhart/NIKE/otp1.csv',
#                    encoding = 'utf-8')
# print("--- %s seconds ---" % (time.time() - start_time)) 
#==============================================================================

# Combine otp2 with PROC_PROCMOD_frequency
#==============================================================================
# otp2 = pd.read_sas('/Users/yuchenli/Box Sync/Yuchen_project/'
#                    'MarketScan_update_Mark_Goodhart/Data/otp2.sas7bdat')
#==============================================================================
