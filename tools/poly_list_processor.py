# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> poly_list_processor.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 15:57
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import copy
import random

import packing_algorithm.tools.bottom_left_fill
from tools import heuristic
from tools.poly import Poly


def main(name):
    print(f'Hi, {name}')
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class PolyListProcessor(object):
    @staticmethod
    def getPolyObjectList(polys, allowed_rotation):
        '''
        将Polys和允许旋转的角度转化为poly_lists
        '''
        poly_list = []
        for i, poly in enumerate(polys):
            poly_list.append(Poly(i, poly, allowed_rotation))
        return poly_list

    @staticmethod
    def getPolysVertices(_list):
        '''排序结束后会影响'''
        polys = []
        for i in range(len(_list)):
            polys.append(_list[i].poly)
        return polys

    @staticmethod
    def getPolysVerticesCopy(_list):
        '''不影响list内的形状'''
        polys = []
        for i in range(len(_list)):
            polys.append(copy.deepcopy(_list[i].poly))
        return polys

    @staticmethod
    def getPolyListIndex(poly_list):
        index_list = []
        for i in range(len(poly_list)):
            index_list.append(poly_list[i].num)
        return index_list

    @staticmethod
    def getIndex(item, _list):
        for i in range(len(_list)):
            if item == _list[i]:
                return i
        return -1

    @staticmethod
    def getIndexMulti(item, _list):
        index_list = []
        for i in range(len(_list)):
            if item == _list[i]:
                index_list.append(i)
        return index_list

    @staticmethod
    def packingLength(poly_list, history_index_list, history_length_list, width, **kw):
        polys = PolyListProcessor.getPolysVertices(poly_list)
        index_list = PolyListProcessor.getPolyListIndex(poly_list)
        length = 0
        check_index = PolyListProcessor.getIndex(index_list, history_index_list)
        if check_index >= 0:
            length = history_length_list[check_index]
        else:
            try:
                if 'NFPAssistant' in kw:
                    length = packing_algorithm.tools.bottom_left_fill.BottomLeftFill(width, polys, NFPAssistant=kw['NFPAssistant']).contain_length
                else:
                    length = packing_algorithm.tools.bottom_left_fill.BottomLeftFill(width, polys).contain_length
            except:
                print('出现Self-intersection')
                length = 99999
            history_index_list.append(index_list)
            history_length_list.append(length)
        return length

    @staticmethod
    def randomSwap(poly_list, target_id):
        new_poly_list = copy.deepcopy(poly_list)

        swap_with = int(random.random() * len(new_poly_list))

        item1 = new_poly_list[target_id]
        item2 = new_poly_list[swap_with]

        new_poly_list[target_id] = item2
        new_poly_list[swap_with] = item1
        return new_poly_list

    @staticmethod
    def randomRotate(poly_list, min_angle, target_id):
        new_poly_list = copy.deepcopy(poly_list)

        index = random.randint(0, len(new_poly_list) - 1)
        heuristic.RatotionPoly(min_angle).rotation(new_poly_list[index].poly)
        return new_poly_list

    @staticmethod
    def showPolyList(width, poly_list):
        blf = packing_algorithm.tools.bottom_left_fill.BottomLeftFill(width, PolyListProcessor.getPolysVertices(poly_list))
        blf.show_all()

    @staticmethod
    def deleteRedundancy(_arr):
        new_arr = []
        for item in _arr:
            if not item in new_arr:
                new_arr.append(item)
        return new_arr

    @staticmethod
    def getPolysByIndex(index_list, poly_list):
        choosed_poly_list = []
        for i in index_list:
            choosed_poly_list.append(poly_list[i])
        return choosed_poly_list