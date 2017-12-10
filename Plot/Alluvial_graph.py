#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 09:21:56 2017

@author: yuchenli
@content: alluvial graph
@update: 2017-10-23 15:16:18:
            Alluvial graph can be plotted online using http://rawgraphs.io/
"""

import json, urllib
import plotly.plotly as py
import pandas as pd
import numpy as np
import csv

#==============================================================================
# # Convert cpt_ccs to dictionary
# cpt_ccs = dict()
# snippet1 = open('/Users/yuchenli/Box Sync/Yuchen_project/'
#                'MarketScan_update_Mark_Goodhart/Plot/CPT_CCS.csv')
# reader1 = csv.reader(snippet1)
# i=0
# for row in reader1:
#     if i==0:
#         i+=1
#         continue
#     i+=1    
#     key = str(row[0])
#     value = {'ccs':str(row[1]), 'ccs_description':str(row[2])}
#     
#     if key in cpt_ccs:
#         continue
#     else:
#         cpt_ccs[key] = value
#==============================================================================


# Convert cpt_procgrp to dictionary
cpt_procgrp = dict()
snippet2 = open('/Users/yuchenli/Box Sync/Yuchen_project/'
               'MarketScan_update_Mark_Goodhart/Plot/PROC1_PROCGRP.csv')
reader2 = csv.reader(snippet2)
i=0
for row in reader2:
    if i==0:
        i+=1
        continue
    i+=1    
    key = str(row[0])
    value = {'procgrp': str(row[1]), 'procgrp_description': str(row[2])}
    
    if key in cpt_procgrp:
        continue
    else:
        cpt_procgrp[key] = value
        
# Which procgrp description includes the word "other"?
procgrp_keyword_other = list()
for key in cpt_procgrp:
    if str.lower(cpt_procgrp[key]['procgrp_description']).find('other ') != -1:
        procgrp_keyword_other.append(key)

    
with open('/Users/yuchenli/Box Sync/Yuchen_project/'
          'MarketScan_update_Mark_Goodhart/Plot'
          '/PROC1_PROCGRP_keyword_other.csv', "w") as csvfile:
    fieldnames = ['cpt', "procgrp", "procgrp_description"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key in cpt_procgrp:
        try:
            if (key in procgrp_keyword_other):
                writer.writerow({'cpt': ("b:" + key), 
                                 "procgrp": cpt_procgrp[key]['procgrp'], 
                                 "procgrp_description": cpt_procgrp[key]['procgrp_description']})
        except:
            pass
        
#==============================================================================
# # Construct a subset of 100 proc1
# j=0
# subset = dict()
# for key, value in cpt_ccs.items():
#     j+=1
#     if (j<=100):
#         subset[j] = {'proc1':key,
#                      'procgrp': cpt_procgrp[key]['procgrp'],
#                      'procgrp_description': cpt_procgrp[key]['procgrp_description'],
#                      'ccs': cpt_ccs[key]['ccs'],
#                      'ccs_description':  cpt_ccs[key]['ccs_description']}
#     else:
#         pass
#     
# subset_pd = pd.DataFrame.from_dict(subset, orient = 'index')
# subset_pd.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
#                  'MarketScan_update_Mark_Goodhart/Plot/subset_100.csv',
#                  index = False)
#==============================================================================


# Read in CPT_range_CCS
cpt_range_ccs = dict()
ccs_description = dict()
snippet3 = open('/Users/yuchenli/Box Sync/Yuchen_project/'
               'MarketScan_update_Mark_Goodhart/Plot/CPT_range_CCS.csv')
reader3 = csv.reader(snippet3)
i=0
for row in reader3:
    if i==0:
        i+=1
        continue
    i+=1    
    key = str(row[0])
    value = str(row[1])
    value2 = str(row[2])
    
    if key in cpt_range_ccs:
        continue
    else:
        cpt_range_ccs[key] = value
    
    if value in ccs_description:
        continue
    else:
        ccs_description[value] = value2

# Map CPT to CCS
cpt_ccs = dict()
list_not_found = list()
i=1
for key in cpt_procgrp:
    i+=1
    print(i)
    found = False
    if (key == ""):
        continue
    else:
        for key2 in cpt_range_ccs:
            index_of_dash = key2.find('-')
            if (index_of_dash == -1):
                lower_bound = key2
                higher_bound = key2
            else:
                lower_bound = key2[0:index_of_dash]
                higher_bound = key2[index_of_dash+1:]
            
            if (key <= higher_bound and key >= lower_bound):
                cpt_ccs[key] = cpt_range_ccs[key2]
                found = found or True

    if (found == False):
        list_not_found.append(key)
        
import csv
with open('/Users/yuchenli/Box Sync/Yuchen_project/'
          'MarketScan_update_Mark_Goodhart/Plot/CPT_CCS.csv', "w") as csvfile:
    fieldnames = ['cpt', "ccs", "ccs_description"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for key, value in cpt_ccs.items():
        try:
            writer.writerow({'cpt': ("b:" + key), "ccs": value, 
                             "ccs_description": ccs_description[value]})
        except:
            pass
        
        
# Construct complete mapping where PROCGRP consist "other" as keyword
j=0
subset_other = dict()
subset_other_for_plot = dict()
for element in procgrp_keyword_other:
    j+=1
    try:
        subset_other[j] = {'proc1':element,
                     'procgrp': cpt_procgrp[element]['procgrp'],
                     'procgrp_description': cpt_procgrp[element]['procgrp_description'],
                     'ccs': cpt_ccs[element],
                     'ccs_description':  ccs_description[cpt_ccs[element]]}
        subset_other_for_plot[j] = {'proc1':element,
                     'procgrp': str(cpt_procgrp[element]['procgrp']) + ':' +
                     cpt_procgrp[element]['procgrp_description'],
                     'ccs': str(cpt_ccs[element]) + ':' +
                     ccs_description[cpt_ccs[element]]}
    except:
        pass
    
subset_other_pd = pd.DataFrame.from_dict(subset_other, orient = 'index')
subset_other_pd.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                 'MarketScan_update_Mark_Goodhart/Plot/subset_other.csv',
                 index = False)

subset_other_for_plot_pd = pd.DataFrame.from_dict(subset_other_for_plot, orient = 'index')
subset_other_for_plot_pd.to_csv('/Users/yuchenli/Box Sync/Yuchen_project/'
                 'MarketScan_update_Mark_Goodhart/Plot/subset_other_for_plot.csv',
                 index = False)
        