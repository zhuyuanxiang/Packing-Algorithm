# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> packing_util.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 15:57
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions


def main(name):
    print(f'Hi, {name}')
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class PackingUtil(object):

    @staticmethod
    def getInnerFitRectangle(poly, x, y):
        left_index, bottom_index, right_index, top_index = GeometryFunctions.check_bound(poly)  # 获得边界
        new_poly = GeometryFunctions.get_slide(poly, -poly[left_index][0], -poly[bottom_index][1])  # 获得平移后的结果

        refer_pt = [new_poly[top_index][0], new_poly[top_index][1]]
        ifr_width = x - new_poly[right_index][0]
        ifr_height = y - new_poly[top_index][1]

        IFR = [refer_pt, [refer_pt[0] + ifr_width, refer_pt[1]], [refer_pt[0] + ifr_width, refer_pt[1] + ifr_height],
               [refer_pt[0], refer_pt[1] + ifr_height]]
        return IFR