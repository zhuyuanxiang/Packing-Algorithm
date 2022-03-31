# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> initial_result.py
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
import itertools

from packing_algorithm.tools.bottom_left_fill import BottomLeftFill
from tools.lp_assistant import LPAssistant
from tools.nfp_assistant import NFPAssistant


class InitialResult(object):
    def __init__(self, polys):
        self.polys = polys
        self.main(_type="length")

    def main(self, _type):
        _list = []
        if _type == "area":
            pass
        elif _type == "length":
            _list = self.getLengthDecreaing()
        elif _type == "width":
            _list = self.getWidthDecreaing()
        elif _type == "rectangularity":
            pass
        else:
            pass
        # 重排列后的结果
        self.nfp_assistant = NFPAssistant(self.polys, store_nfp=True, get_all_nfp=False, load_history=False)
        new_list = sorted(_list, key=lambda item: item[1], reverse=True)

    def checkOneSeq(self, one_list):
        new_polys = []
        for item in one_list:
            new_polys.append(self.polys[item[0]])

        packing_polys = BottomLeftFill(760, new_polys, NFPAssistant=self.nfp_assistant).polygons
        _len = LPAssistant.getLength(packing_polys)

        ratio = 433200 / (_len * 760)

        res = [[] for i in range(len(new_polys))]
        for i, item in enumerate(one_list):
            res[one_list[i][0]] = packing_polys[i]

        return ratio, res

    def getAreaDecreaing(self):
        pass

    def getWidthDecreaing(self, polys):
        width_list = []
        for i, poly in enumerate(self.polys):
            left_pt, right_pt = LPAssistant.getLeftPoint(poly), LPAssistant.getRightPoint(poly)
            width_list.append([i, right_pt[0] - left_pt[0]])
        return width_list

    def getLengthDecreaing(self):
        length_list = []
        for i, poly in enumerate(self.polys):
            bottom_pt, top_pt = LPAssistant.getBottomPoint(poly), LPAssistant.getTopPoint(poly)
            length_list.append([i, top_pt[1] - bottom_pt[1]])
        return length_list

    def getRectangularityDecreaing(self, polys):

        pass

    def getAllSeq(self, _list):
        '''
        当前获得是全部序列
        '''
        # 初步排列
        new_list = sorted(_list, key=lambda item: item[1], reverse=True)
        # 获得全部聚类结果
        clustering, now_clustering, last_value = [], [], new_list[0][1]
        for i, item in enumerate(new_list):
            if item[1] == last_value:
                now_clustering.append(item)
            else:
                clustering.append(now_clustering)
                last_value = item[1]
                now_clustering = [item]
        clustering.append(now_clustering)
        # 获得全部序列
        all_list0 = list(itertools.permutations(clustering[0]))
        all_list1 = list(itertools.permutations(clustering[1]))

        n = 0
        with open("/Users/sean/Documents/Projects/Data/all_list.csv", "a+") as csvfile:
            writer = csv.writer(csvfile)
            for permutations0 in all_list0:
                for permutations1 in all_list1:
                    print("计算第", n, "个组合")
                    one_list = list(permutations0 + permutations1) + [clustering[2][0]] + [clustering[3][0]]
                    ratio, res = self.checkOneSeq(one_list)
                    writer.writerows([[n, one_list]])
                    n = n + 1
