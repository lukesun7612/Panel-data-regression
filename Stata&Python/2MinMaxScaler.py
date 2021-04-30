#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: lukes
@project: JA3
@file: MinMaxScaler.py
@time: 2020/12/31 18:28
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from scipy.stats.mstats import winsorize
import matplotlib.pyplot as plt

# set input path and output path
inputpath = './coefresult.csv'
outputpath = './scoreresult.xlsx'
usecol = ['overspeed','highspeedbrake','harshacceleration','harshdeceleration']
# Read the data and organize it
data = pd.read_csv(inputpath, skiprows=2, index_col=0)
data.columns = usecol
data.index.names = ['id']
data = data.drop(data.tail(1).index)
data.loc['id1'] = [0, 0, 0, 0]
data = data.iloc[np.arange(-1, len(data)-1)]
# winsorize the data with Package<winsorize>
data_w = winsorize(data, limits=[0.01, 0.01], axis=0, inplace=True)
# Normalize the winsorized data, map into [0,5]
scaler1 = MinMaxScaler(feature_range=(0,5))
result1 = scaler1.fit_transform(data_w)
df = pd.DataFrame(result1, index=data.index, columns=usecol)
print(df)

# plot risk level figure
# Add scatters
fig, ax = plt.subplots()
plot = ax.scatter(np.ones(182)+0.001*np.arange(1,183), df['overspeed'].values, c=df['overspeed'].values, cmap='rainbow', alpha=0.5)
ax.scatter(2*np.ones(182)+0.001*np.arange(1,183), df['highspeedbrake'].values, c=df['highspeedbrake'].values, cmap='rainbow', alpha=0.5)
ax.scatter(3*np.ones(182)+0.001*np.arange(1,183), df['harshacceleration'].values, c =df['harshacceleration'].values, cmap='rainbow', alpha=0.5)
ax.scatter(4*np.ones(182)+0.001*np.arange(1,183), df['harshdeceleration'].values, c=df['harshdeceleration'].values, cmap='rainbow', alpha=0.5)
# Adjust coordinate axis
plt.xlim(0.2,5)
plt.ylim(-0.05,5.05)
plt.xticks([1.091,2.091,3.091,4.091],["Over-speed","High-speed-brake","Harsh-acceleration","Harsh-deceleration"])
plt.yticks([1,2,3,4,5.05],["level 1","level 2","level 3","level 4","level 5"])
plt.xlabel('Near-miss Event')
plt.ylabel('Driving Risk Level')
plt.grid(axis='y', ls='--')
# Add annotate
plt.scatter(1.125,df.overspeed[124], edgecolors='k', c='')
plt.annotate("id125(score=%s)"%df.overspeed[124].round(3), xy=(1.125, df.overspeed[124]), xytext=(1.3,4.1), arrowprops=dict(arrowstyle='->', connectionstyle="arc3"), bbox=dict(boxstyle='Round,pad=0.5', fc='white', lw=1, ec='k', alpha=0.5))
plt.scatter(2.125,df.highspeedbrake[124], edgecolors='k', c='')
plt.annotate("id125(score=%s)"%df.highspeedbrake[124].round(3), xy=(2.125, df.highspeedbrake[124]), xytext=(2.3,1.2), arrowprops=dict(arrowstyle='->', connectionstyle="arc3"), bbox=dict(boxstyle='Round,pad=0.5', fc='white', lw=1, ec='k', alpha=0.5))
plt.scatter(3.125,df.harshacceleration[124], edgecolors='k', c='')
plt.annotate("id125(score=%s)"%df.harshacceleration[124].round(3), xy=(3.125, df.harshacceleration[124]), xytext=(3.3,2.8), arrowprops=dict(arrowstyle='->', connectionstyle="arc3"), bbox=dict(boxstyle='Round,pad=0.5', fc='white', lw=1, ec='k', alpha=0.5))
plt.scatter(4.125,df.harshdeceleration[124], edgecolors='k', c='')
plt.annotate("id125(score=%s)"%df.harshdeceleration[124].round(3), xy=(4.125, df.harshdeceleration[124]), xytext=(4.3,3.2), arrowprops=dict(arrowstyle='->', connectionstyle="arc3"), bbox=dict(boxstyle='Round,pad=0.5', fc='white', lw=1, ec='k', alpha=0.5))
# Add colorbar, make sure to specify tick locations to match desired ticklabels
cbar = fig.colorbar(plot, ticks=[-1, 0, 1])
cbar.set_ticks([0,1.3,2.5,3.8,5])
cbar.set_ticklabels(["Excellent","Good","Medium","Bad","Terrible"])
plt.show()

if __name__ == '__main__':
    df.to_excel(outputpath)
