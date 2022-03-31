# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> data_load.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 17:49
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import pandas as pd


def main(name):
    print(f'Hi, {name}')
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class DataLoad(object):
    def getLSTMData(self):
        x_train,y_train,x_val,y_val=[],[],[],[]
        _input=pd.read_csv("/Users/sean/Documents/Projects/Data/input.csv")
        _output=pd.read_csv("/Users/sean/Documents/Projects/Data/output_position.csv")

    def getPointerData(self):
        pass