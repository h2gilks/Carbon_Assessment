#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 08:21:40 2021

@author: henry
"""

import pandas as pd

# Step 1: make a master project list that has all the required data - it has the project type and name and info etc

# merge this file with the daily file.

# or even do the join in tableau

# Two files
# Issuances
# VIntages

excel1 = 'output.xlsx'
excel4 = 'Methodologies.xlsx'
excel5 = 'expanded_output.csv'


# Create methodology file -------------------------------------------------------------

df2 = pd.read_excel (excel4, sheet_name='Full Methodology List')
df2 = pd.DataFrame(df2, columns = ['Source', 'Methodology', 'Methodology Name'])
# headers in this file - Source 	Methodology	Methodology Name

df3 = pd.read_excel (excel4, sheet_name='ProjectTypeAligned')
# two headers in the file - Project Type	Project Type Aligned

#Issuance Output -------------------------------------------------------------

df1 = pd.read_excel(excel1)
df5 = pd.DataFrame(df1, columns = ['Project Ref', 'Project Type', 'Methodology'])

df1_drop = df5.drop_duplicates(subset= ['Project Ref'], keep='first', inplace=False, ignore_index=False)
# Returns full list of projects

df1_merge = df1_drop.merge(df2, on='Methodology', how='left')
# joins methodology list onto list of projects

df1_merge = df1_merge.merge(df3, on='Project Type', how='left')

df1Trim = pd.DataFrame(df1, columns = ['Data Source	','Project Ref','Issuance Date','Vintage Start','Vintage End','Vintage Year','ID','Project Name','Country','Total Vintage Quantity','Quantity','Serial Number','Additional Certifications','Project Developer','Retirement/Cancellation Date','Retirement Details','Retirement Beneficiary','Retirement Reason'])

OutputwithPRef = df1Trim.merge(df1_merge, on = 'Project Ref', how = 'left')



# Vintage Output -------------------------------------------------------------

df4 = pd.read_csv(excel5)
df6 = pd.DataFrame(df1, columns = ['Data Source', 'Project Ref', 'Project Name', 'Country', 'Project Type', 'Methodology'])

df6_drop = df6.drop_duplicates(subset= ['Project Ref'], keep='first', inplace=False, ignore_index=False)
# Returns full list of projects

df6_merge = df6_drop.merge(df2, on='Methodology', how='left')
# joins methodology list onto list of projects

df6_merge = df6_merge.merge(df3, on='Project Type', how='left')


ExpandedWithPRef = df4.merge(df6_merge, on = 'Project Ref', how = 'left')



OutputwithPRef.to_csv("Output_With_PRef.csv", index=False)
ExpandedWithPRef.to_csv("Expanded_With_PRef.csv", index=False)