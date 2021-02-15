#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: lukes
@project: JA3
@file: PCA.py
@time: 2020/6/2 11:10
"""
import pandas as pd
from sklearn.decomposition import PCA

usecol = ['Overspeed','Highspeedbrake','Harshacceleration','Harshdeceleration']
data = pd.read_csv('D:/result/paneldata0.csv',usecols=usecol)
pca = PCA(n_components='mle')
pca = pca.fit(data)
y = pca.transform(data)
print(pca.explained_variance_ratio_)
print(y)


if __name__ == '__main__':
    pass