#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: lukes
@project: JA3
@file: panel regression1.py
@time: 2020/4/15 11:09
"""
import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS,PooledOLS,RandomEffects,BetweenOLS,compare
import statsmodels.api as sm
import time
import datetime



date = ['2018-06-27','2018-06-28','2018-06-29','2018-06-30','2018-07-01','2018-07-02']
data = pd.read_csv('D:/result/paneldata0.csv')
data = data.rename(columns={'Selected speed(km/h)': 'Speed'})
data2 = data.loc[data['Date'].isin(date)]
data2.to_csv('D:/result/paneldata2.csv',index=0)
data1 = data.loc[~data['Date'].isin(date)]
data1.to_csv('D:/result/paneldata1.csv',index=0)



li = []
for i in data1['Date']:
    i = i.replace('-','')
    li.append(int(i))
data1['Date'] = li
# print(data1)


d = pd.Categorical(data1['Date'])
data1 = data1.set_index(['ID','Date'])
data1['Date'] = d
# print(data1)


exog_vars = ['Kilo','Brakes','Range','Speed', 'RPM', 'Engine fuel rate','Date']
a = ['Kilo','Brakes','Range','Speed', 'RPM', 'Engine fuel rate']
print(data1[a])
exog = sm.add_constant(data1[exog_vars])
exog1 = sm.add_constant(data1[a])
mod = PanelOLS(data1['Accelerator pedal position'], exog, entity_effects=True, time_effects=False)
mod1 = PooledOLS(data1['Accelerator pedal position'], exog1)
mod2 = RandomEffects(data1['Accelerator pedal position'],exog1)
mod3 = BetweenOLS(data1['Accelerator pedal position'], exog1)
res = mod.fit()
pooled_res = mod1.fit()
re_res = mod2.fit()
be_res = mod3.fit()
print(res)

print(compare({'Pooled':pooled_res,'RE':re_res,'BE':be_res}))





if __name__ == '__main__':
    pass