# Step 1: Taking all the registry files - let's get them into a format that we need for aggregating

import pandas as pd

from datetime import datetime

excel1 = 'vcus.xlsx'
excel2 = 'GSF Registry Credits Export.csv'
excel3 = 'Collated New.xlsx'
excel4 = 'Methodologies.xlsx'

# File2Match = pd.read_excel (excel3, sheet_name='Collated')

df1 = pd.read_excel (excel1, sheet_name='Results')
df2 = pd.read_csv (excel2)
df3 = pd.read_excel (excel4, sheet_name='Full Methodology List')
df4 = pd.read_excel (excel4, sheet_name='ProjectTypeAligned')
# print (df1.columns)
# print('\n')
# print (df2.columns)
# print('\n')
# print (File2Match.columns)
# print(df2.dtypes)


##---------------------------------------------------------------------------

# dataframe 1 rename

df1.rename(columns={'Name':'Project Name'}, inplace=True)
df1.rename(columns={'Credits Quantity Issued':'Quantity'}, inplace=True)
 
# dataframe 2 rename

df2.rename(columns={'GSID':'ID'}, inplace=True)
df2.rename(columns={'Vintage':'Vintage Year'}, inplace=True)
df2.rename(columns={'Note':'Retirement Details'}, inplace=True)
df2.rename(columns={'Retirement Date':'Retirement/Cancellation Date'}, inplace=True)

# Add reference column

df1['Project Developer'] =  "Not included in VCS data"
df2['Additional Certifications'] =  "Not relevant for Gold Standard"
df1['Project Ref'] =  "VCS_" + df1['ID'].astype(str)
df2['Project Ref'] =  "GS_" + df2['ID'].astype(str)
df1['Data Source'] =  "VCS"
df2['Data Source'] =  "Gold Standard"
df2['Product Type'] = df2['Product Type'] + "_Gold Standard"
df2.rename(columns={'Product Type':'Methodology'}, inplace=True)

df1['Vintage Year'] = pd.DatetimeIndex(df1['Vintage End']).year

## QUESTION FOR JEREMY - how can I get the start and end of the year from 'Vintage Year'???
## This then needs to feed into the next stage of the process

df2['Vintage Start'] = pd.to_datetime(df2["Vintage Year"].astype(str)+ "/01/01")
df2['Vintage End'] = pd.to_datetime(df2["Vintage Year"].astype(str)+ "/12/31")


##---------------------------------------------------------------------------
# New columns to align project type naming
## QUESTION FOR JEREMY - can I do the below in a quicker way?

# df1.loc[ df1['Project Type'].str.contains(';') , 'Project Type Aligned' ] = 'Multiple Categories'
# df1.loc[ (df1['Project Type'] == 'Energy demand') & (~df1['Project Type'].str.contains(';')) , 'Project Type Aligned' ] = 'Energy Demand'
# df1.loc[ (df1['Project Type'] =='Chemical industry') & (~df1['Project Type'].str.contains(';')), 'Project Type Aligned' ] = 'Chemical industry'
# df1.loc[ (df1['Project Type'] =='Energy distribution') & (~df1['Project Type'].str.contains(';') ), 'Project Type Aligned' ] = 'Energy distribution'
# df1.loc[ (df1['Project Type'] =='Energy industries (renewable/non-renewable sources)') & (~df1['Project Type'].str.contains(';') ), 'Project Type Aligned' ] = 'Energy (renewable/non-renewable sources)'
# df1.loc[ (df1['Project Type'] =='Manufacturing industries') & (~df1['Project Type'].str.contains(';') ), 'Project Type Aligned' ] = 'Manufacturing industries'
# df1.loc[ (df1['Project Type'] =='Metal production') & (~df1['Project Type'].str.contains(';') ), 'Project Type Aligned' ] = 'Metal production'
# df1.loc[ (df1['Project Type'] =='Mining/mineral production') & (~df1['Project Type'].str.contains(';') ), 'Project Type Aligned' ] = 'Mining/mineral production'
# df1.loc[ (df1['Project Type'] =='Transport') & (~df1['Project Type'].str.contains(';') ), 'Project Type Aligned' ] = 'Transport'
# df1.loc[ (df1['Project Type'] =='Waste handling and disposal') & (~df1['Project Type'].str.contains(';') ), 'Project Type Aligned' ] = 'Waste handling and disposal'
# df1.loc[ (df1['Project Type'] == 'Agriculture Forestry and Other Land Use') & (~df1['Project Type'].str.contains(';')) , 'Project Type Aligned' ] = 'Agriculture, Forestry, Land Use'
# df1.loc[ (df1['Project Type'] == 'Energy industries (renewable/non-renewable sources)') & (~df1['Project Type'].str.contains(';')) , 'Project Type Aligned' ] = 'Energy (renewable/non-renewable sources)'
# df1.loc[ (df1['Project Type'] == 'Fugitive emissions from fuels (solid, oil and gas)') & (~df1['Project Type'].str.contains(';')) , 'Project Type Aligned' ] = 'Fugitive emissions'
# df1.loc[ (df1['Project Type'] == 'Fugitive emissions from production and consumption of halocarbons and sulphur hexafluoride') & (~df1['Project Type'].str.contains(';')) , 'Project Type Aligned' ] = 'Fugitive emissions'
# df1.loc[ (df1['Project Type'] == 'Livestock, enteric fermentation, and manure management') & (~df1['Project Type'].str.contains(';')) , 'Project Type Aligned' ] = 'Livestock and manure management'




##---------------------------------------------------------------------------
# Join code

values1 = df1
values2 = df2

dataframes = [values1, values2]

join = pd.concat(dataframes, axis = 0, sort = False)

# print(join.columns)

join.to_excel("output.xlsx", index=False, columns = ['Data Source', 'Project Ref', 'Issuance Date', 'Vintage Start', 'Vintage End', 'Vintage Year', 'ID', 'Project Name', 'Country', 'Project Type', 'Methodology', 'Total Vintage Quantity', 'Quantity', 'Serial Number', 'Additional Certifications', 'Project Developer', 'Retirement/Cancellation Date', 'Retirement Details', 'Retirement Beneficiary', 'Retirement Reason'])

##---------------------------------------------------------------------------
# Merge code


# join = join.merge(df3, on='Methodology', how='left')


# REDUNDANT CODE

##---------------------------------------------------------------------------
## Useful code references

# print(df1.dtypes)

# df1["Issuance Date"] = pd.to_datetime(df1["Issuance Date"])

# df1.head()

# print(df1['Name'])

# print(df1.head(4))

# print(df1.iloc[1])

# print(df1.loc[df['Name'] == "Parbati Hydroelectric Project Stage III"])

# df1.to_excel('modified_vcus.xlsx',index=False)

# print(df1.loc[df['Name'].str.contains('Katingan')  ])

# df1.loc[df["Project Type"] == "A", "Project Type"] = "B"
