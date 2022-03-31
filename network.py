# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> network.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 14:41
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
网络训练情况
1. 标准化：形状全部转化为向量表示，收缩将1000作为收缩参数，后续获得其最大值，宽度为其
2. 宽度：暂时不考虑宽度输入，默认为1500，后续"宽度/10000"作为第一个输入参数
3. 输出：分别为重心的x/y坐标
4. 旋转角度：后续增加旋转角度的处理
5. 利用率：可以预测利用率的范围
6. 可行化：(a) 采用Minimize Overlap，形状全部向下平移 (b) 采用最低高度进行序列生成
==================================================
"""
from packing_algorithm.lstm_predict import LSTMPredict

if __name__ == '__main__':
    lstm = LSTMPredict()
    lstm.run()
    # lstm.getPrediction()
    # lstm.getPredictionAbsolute()
    pass
