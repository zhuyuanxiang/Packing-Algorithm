# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> reverse_function.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 11:02
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import csv
import json

import pandas as pd


class ReverseFunction(object):
    def __init__(self):
        new_poly = self.get_reverse(
                [[0.0, 0.0], [50.0, 150.0], [0.0, 250.0], [100.0, 200.0], [200.0, 250.0], [150.0, 100.0], [200.0, 0.0],
                 [200.0, -150.0], [100.0, -200.0], [0.0, -150.0]])
        print(new_poly)  # self.main()

    def main(self):
        fu = pd.read_csv("../record/c_blf.csv")
        _len = fu.shape[0]

        for i in range(_len):
            polys = json.loads(fu["polys"][i])
            clock_polys = []
            for poly in polys:
                new_poly = self.get_reverse(poly)
                clock_polys.append(new_poly)
            with open("../record/new_c_blf.csv", "a+") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows([[fu["index"][i],
                                   fu["descript"][i],
                                   fu["width"][i],
                                   fu["total_area"][i],
                                   fu["overlap"][i],
                                   fu["polys_orientation"][i],
                                   clock_polys]])

    def get_reverse(self, polys):
        # ToDo: 1. 改成 static 函数
        # ToDo: 2. 改成函数
        # ToDo: 3. 改成 for 循环
        i = len(polys) - 1
        new_polys = []
        while i >= 0:
            new_polys.append(polys[i])
            i = i - 1
        return new_polys
