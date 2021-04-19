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
            a = x.strftime("%H%m%s")
            timedelta.append(int(a[0:2]) * 3600 + int(a[2:4]) * 60 + int(a[4:]))
        else:
            timedelta.append(0)
    return pd.DataFrame(timedelta).diff(1)
def getAbj(se):
    '''
    得到相邻数据的里程差和时间差信息
    :param se: 里程信息，以Series的形式
    :return: 行程差信息列表和时间差信息列表
    '''
    mile_dist = se[1:].values - se[:-1].values
    mile_dist_time = (se[1:].index.values - se[:-1].index.values) / np.timedelta64(1, 's')
    mile_dist = pd.Series(mile_dist)
    mile_dist_time = pd.Series(mile_dist_time)
    return mile_dist, mile_dist_time
def split_journey(df, rotate=100, dura=5):
    """
    切分行程
    :param df: 输入信息，这里是dataframe的形式，信息包括'发动机转速'
    :param rotate: 转速阈值，超过阈值即认为在行程中
    :param dura: 转速不大于0超过dura即认为行程结束
    :return: 两部分：行程切分点列表和行程时间长度列表
    """

    df['GPS time'] = df['GPS time'].astype('datetime64')
    df = df.set_index('GPS time', drop=False)
    df['trip'] = np.where(rotate >= df['RPM'], 1, 0) # 将转速超过rotate的部分标记为行程内
    biaoji, mile_dist_time1 = getAbj(df['trip'])


    if df['trip'][0] == 1:
        biaoji[0] = 1
    else:
        biaoji[0] = -1

    if df['trip'][-1] == 1:
        biaoji[-1] = -1
    else:
        biaoji[-1] = 1

    biaoji = biaoji[biaoji != 0]
    biao_idx = biaoji.index  # 1到-1时run

    segment = []
    segment_time = []
    seg_start, seg_end = 0, 0
    assign = True

    for s, e in zip(biao_idx[:-1], biao_idx[1:]):
        start = 0 if s == 0 else s + 1
        duration = mile_dist_time1[start: e + 1].sum()
        assert s != e
        if biaoji[s] == 1 and assign:
            seg_start = start
            assign = False
        elif biaoji[s] == -1:
            if duration > dura * 60 and s != 0:
                seg_end = start
                seg_time = mile_dist_time1[seg_start: seg_end].sum() / 60
                segment.append((seg_start, seg_end))
                segment_time.append(seg_time)
                assign = True
    return segment, segment_time



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