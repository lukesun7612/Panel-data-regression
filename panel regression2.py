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
import statsmodels.api as sm
from sklearn.preprocessing import OneHotEncoder

date = ['2018-07-03', '2018-07-04', '2018-07-05', '2018-07-06', '2018-07-07', '2018-07-08']
# read panel data set
data = pd.read_csv('D:/result/summary1.csv')
idate = OneHotEncoder(categories='auto').fit_transform(data['Date'].values.reshape(-1,1)).toarray()
idate = pd.DataFrame(idate,columns=date,index=data.index)
iid = OneHotEncoder(categories='auto').fit_transform(data['ID'].values.reshape(-1,1)).toarray()
iid = pd.DataFrame(iid,columns=list(range(1,183)))


data = pd.concat([data,idate,iid],1)
data.Kilo[data['Kilo'] == 0] = 0.01
print(data)


exog_vars = ['Brakes', 'Range', 'Speed', 'RPM', 'Accelerator pedal position', 'Engine fuel rate']
exog = sm.add_constant(data[exog_vars+date[1:]+list(range(2,183))])
Poi_mod1 = sm.Poisson(data['Overspeed'], exog, exposure=np.asarray(data['Kilo']))
Poi_mod2 = sm.Poisson(data['Highspeedbrake'], exog, exposure=np.asarray(data['Kilo']))
Poi_mod3 = sm.Poisson(data['Harshacceleration'], exog, exposure=np.asarray(data['Kilo']))
Poi_mod4 = sm.Poisson(data['Harshdeceleration'], exog, exposure=np.asarray(data['Kilo']))
res1 = Poi_mod1.fit()
res2 = Poi_mod2.fit()
res3 = Poi_mod3.fit()
res4 = Poi_mod4.fit()

print(res1.summary())
# print(compare({'Overspeed':res1,'Highspeedbrake':res2,'Harshacceleration':res3,'Harshdeceleration':res4}))





if __name__ == '__main__':
    pass