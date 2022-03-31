# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> topos.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-06 16:39
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from shapely.geometry import mapping
from shapely.geometry import Polygon
from shapely.geometry import Polygon

import tools.nfp_assistant
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.geometry_functions import GeometryFunctions
from tools.plt_func import PltFunc
from tools.plt_func import PltFunc


def main(name):
    print(f'Hi, {name}')
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class TOPOS(object):
    '''
    TOPOS启发式算法：将形状一个个放入，动态移动整体的位置，该算法参考Bennell的TOPOS Revised
    问题：中线情况、好像有一些bug
    '''

    def __init__(self, original_polys, width):
        self.polys = original_polys
        self.cur_polys = []
        self.width = width
        self.NFPAssistant = tools.nfp_assistant.NFPAssistant(self.polys, store_nfp=False, get_all_nfp=True, load_history=True)

        self.run()

    def run(self):
        self.cur_polys.append(GeometryFunctions.get_slide(self.polys[0], 1000, 1000))  # 加入第一个形状
        self.border_left, self.border_right, self.border_bottom, self.border_top = 0, 0, 0, 0  # 初始化包络长方形
        self.border_height, self.border_width = 0, 0
        for i in range(1, len(self.polys)):
            # 更新所有的边界情况
            self.updateBound()

            # 计算NFP的合并情况
            feasible_border = Polygon(self.cur_polys[0])
            for fixed_poly in self.cur_polys:
                nfp = self.NFPAssistant.getDirectNFP(fixed_poly, self.polys[i])
                feasible_border = feasible_border.union(Polygon(nfp))

            # 获得所有可行的点
            feasible_point = self.chooseFeasiblePoint(feasible_border)

            # 获得形状的左右侧宽度
            poly_left_pt, poly_bottom_pt, poly_right_pt, poly_top_pt = GeometryFunctions.check_bound_point(self.polys[i])
            poly_left_width, poly_right_width = poly_top_pt[0] - poly_left_pt[0], poly_right_pt[0] - poly_top_pt[0]

            # 逐一遍历NFP上的点，选择可行且宽度变化最小的位置
            min_change = 999999999999
            target_position = []
            for pt in feasible_point:
                change = min_change
                if pt[0] - poly_left_width >= self.border_left and pt[0] + poly_right_width <= self.border_right:
                    # 形状没有超出边界，此时min_change为负
                    change = min(self.border_left - pt[0], self.border_left - pt[0])
                elif min_change > 0:
                    # 形状超出了左侧或右侧边界，若变化大于0，则需要选择左右侧变化更大的值
                    change = max(self.border_left - pt[0] + poly_left_width,
                                 pt[0] + poly_right_width - self.border_right)
                else:
                    # 有超出且min_change<=0的时候不需要改变
                    pass

                if change < min_change:
                    min_change = change
                    target_position = pt

            # 平移到最终的位置
            reference_point = self.polys[i][GeometryFunctions.check_top(self.polys[i])]
            self.cur_polys.append(GeometryFunctions.get_slide(self.polys[i], target_position[0] - reference_point[0],
                                                              target_position[1] - reference_point[1]))

        self.slideToBottomLeft()
        self.showResult()

    def updateBound(self):
        '''
        更新包络长方形
        '''
        border_left, border_bottom, border_right, border_top = GeometryFunctions.check_bound_value(self.cur_polys[-1])
        if border_left < self.border_left:
            self.border_left = border_left
        if border_bottom < self.border_bottom:
            self.border_bottom = border_bottom
        if border_right > self.border_right:
            self.border_right = border_right
        if border_top > self.border_top:
            self.border_top = border_top
        self.border_height = self.border_top - self.border_bottom
        self.border_width = self.border_right - self.border_left

    def chooseFeasiblePoint(self, border):
        '''选择可行的点'''
        res = mapping(border)
        _arr = []
        if res["type"] == "MultiPolygon":
            for poly in res["coordinates"]:
                _arr = _arr + self.feasiblePoints(poly)
        else:
            _arr = _arr + self.feasiblePoints(res["coordinates"][0])

        return _arr

    def feasiblePoints(self, poly):
        '''
        1. 将Polygon对象转化为点
        2. 超出Width范围的点排除
        3. 直线与边界的交点选入
        '''
        result = []
        for pt in poly:
            # (1) 超出了上侧&总宽度没有超过
            feasible1 = pt[1] - self.border_top > 0 and pt[1] - self.border_top + self.border_height <= self.width
            # (2) 超过了下侧&总宽度没有超过
            feasible2 = self.border_bottom - pt[1] > 0 and self.border_bottom - pt[1] + self.border_heigt <= self.width
            # (3) Top和bottom的内部
            feasible3 = pt[1] <= self.border_top and pt[1] >= self.border_bottom
            if feasible1 == True or feasible2 == True or feasible3 == True:
                result.append([pt[0], pt[1]])
        return result

    def slideToBottomLeft(self):
        '''移到最左下角位置'''
        for poly in self.cur_polys:
            GeometryFunctions.slide_polygon(poly, -self.border_left, -self.border_bottom)

    def showResult(self):
        '''显示排样结果'''
        for poly in self.cur_polys:
            PltFunc.addPolygon(poly)
        PltFunc.showPlt(width=2000, height=2000)