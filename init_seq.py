# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> init_seq.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-24 14:33
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import itertools
from datetime import datetime

from shapely.geometry import Polygon

from packing_algorithm.tools import BottomLeftFill
from tools.geometry_functions import GeometryFunctions
from tools.nfp_assistant import NFPAssistant


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class InitSeq(object):
    def __init__(self, width, polys, nfp_load=None, nfp_asst=None):
        self.polys = polys
        self.width = width
        self.simple = True
        if nfp_load is not None:
            self.NFPAssistant = NFPAssistant(polys, load_history=True, history_path=nfp_load)
        else:
            self.NFPAssistant = nfp_asst

    # 获得面积/长度/高度降序排列的形状结果
    def get_decrease(self, criteria):
        poly_list = []
        for index, poly in enumerate(self.polys):
            if criteria == 'length':
                left, bottom, right, top = GeometryFunctions.check_bound_value(poly)
                poly_list.append([poly, right - left, index])
            elif criteria == 'height':
                left, bottom, right, top = GeometryFunctions.check_bound_value(poly)
                poly_list.append([poly, top - bottom, index])
            else:
                poly_list.append([poly, Polygon(poly).area, index])
        poly_list = sorted(poly_list, key=lambda _item: _item[1], reverse=True)  # 排序，包含index
        dec_polys = []
        for item in poly_list:
            dec_polys.append(item)
        return dec_polys

    # 获得所有降序排列方案的最优解
    def get_best(self):
        min_height = 999999999
        heights = []
        best_criteria = ''
        final_polys = []
        final_indexes = []
        for criteria in ['area', 'length', 'height']:
            init_list = self.get_decrease(criteria)
            if not self.simple:
                # 获得全部聚类结果
                clustering, now_clustering, last_value = [], [], init_list[0][1]
                for item in init_list:
                    if item[1] == last_value:
                        now_clustering.append(item)
                    else:
                        clustering.append(now_clustering)
                        last_value = item[1]
                        now_clustering = [item]
                clustering.append(now_clustering)
                # 获得全部序列
                one_lists = []
                for item in clustering:
                    one_list = list(itertools.permutations(item))
                    one_lists.append(one_list)
                all_lists = itertools.product(*one_lists)
                lists = []
                for cur_lists in all_lists:
                    cur_list = []
                    for polys in cur_lists:
                        for poly in polys:
                            cur_list.append(poly)
                    lists.append(cur_list)
            else:
                lists = [init_list]
            for item in lists:
                polys_final = []
                indexes_final = []
                for poly in item:
                    polys_final.append(poly[0])
                    indexes_final.append(poly[2])
                blf = BottomLeftFill(self.width, polys_final, vertical=False, NFPAssistant=self.NFPAssistant)
                height = blf.get_length()
                heights.append(height)
                if height < min_height:
                    min_height = height
                    best_criteria = criteria
                    final_polys = polys_final
                    final_indexes = indexes_final
        # print(sorted(heights,reverse=False))
        # print(min_height,best_criteria)
        area = 0
        for poly in self.polys:
            area = area + Polygon(poly).area
        use_ratio = area / (self.width * min_height)
        # print(area,use_ratio)
        return use_ratio, best_criteria, final_polys, final_indexes

    # 枚举所有序列并选择最优
    def get_all(self):
        all_com = list(itertools.permutations([(i) for i in range(len(self.polys))]))
        min_height = 999999999
        best_order = []
        for item in all_com:
            seq = self.get_polys(item)
            height = BottomLeftFill(self.width, seq, NFPAssistant=self.NFPAssistant).get_length()
            if height < min_height:
                best_order = item
                min_height = height
        area = 0
        for poly in self.polys:
            area = area + Polygon(poly).area
        use_ratio = area / (self.width * min_height)
        return best_order, min_height, use_ratio

    def get_polys(self, seq):
        seq_polys = []
        for i in seq:
            seq_polys.append(self.polys[i])
        return seq_polys