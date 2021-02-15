#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: lukes
@project: data description
@file: creatsummary.py
@time: 2020/4/9 15:26
"""

import pandas as pd
import numpy as np
import os
import time
pd.options.display.max_columns = None
pd.options.display.max_rows = None
input = 'D:/result/dataset1'
output = 'D:/result/paneldata01.csv'
usecol = ['Speed', 'RPM', 'Accelerator pedal position', 'Engine fuel rate']
def fun(x):
    if x > 1:
        return 0
    else:
        return x

def diff_value(df_column_name):
    a = np.array(df_column_name).tolist()
    if len(a) == 0:
        return 0
    else:
        return a[-1] - a[0]

def Range(longitude,latitude):
    a = 10**(-6)*np.array([longitude.min(), latitude.min()])
    b = 10**(-6)*np.array([longitude.max(), latitude.max()])
    dist = np.linalg.norm(b - a)
    return dist

def avgBrake(dataframe):
    if dataframe['Brake times'].sum() > 3*diff_value(dataframe['Integral kilometer']):
        n = np.mean([dataframe['Brake switch'].sum(), dataframe['Brake times'].sum()])
    else:
        n = dataframe['Brake times'].sum()
    return n

def time_c(timeTemp):

    tupTime = time.localtime(timeTemp)
    stadardTime = time.strftime("%m%d", tupTime)
    return stadardTime

def highspeedbrake(df):
    df['highspeedbrake'] = np.where((df['Speed']>90)&((df['Brake times']>0)|(df['Brake switch']>0)),1,0)
    return df['highspeedbrake'].sum()
def hashaccelerate(df, up=0.556):
    df['hashaccelerate'] = np.where(df['accelerated speed']>up,1,0)
    return df['hashaccelerate'].sum()
def hashdecelerate(df, low=-0.556):
    df['hashdecelerate'] = np.where(df['accelerated speed']<low,1,0)
    return df['hashdecelerate'].sum()
def overspeed(df):
    df['overspeed'] = np.where(df['Speed']>100,1,0)
    return df['overspeed'].sum()
def time2float(b):
    timedelta = []
    for x in b:
        if x:
            a = x.strftime("%H%M%S")
            timedelta.append(int(a[0:2]) * 3600 + int(a[2:4]) * 60 + int(a[4:]))

        else:
            timedelta.append(0)
    # timestr = [x.strftime("%h%m%s") for x in b]
    return pd.DataFrame(timedelta).diff(1)

def abnormal_box(se, level=3):
	'''
	箱线图法获取速度阈值
	:param se:
	:param level:
	:return:
	'''
	# Q2 = np.median(se)  # 中位数
	Q1 = se.quantile(0.25)
	Q3 = se.quantile(0.75)
	IQR = Q3 - Q1
	low, upp = Q1 - level * IQR, Q3 + level * IQR
	return low, upp

results = pd.DataFrame()
count = 0
LOW, UP = [], []
for i, file in enumerate(os.listdir(input)):
    print(i, file)

    filepath = os.path.join(input, file)
    df = pd.read_csv(filepath, header=0)
    df = df.drop_duplicates(['GPS time'])
    df = df.rename(columns={'Selected speed(km/h)': 'Speed'})
    df = df.loc[df['Longitude'].apply(lambda x: x > 0)].loc[df['Latitude'].apply(lambda y: y > 0)]
    df['Brake switch'] = df['Brake switch'].apply(lambda x: fun(x))
    # df['journey'] = np.where(df['RPM'] >= 100, 1, 0)
    # df = df.loc[df['journey'] == 1]
    # df['highspeedbrake'] = np.where((df['Selected speed(km/h)'] > 90) & ((df['Brake times'] > 0)|(df['Brake switch'] > 0)),
    #                                 1, 0)
    # print(df['highspeedbrake'].sum())


    df['speeddiff'] = df['Speed'].diff(1)/3.6
    df['timediff'] = time2float(df['GPS time'].astype('datetime64'))
    df['accelerated speed'] = df.apply(lambda x: x['speeddiff']/x['timediff'],axis=1)
    # low, upp = abnormal_box(df['accelerated speed'])
    # LOW.append(low)
    # UP.append(upp)
    for j in range(len(df)):
        df.iloc[j,1] = df.iloc[j,1][0:10]
        # print(df.iloc[j,1])
    # print(df.loc[df['GPS time'] == '07-08',:])
    date = pd.unique(df['GPS time']).tolist()
    result = pd.DataFrame()
    for k in date:
        df1 = df.loc[df['GPS time'].str.contains(k)]
        res = pd.DataFrame(df1[usecol].mean()).T
        res.insert(0, column='Range', value=Range(df1['Longitude'], df1['Latitude']))
        res.insert(0, column='Brakes', value=avgBrake(df1))
        res.insert(0, column='Fuel', value=diff_value(df1['Integral fuel consumption']))
        res.insert(0, column='Kilo', value=diff_value(df1['Integral kilometer']))
        res.insert(0, column='Harshdeceleration', value=hashdecelerate(df1))
        res.insert(0, column='Harshacceleration', value=hashaccelerate(df1))
        res.insert(0, column='Highspeedbrake', value=highspeedbrake(df1))
        res.insert(0, column='Overspeed', value=overspeed(df1))
        res.insert(0, column='Date',value=k)
        res.insert(0, column='ID',value=file[:11])
        result = pd.concat([result, res])
    if (result['Fuel'].sum() < 10) | (len(result) < 6):
        pass
    else:
        results = pd.concat([results, result])
        count += 1
    print(count)
# results = results.loc[results['Kilo difference'].apply(lambda x: x > 5)].loc[results['Brakes'].apply(lambda y: y > 18)]
results = results.set_index('ID')
results = results.fillna(0)
# print(np.mean(LOW))
# print(np.mean(UP))


if __name__ == '__main__':
    results.to_csv(output, mode='w')