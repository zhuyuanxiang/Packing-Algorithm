# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> bottom_left_fill.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-06 16:38
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from shapely.geometry import Polygon

import tools.packing_util
from tools.geometry_functions import GeometryFunctions
from tools.nfp import NFP
from tools.plt_func import PltFunc


class BottomLeftFill(object):
    """
    左底填充算法
    """
    def __init__(self, width, original_polygons, **kw):
        self.choose_nfp = False
        self.width = width
        self.length = 150000  # 代表长度
        self.contain_length = 3000
        self.polygons = original_polygons
        self.placeFirstPoly()
        self.NFPAssistant = None

        if 'NFPAssistant' in kw:
            self.NFPAssistant = kw["NFPAssistant"]
        # else:
        #     # 若未指定外部NFPasst则内部使用NFPasst开多进程
        #     self.NFPAssistant=packing.NFPAssistant(self.polygons,fast=True)
        self.vertical = False
        if 'vertical' in kw:
            self.vertical = kw['vertical']
        if 'rectangle' in kw:
            self.rectangle = True
        else:
            self.rectangle = False
        # for i in range(1,3):
        for i in range(1, len(self.polygons)):
            # print("##############################放置第",i+1,"个形状#################################")
            self.placePoly(i)  # self.showAll()

        self.get_length()  # self.showAll()

    def placeFirstPoly(self):
        poly = self.polygons[0]
        left_index, bottom_index, right_index, top_index = GeometryFunctions.check_bound(poly)  # 获得边界
        GeometryFunctions.slide_polygon(poly, -poly[left_index][0], -poly[bottom_index][1])  # 平移到左下角

    def placePoly(self, index):
        adjoin = self.polygons[index]
        # 是否垂直
        if self.vertical == True:
            ifr = tools.packing_util.PackingUtil.getInnerFitRectangle(self.polygons[index], self.width, self.length)
        else:
            ifr = tools.packing_util.PackingUtil.getInnerFitRectangle(self.polygons[index], self.length, self.width)
        differ_region = Polygon(ifr)

        for main_index in range(0, index):
            main = self.polygons[main_index]
            if self.NFPAssistant == None:
                nfp = NFP(main, adjoin, rectangle=self.rectangle).nfp
            else:
                nfp = self.NFPAssistant.get_direct_nfp(main, adjoin)
            nfp_poly = Polygon(nfp)
            try:
                differ_region = differ_region.difference(nfp_poly)
            except:
                print(differ_region)
                print(nfp_poly)
                print('NFP failure, polys and nfp are:')
                print([main, adjoin])
                print(nfp)
                self.show_all()
                self.show_polygons([main] + [adjoin] + [nfp])  # print('NFP loaded from: ',self.NFPAssistant.history_path)

        differ = GeometryFunctions.polygon_to_array(differ_region)
        differ_index = self.getBottomLeft(differ)
        refer_pt_index = GeometryFunctions.check_top(adjoin)
        GeometryFunctions.slideToPoint(self.polygons[index], adjoin[refer_pt_index], differ[differ_index])

    def getBottomLeft(self, poly):
        '''
        获得左底部点，优先左侧，有多个左侧选择下方
        '''
        bl = []  # bottom left的全部点
        _min = 999999
        # 选择最左侧的点
        for i, pt in enumerate(poly):
            pt_object = {"index": i, "x": pt[0], "y": pt[1]}
            if self.vertical == True:
                target = pt[1]
            else:
                target = pt[0]
            if target < _min:
                _min = target
                bl = [pt_object]
            elif target == _min:
                bl.append(pt_object)
        if len(bl) == 1:
            return bl[0]["index"]
        else:
            if self.vertical == True:
                target = "x"
            else:
                target = "y"
            _min = bl[0][target]
            one_pt = bl[0]
            for pt_index in range(1, len(bl)):
                if bl[pt_index][target] < _min:
                    one_pt = bl[pt_index]
                    _min = one_pt["y"]
            return one_pt["index"]

    def show_all(self):
        # for i in range(0,2):
        for i in range(0, len(self.polygons)):
            PltFunc.addPolygon(self.polygons[i])
        length = max(self.width, self.contain_length)
        # PltFunc.addLine([[self.width,0],[self.width,self.contain_height]],color="blue")
        PltFunc.showPlt(width=max(length, self.width), height=max(length, self.width), minus=100)

    def show_polygons(self, polys):
        for i in range(0, len(polys) - 1):
            PltFunc.addPolygon(polys[i])
        PltFunc.addPolygonColor(polys[len(polys) - 1])
        length = max(self.width, self.contain_length)
        PltFunc.showPlt(width=max(length, self.width), height=max(length, self.width), minus=200)

    def get_length(self):
        _max = 0
        for i in range(0, len(self.polygons)):
            if self.vertical:
                extreme_index = GeometryFunctions.check_top(self.polygons[i])
                extreme = self.polygons[i][extreme_index][1]
            else:
                extreme_index = GeometryFunctions.check_right(self.polygons[i])
                extreme = self.polygons[i][extreme_index][0]
            if extreme > _max:
                _max = extreme
        self.contain_length = _max
        # PltFunc.addLine([[0,self.contain_length],[self.width,self.contain_length]],color="blue")
        return _max


def main(name):
    print(f'Hi, {name}')
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
