# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> test_nfp.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-15 14:48
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from datetime import datetime

from tools.geometry_functions import GeometryFunctions
from tools.plt_func import PltFunc


def try_nfp():
    # 计算NFP然后寻找最合适位置
    # 3 2 和 2 3
    # line = 2*2*2*4+3*2*2+1*2+1
    # line = 11
    # line = index
    # nfp = pd.read_csv("data/dagli_clus_nfp.csv")
    # polys = pd.read_csv("data/swim.csv")
    # for i in range(1):
    #     poly1 = json.loads(polys['polygon'][6])
    #     poly2 = json.loads(polys['polygon'][9])
    #     GeoFunc.normData(poly1,0.2)
    #     GeoFunc.normData(poly2,0.2)
    #     GeoFunc.slideToPoint(poly2, [288.3601990744186, 157.44678262857144])
    # GeoFunc.slidePoly(nfp, -200, -200)
    # PltFunc.addPolygon(poly1)
    # PltFunc.addPolygon(poly2)
    # PltFunc.addPolygonColor(poly)
    # GeoFunc.slideToPoint(poly2, [288.3601990744186, 157.44678262857144])
    # print(poly1)
    # print(poly2)
    # print(mapping(Polygon(poly1).intersection(Polygon(poly2))))
    # PltFunc.showPlt()
    # nfp = NFP(poly1,poly2,show=True,rectangle=False)
    # print(nfp.nfp)
    GeometryFunctions.normal_data(new_poly, 5)
    print(new_poly)
    # nfp = json.loads(nfp['nfp'][index])
    PltFunc.addPolygon(new_poly)
    # PltFunc.addPolygonColor(nfp)
    PltFunc.showPlt()  # GeoFunc.normData(poly2,20)
    pass


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
    try_nfp()
