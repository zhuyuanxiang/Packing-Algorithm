# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> new_nfp_assistant.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-06 16:39
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import json

import pandas as pd
from shapely.geometry import Polygon

from tools.geometry_assitant import GeometryAssistant


class NewNfpAssistant(object):
    """
    处理排样具体数据集加入，输入是形状，不考虑旋转！！
    """

    def __init__(self, dataset_name, allowed_rotation):
        self.dataset_name = dataset_name
        self.allowed_rotation = allowed_rotation
        self.all_polygons = pd.read_csv("../data/" + self.dataset_name + "_orientation.csv")
        self.all_nfps = pd.read_csv("../data/" + self.dataset_name + "_nfp.csv")
        pass

    def get_direct_nfp(self, main, adjoin):
        # 分别为固定i/移动j的形状
        i, j = self.judge_type(main), self.judge_type(adjoin)
        # row = self.all_polygons.shape[0] * self.allowed_rotation * self.allowed_rotation * i + self.allowed_rotation * self.allowed_rotation * j + self.allowed_rotation * 0 + 1 * 0
        row = self.allowed_rotation * self.allowed_rotation * (self.all_polygons.shape[0] * i + j)
        bottom_point = GeometryAssistant.get_bottom_point(main)
        nfp = GeometryAssistant.getSlide(json.loads(self.all_nfps["nfp"][row]), bottom_point[0], bottom_point[1])
        # showPolys([main,adjoin,nfp],coloring=nfp)
        return nfp

    def judge_type(self, poly):
        # 判断形状类别，用于计算具体的NFP
        area = int(Polygon(poly).area)
        for i in range(self.all_polygons.shape[0]):
            new_poly = json.loads(self.all_polygons["o_0"][i])
            test_poly_area = Polygon(new_poly).area
            if abs(test_poly_area - area) < 2 and abs(
                    (new_poly[1][0] - new_poly[0][0]) - (poly[1][0] - poly[0][0])) < 2:
                return i
        print("NFP错误")
        pass

    pass


def main(name):
    print(f'Hi, {name}')
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
