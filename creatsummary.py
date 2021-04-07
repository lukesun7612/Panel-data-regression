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
output = 'D:/result/summary1.csv'
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



result = pd.DataFrame()
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
    df['speeddiff'] = df['Speed'].diff(1)/3.6
    df['timediff'] = time2float(df['GPS time'].astype('datetime64'))
    df['accelerated speed'] = df.apply(lambda x: x['speeddiff']/x['timediff'],axis=1)

    res = pd.DataFrame(df[usecol].mean()).T
    res.insert(0, column='Range', value=Range(df['Longitude'], df['Latitude']))
    res.insert(0, column='Brakes', value=avgBrake(df))
    res.insert(0, column='Fuel', value=diff_value(df['Integral fuel consumption']))
    res.insert(0, column='Kilo', value=diff_value(df['Integral kilometer']))
    res.insert(0, column='Harshdeceleration', value=hashdecelerate(df))
    res.insert(0, column='Harshacceleration', value=hashaccelerate(df))
    res.insert(0, column='Highspeedbrake', value=highspeedbrake(df))
    res.insert(0, column='Overspeed', value=overspeed(df))
    res.insert(0, column='ID',value=file[:11])

    if (res['Fuel'].sum()<10):
        pass
    else:
        result = pd.concat([result, res])
        count += 1
    print(count)
# result = result.loc[result['Kilo'].apply(lambda x: x > 5)].loc[result['Brakes'].apply(lambda y: y > 18)]
result = result.set_index('ID')
result = result.fillna(0)



if __name__ == '__main__':
    result.to_csv(output, mode='w')