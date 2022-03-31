# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> plt_func.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 11:04
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
ToDo: 把这个类拆成函数
==================================================
"""
import time

from matplotlib import pyplot as plt


class PltFunc(object):
    def addPolygon(poly):
        for i in range(0, len(poly)):
            if i == len(poly) - 1:
                PltFunc.addLine([poly[i], poly[0]])
            else:
                PltFunc.addLine([poly[i], poly[i + 1]])

    def addPolygonColor(poly, color="blue"):
        for i in range(0, len(poly)):
            if i == len(poly) - 1:
                PltFunc.addLine([poly[i], poly[0]], color=color)
            else:
                PltFunc.addLine([poly[i], poly[i + 1]], color=color)

    def addLine(line, **kw):
        if len(kw) == 0:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color="black", linewidth=0.5)
        else:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=kw["color"], linewidth=0.5)

    def addLineColor(line):
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color="blue", linewidth=0.5)

    def showPlt(**kw):
        if len(kw) > 0:
            if "minus" in kw:
                plt.axhline(y=0, c="blue")
                plt.axvline(x=0, c="blue")
                plt.axis([-kw["minus"], kw["width"], -kw["minus"], kw["height"]])

            else:
                plt.axis([0, kw["width"], 0, kw["height"]])
        else:
            plt.axis(
                [0, 1000, 0, 1000])  # plt.axis([-1000,2000,-979400.4498015114,20000])  # plt.axis([-500,1000,0,1500])
        plt.show()
        plt.clf()

    def showPolys(polys, saving=False, coloring=None):
        """
        展示全部形状以及边框
        """
        for poly in polys:
            if coloring is not None and (poly == coloring or poly in coloring):
                PltFunc.addPolygonColor(poly, "red")  # 红色突出显示
            else:
                PltFunc.addPolygon(poly)
        if saving:
            PltFunc.saveFig('figs/LP_Search/{}.png'.format(str(time.strftime("%H_%M_%S", time.localtime()))))
        else:
            PltFunc.showPlt(width=1500, height=1500)

    def saveFig(path):
        plt.savefig(path)
        plt.cla()
