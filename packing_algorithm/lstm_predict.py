# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> lstm_predict.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 17:50
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import json
import random

import numpy as np
from shapely.geometry import Polygon
from shapely.geometry import Polygon
from shapely.geometry import Polygon
from tensorflow.python.keras.saving.save import load_model
from tensorflow.python.keras.saving.save import load_model

import pandas as pd
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import Dropout
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import LSTM

from history_show import HistoryShow
from history_show import HistoryShow
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.plt_func import PltFunc
from tools.plt_func import PltFunc
from tools.plt_func import PltFunc
from tools.plt_func import PltFunc
from tools.plt_func import PltFunc
from tools.plt_func import PltFunc


def main(name):
    print(f'Hi, {name}')
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class LSTMPredict(object):
    def __init__(self):
        pass

    def run(self):
        self.loadData()
        model = Sequential()
        model.add(LSTM(256,return_sequences=True,input_shape=(8,256)))
        model.add(Dropout(0.25))
        model.add(LSTM(256,return_sequences=True))
        model.add(Dropout(0.25))
        model.add(LSTM(256,return_sequences=True))
        model.add(Dropout(0.25))
        model.add(LSTM(256,return_sequences=True))
        model.add(Dropout(0.25))
        model.add(LSTM(256,return_sequences=True))
        model.add(Dropout(0.25))
        model.add(Dense(2, activation='tanh'))
        model.summary()
        model.compile(loss='mean_squared_error',optimizer='rmsprop', metrics=['accuracy'])

        history=model.fit(self.x_train, self.y_train, batch_size=256, epochs=1000, validation_data=(self.x_val, self.y_val))

        model.save("/Users/sean/Documents/Projects/Packing-Algorithm/model/absolute_lstm_num_3_layer_128_56_2_epochs_1000.h5")
        HistoryShow.showAccr(history)
        HistoryShow.showLoss(history)

    def loadData(self):
        # _input=pd.read_csv("/Users/sean/Documents/Projects/Data/input_seq.csv")
        # _output=pd.read_csv("/Users/sean/Documents/Projects/Data/output_relative_position.csv")
        # np_input=np.asarray([json.loads(_input["x_256"][i]) for i in range(0,5000)])
        # np_output=np.asarray([json.loads(_output["y"][i]) for i in range(0,5000)])

        file=pd.read_csv("/Users/sean/Documents/Projects/Data/8_lstm_test.csv")
        np_input=np.asarray([json.loads(file["x_256"][i]) for i in range(0,4700)])
        np_output=np.asarray([json.loads(file["y"][i]) for i in range(0,4700)])

        self.x_train=np_input[0:3700]
        self.y_train=np_output[0:3700]
        self.x_val=np_input[3700:4700]
        self.y_val=np_output[3700:4700]

    '''测试LSTM预测模型用 3.10'''
    def getPredictionRelative(self):
        model = load_model("/Users/sean/Documents/Projects/Packing-Algorithm/model/lstm_num_5_layer_128_56_2_epochs_70.h5")
        pre_train = pd.read_csv("/Users/sean/Documents/Projects/Data/pre_train.csv") # 读取形状
        _input = pd.read_csv("/Users/sean/Documents/Projects/Data/input_seq.csv") # 读取输入
        _output = pd.read_csv("/Users/sean/Documents/Projects/Data/output_relative_position.csv") # 读取输入


        # index=random.randint(4000,5000)
        index=4500

        polys=json.loads(pre_train["polys"][index]) # 形状
        X = np.array([json.loads(_input["x_256"][index])]) # 输入
        predicted_Y = model.predict(X, verbose=0)[0]*1500
        print(predicted_Y)
        Y=np.array(json.loads(_output["y"][index]))*1500
        print(Y)

        old_centroid=[0,0]
        for i,poly in enumerate(polys):
            # 获得初始的中心和预测的位置
            centroid_origin=GeometryFunctions.getPt(Polygon(poly).centroid)
            centroid_predicted=[Y[i][0]+old_centroid[0],Y[i][1]+old_centroid[1]]

            # 获得新的形状并更新
            new_poly=GeometryFunctions.get_slide(poly, centroid_predicted[0] - centroid_origin[0], centroid_predicted[1] - centroid_origin[1])
            old_centroid=GeometryFunctions.getPt(Polygon(new_poly).centroid)

            PltFunc.addPolygon(poly)
            PltFunc.addPolygonColor(new_poly)

        PltFunc.showPlt()

    def getPredictionAbsolute(self):
        model = load_model("/Users/sean/Documents/Projects/Packing-Algorithm/model/absolute_lstm_num_8_layer_128_56_2_epochs_200.h5")

        file= pd.read_csv("/Users/sean/Documents/Projects/Data/8_lstm_test.csv") # 读取输入

        index=random.randint(3700,4700)
        index=3000

        polys=json.loads(file["polys"][index]) # 形状
        X = np.array([json.loads(file["x_256"][index])]) # 输入
        predicted_Y = model.predict(X, verbose=0)[0]*4000

        for i,poly in enumerate(polys):
            centroid_origin=GeometryFunctions.getPt(Polygon(poly).centroid)
            PltFunc.addPolygon(poly)

            new_poly=GeometryFunctions.get_slide(poly, predicted_Y[i][0] - centroid_origin[0], predicted_Y[i][1] - centroid_origin[1])
            PltFunc.addPolygonColor(new_poly)

        PltFunc.showPlt()