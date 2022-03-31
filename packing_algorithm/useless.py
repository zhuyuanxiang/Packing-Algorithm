# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> useless.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-06 17:08
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from tools.plt_func import PltFunc
from tools.plt_func import PltFunc
from tools.plt_func import PltFunc


def main(name):
    print(f'Hi, {name}')
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


def show_polygons(polygons, coloring=None):
    """
    展示全部形状以及边框
    """
    for polygon in polygons:
        if coloring is not None and polygon == coloring:
            PltFunc.addPolygonColor(polygon, "red")  # 红色突出显示
        else:
            PltFunc.addPolygon(polygon)
    # PltFunc.addPolygonColor([[0,0], [1500,0], [self.cur_length,self.width], [0,self.width]])
    PltFunc.showPlt(width=1500, height=1500)