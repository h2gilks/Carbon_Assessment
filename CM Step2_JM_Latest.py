# Step 2: Building the data frame to apportion all data across daily date periods

import pandas as pd
from datetime import datetime

excel1 = 'output.xlsx'

df3 = pd.read_excel(excel1)

## --> QUESTION FROM JEREMY --> how can we split out the data frame based upon vintage start and end date?

# First create a "period" column. Using a simple string concatenation of the start and end
# (separated by 3 spaces) in order to then easily perform a groupby
df3['Vintage Period'] = df3['Vintage Start'].astype(str) + '   ' + df3['Vintage End'].astype(str)

# Get the summed Quantity using groubpy in a single line
df_summed = df3.groupby(['Project Ref','Vintage Period']).sum()[['Quantity']]
# Simple string manipulation on the index (which was 'Vintage Period' in df3)
# gives us a time-delta, i.e. a difference between two dates
df_summed['Days'] = (
    df_summed.index.to_series()
    .apply(lambda item: item[1].split('   '))
    .apply(lambda item: (pd.to_datetime(item[1]) - pd.to_datetime(item[0])).days)
)

df_summed['Days'] = df_summed['Days'] + 1

# The daily average is then simply the summed average divided by (integer version of) the days timedelta
df_summed['Carbon Units'] = df_summed['Quantity'] / df_summed['Days']

# Now we're converting the single period entries into full time-ranges, essentially
# by iterating over the rows, and for each period-string converting it to a "date_range" index
# and concatenating all of these dataframes into the "expanded" version.
df_expanded = []
for (project_ref, period), data in df_summed.iterrows():
    start, end = period.split('   ')
    df_period = pd.DataFrame({
            'Project Ref': project_ref,
            'Period': period,
            'Summed Quantity': data.Quantity,
            'Days' : data.Days,
            'Carbon Units': data['Carbon Units'],
        },
        index=pd.date_range(start=start, end=end))
    df_expanded.append(df_period)
df_expanded = pd.concat(df_expanded)

# If needed, df_expanded can be pivoted (transposed) at this point
# as shown here:
# df_expanded_transposed = df_expanded.transpose()
# However I don't recommend this - the format of your data seems to make more sense in the un-pivoted form...

df_summed.to_csv('summed.csv',index=True)

df_expanded.to_csv('expanded_output.csv',index=True)


# REDUNDANT CODE


## attemps-------------------------------------------

# print(df3.dtypes)

# print(df3.columns)

# df3['Number of Days'] = df3['Vintage Start'] - df3['Vintage End'] + 1
# df3['Amount per day'] = df3['Amount per day'] / df3['Number of Days']


# df4 = pd.DataFrame(df3, columns = ['Project Ref', 'ID', 'Issuance Date', 'Quantity'])

# print(df4.resample('D', on='Issuance Date').Quantity.sum())

# df4.groupby('Issuance Date').sum()


# Attempt 1 ---------------------------------------------------------------

# print(df4.head())

# df4 = df4.drop_duplicates(subset = ['Project Ref'] )

# print(df4.head())

# df4 = pd.DataFrame(df3, columns = ['Project Ref', 'ID', 'Issuance Date', 'Vintage Start', 'Vintage End', 'Quantity'])
# mindate = df4['Vintage Start'].min()
# maxdate = df4['Vintage End'].max()
# number_of_days = (maxdate - mindate).days

# print(number_of_days)

# date1 = pd.Series(pd.date_range(mindate, periods = float(number_of_days), freq='D' ))
# date_df = pd.DataFrame(dict( Vintage_Date = date1))

# df4 = pd.DataFrame(df3, columns = ['Project Ref', 'ID', 'Issuance Date', 'Vintage Start', 'Vintage End', 'Quantity'])
# df4['date'] = pd.Series(pd.date_range(mindate, periods = number_of_days, freq='D' ))
# mask = (df4['date'] >= df4['Vintage End']) & (df4['date'] <= df4['Vintage Start'])
# print(df4.loc[mask])

# df = pd.DataFrame(np.random.random((200,3)))
# df['date'] = pd.date_range('2000-1-1', periods=200, freq='D')
# mask = (df['date'] > '2000-6-1') & (df['date'] <= '2000-6-10')
# print(df.loc[mask])
