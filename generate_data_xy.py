# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> generate_data_xy.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-24 14:32
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from datetime import datetime

import numpy as np

from tools.nfp_assistant import NFPAssistant
from tools.polygon import get_data


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class GenerateDataXY(object):
    """
    04/09后采用vector方法生成 弃用此类
    """

    @staticmethod
    def generate_rectangle(poly_num=1, max_width=51, max_height=51):
        """
        随机生成矩形

        Args:
            poly_num: 生成矩形的个数
            max_width: 生成矩形的最大宽度
            max_height: 生成矩形的最大高度
        """
        rectangle_array = np.zeros((poly_num, 4 * 2))  # 4个点 x 2个坐标
        for i in range(poly_num):
            x = np.random.randint(50, max_width)
            y = np.random.randint(50, max_height)
            points = [0, 0, x, 0, x, y, 0, y]
            rectangle_array[i] = points
        return rectangle_array

    @staticmethod
    def generate_regular_polygon(poly_num=1, max_point_num=1):
        """
        随机生成正多边形
        poly_num: 生成正多边形个数
        max_point_num: 多边形的顶点个数
        """
        polys = np.zeros((poly_num, max_point_num * 2))
        center = [200, 200]  # 中心坐标
        for i in range(poly_num):
            point_num = np.random.randint(3, max_point_num + 1)
            angle = 360 / point_num  # 根据边数划分角度区域
            theta_start = np.random.randint(0, angle)
            for j in range(point_num):
                theta = (theta_start + angle * j) * np.pi / 180  # 在每个区域中取角度并转为弧度
                # max_r=min(np.math.fabs(500/np.math.cos(theta)),np.math.fabs(500/np.math.sin(theta)))
                r = 100 + (160 - 100) * np.random.random()
                x = center[0] + r * np.math.cos(theta)
                y = center[1] + r * np.math.sin(theta)
                polys[i, 2 * j] = x
                polys[i, 2 * j + 1] = y
                # print(theta,x,y)
        return polys

    @staticmethod
    def generate_test_data(size, poly_num=10, max_point_num=4):
        x = []
        for i in range(size):
            polys = GenerateDataXY.polys2data(get_data())
            # polys=generate_regular_polygon(poly_num,max_point_num)
            polys = polys.T
            x.append(polys)
        x = np.array(x)
        np.save('test{}_{}_{}'.format(size, poly_num, max_point_num), x)

    @staticmethod
    def get_all_nfp(data_source, max_point_num):
        data = np.load(data_source)
        polys = []
        for i in range(0, len(data)):
            line = data[i]
            poly_new = []
            line = line.T
            for j in range(len(line)):
                poly_new.append(line[j].reshape(max_point_num, 2).tolist())
            poly_new = GenerateDataXY.drop0(poly_new)
            nfp_asst = NFPAssistant(poly_new, get_all_nfp=True, store_nfp=True,
                                    store_path='record/fu1500_val/{}.csv'.format(i))

    @staticmethod
    def generate_data_fu(poly_num):
        polys = np.zeros((poly_num, 8))  # 最多4个点 x 2个坐标
        for i in range(poly_num):
            shape = np.random.randint(0, 8)  # 矩形 直角三角形 等腰三角形 直角梯形
            b = 500
            a = 25
            x = a + (b - a) * np.random.random()
            y = a + (b - a) * np.random.random()
            points = [0, 0, 0, 0, 0, 0, 0, 0]
            if shape == 0 or shape == 1:
                points = [0, 0, x, 0, x, y, 0, y]
            elif shape == 2:
                points = [0, 0, x, 0, x, y, 0, 0]
            elif shape == 3:
                points = [0, 0, x, y, 0, y, 0, 0]
            elif shape == 4:
                points = [0, 0, x, 0, x / 2, y, 0, 0]
            elif shape == 5:
                points = [0, 0, x, y / 2, 0, y, 0, 0]
            elif shape == 6:
                x2 = a + (b - a) * np.random.random()
                points = [0, 0, x2, 0, x, y, 0, y]
            elif shape == 7:
                y2 = a + (b - a) * np.random.random()
                points = [0, 0, x, 0, x, y2, 0, y]
            polys[i] = points
        return polys  # [ poly_num x (max_point_num * 2) ]  

    @staticmethod
    def polys2data(polys):
        """
        将poly进行reshape满足网络输入格式
        """
        max_point_num = 0
        size = len(polys)
        for poly in polys:
            point_num = len(poly)
            if point_num > max_point_num:
                max_point_num = point_num
        polys_new = np.zeros((size, max_point_num * 2))
        for i in range(size):
            poly = polys[i]
            point_num = len(poly)
            poly = np.array(poly)
            poly = poly.reshape(1, point_num * 2)
            poly = poly[0]
            for index, point in enumerate(poly):
                polys_new[i][index] = point
        return polys_new

    @staticmethod
    def drop0(polys):
        """
        网络输出的polys传入其他函数之前[必须完成]
        把所有多边形末尾的补零去掉
        """
        polys_new = []
        point_index = 0
        for poly in polys:
            for i in range(len(poly)):
                point_index = len(poly) - 1 - i
                if poly[point_index] == [0, 0]:
                    continue
                else:
                    break
            poly = poly[0:point_index + 1]
            polys_new.append(poly)
        return polys_new