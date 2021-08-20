"""
Dustin Ehling
08/18/2021

Approx 2hrs 30mins
"""

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.parsers import read_csv
import seaborn

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1500)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

#Read in data
data_women = pd.read_csv('C:/Users/Dustin/Downloads/MA Exercise_20180328-2/MA_Exer_PikesPeak_Females.txt',sep='\t')
data_men = pd.read_csv('C:/Users/Dustin/Downloads/MA Exercise_20180328-2/MA_Exer_PikesPeak_Males.txt',sep='\t')

#Fix /tab problem that puts character in gun_time column in womens data
data_women_temp = data_women['Gun Tim']
data_women[['Gun Tim']] = data_women_temp.str.split(" ",n=1,expand=False)

for i in data_women.index:
    if len(data_women['Gun Tim'][i]) > 1:
        char = data_women['Gun Tim'][i][0]
        value = data_women['Gun Tim'][i][1]

        #Write variables
        data_women['Hometown'][i] = data_women['Hometown'][i] + char
        data_women['Gun Tim'][i] = value
    else:
        data_women['Gun Tim'][i] = data_women['Gun Tim'][i][0]

#Add gender column to each dataframe
data_men['Gender'] = 'Men'
data_women['Gender'] = 'Women'

#Merge dataframes
data_all = data_men.append(data_women,ignore_index=True)

#Remove special characters (.,*,#)
data_all['Gun Tim'] = data_all['Gun Tim'].str.replace(r' ','')
data_all['Gun Tim'] = data_all['Gun Tim'].str.replace(r'*','')
data_all['Gun Tim'] = data_all['Gun Tim'].str.replace(r'**','')
data_all['Gun Tim'] = data_all['Gun Tim'].str.replace(r'#','')
data_all['Net Tim'] = data_all['Net Tim'].str.replace(r'#','')
data_all['Net Tim'] = data_all['Net Tim'].str.replace(r'*','')
data_all['Hometown'] = data_all['Hometown'].str.replace(r'.','')

#Standardize time formats
for i in data_all.index:
    if len(data_all['Gun Tim'][i]) < 6:
        data_all['Gun Tim'][i] = '00:' + data_all['Gun Tim'][i]
    else:
        data_all['Gun Tim'][i] = '0' + data_all['Gun Tim'][i]

for i in data_all.index:
    if len(data_all['Net Tim'][i]) < 6:
        data_all['Net Tim'][i] = '00:' + data_all['Net Tim'][i]
    else:
        data_all['Net Tim'][i] = '0' + data_all['Net Tim'][i]

for i in data_all.index:
    if len(data_all['Pace'][i]) < 5:
        data_all['Pace'][i] = '00:0' + data_all['Pace'][i]
    else:
        data_all['Pace'][i] = '00:' + data_all['Pace'][i]

#Convert hh:mm:ss to secs
for i in data_all.index:
    data_all['Gun Tim'][i] = pd.to_timedelta(data_all['Gun Tim'][i]).total_seconds()

for i in data_all.index:
    data_all['Net Tim'][i] = pd.to_timedelta(data_all['Net Tim'][i]).total_seconds()

for i in data_all.index:
    data_all['Pace'][i] = pd.to_timedelta(data_all['Pace'][i]).total_seconds()

data_all['Gun Tim'] = pd.to_numeric(data_all['Gun Tim'],errors='coerce')
data_all['Net Tim'] = pd.to_numeric(data_all['Net Tim'],errors='coerce')
data_all['Pace'] = pd.to_numeric(data_all['Pace'],errors='coerce')
print(data_all)

#Question One
data_all_mean = data_all.groupby('Gender').mean()
print(data_all_mean)
data_all_median = data_all.groupby('Gender').median()
print(data_all_median)
data_all_mode = data_all.groupby('Gender').agg(lambda x: pd.Series.mode(x).values[0])
print(data_all_mode)
boxplot = data_all.boxplot(column=['Net Tim'],by='Gender')

#Question Two
data_all['Time Differential (Gun vs Net)'] = data_all['Gun Tim'] - data_all['Net Tim']
seaborn.displot(data_all, x='Time Differential (Gun vs Net)', kind='kde', bw_adjust=1)
plt.show()

#Question Three
chris_doe = data_all[data_all['Name'] == 'Chris Doe']
top_10_in_div = data_all.loc[data_all['Gender'] == 'Men']
top_10_in_div = top_10_in_div.query('Ag >= 40 & Ag <= 49')

ten_quantile = top_10_in_div.quantile(.1)

chris_doe_diffential_from_top10 = chris_doe['Net Tim'] - ten_quantile['Net Tim']

diff_mins = chris_doe_diffential_from_top10 / 60
#Chris Doe would need to shave 8 mins 3 secs off his net time to break into the 90th percentile 
#in his division

seaborn.displot(top_10_in_div, x='Net Tim', kind='kde', bw_adjust=2)
plt.show()

#Question Four
data_all['Division'] = ''
print(data_all)
for i in data_all.index:
    if data_all['Ag'][i] in range(0,14):
        data_all['Division'][i] = '0-14'
    elif data_all['Ag'][i] in range(15,19):
        data_all['Division'][i] = '15-19'
    elif data_all['Ag'][i]  in range(20,29):
        data_all['Division'][i] = '20-29'
    elif data_all['Ag'][i]  in range(30,39):
        data_all['Division'][i] = '30-39'
    elif data_all['Ag'][i]  in range(40,49):
        data_all['Division'][i] = '40-49'
    elif data_all['Ag'][i]  in range(50,59):
        data_all['Division'][i] = '50-59'
    elif data_all['Ag'][i]  in range(60,69):
        data_all['Division'][i] = '60-69'
    elif data_all['Ag'][i]  in range(70,79):
        data_all['Division'][i] = '70-79'
    else: data_all['Division'][i] = '80-89'

seaborn.catplot(data=data_all,x='Gender', y='Net Tim',col='Division', kind='box',col_wrap=4,legend=True)
plt.show()
