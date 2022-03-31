# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> ILSQN.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-16 11:37
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import copy
import random
from datetime import datetime

from packing_algorithm.tools.bottom_left_fill import BottomLeftFill
from tools.nfp_assistant import NFPAssistant
from tools.poly_list_processor import PolyListProcessor


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class ILSQN():
    '''
    参考资料：2009 An iterated local search algorithm based on nonlinear programming for the irregular strip packing problem
    '''

    def __init__(self, poly_list):
        # 初始设置
        self.width = 1500

        # 初始化数据，NFP辅助函数
        polys = PolyListProcessor.getPolysVertices(poly_list)
        self.NFPAssistant = NFPAssistant(polys, get_all_nfp=False)

        # 获得最优解
        blf = BottomLeftFill(self.width, polys, NFPAssistant=self.NFPAssistant)
        self.best_height = blf.contain_height
        self.cur_height = blf.contain_height

        # 当前的poly_list均为已经排样的情况
        self.best_poly_list = copy.deepcopy(poly_list)
        self.cur_poly_list = copy.deepcopy(poly_list)

        self.run()

    def run(self):
        for i in range(1):
            if self.minimizeOverlap():
                pass
            else:
                pass

    def minimizeOverlap(self):
        k = 0
        while k < 5:
            initial_solution, height = self.swapTwoPolygons()
            lopt_solution = self.separate(initial_solution)
            pass

    def findBestPosition(self):
        pass

    def swapTwoPolygons(self):
        i, j = random.randint(0, len(self.cur_poly_list) - 1), random.randint(0, len(self.cur_poly_list) - 1)
        pass

    def separate(self):
        pass