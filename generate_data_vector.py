# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> generate_data_vector.py
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
from shapely.geometry import Polygon
from tqdm import tqdm
from tqdm import tqdm

from tools.polygon import get_data
from tools.rotation_polygon import RotationPolygon
from tools.rotation_polygon import RotationPolygon
from tools.rotation_polygon import RotationPolygon
from tools.rotation_polygon import RotationPolygon
from tools.rotation_polygon import RotationPolygon
from tools.rotation_polygon import RotationPolygon
from tools.rotation_polygon import RotationPolygon
from tools.rotation_polygon import RotationPolygon
from tools.vectorization import vectorFunc
from tools.vectorization import vectorFunc
from tools.vectorization import vectorFunc


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class GenerateDataVector(object):

    @staticmethod
    def generate_special_polygon(shape):
        # shape: 1 直角三角形 2 等腰三角形 3 矩形 4 直角梯形 5 菱形
        b = 250
        a = 100
        x = a + (b - a) * np.random.random()
        y = a + (b - a) * np.random.random()
        poly = []
        if shape == 1:
            poly = np.array([0, 0, x, 0, 0, y]).reshape(3, 2).tolist()
            RotationPolygon(90).rotation(poly)
        elif shape == 2:
            poly = np.array([0, 0, x, 0, x / 2, y]).reshape(3, 2).tolist()
            RotationPolygon(90).rotation(poly)
        elif shape == 3:
            poly = np.array([0, 0, x, 0, x, y, 0, y]).reshape(4, 2).tolist()
            RotationPolygon(90).rotation(poly)
        elif shape == 4:
            x2 = a + (b - a) * np.random.random()
            poly = np.array([0, 0, x2, 0, x, y, 0, y]).reshape(4, 2).tolist()
            RotationPolygon(90).rotation(poly)
        elif shape == 5:
            poly = np.array([0, 0, x / 2, -y / 2, x, 0, x / 2, y / 2]).reshape(4, 2).tolist()
            RotationPolygon(90).rotation(poly)
        return poly

    @staticmethod
    def generate_polygon(point_num, is_regular):
        """
        随机生成多边形
        point_num: 点的个数
        is_regular: 是否正多边形
        """
        r_max = 140
        r_min = 60
        poly = []
        angle = 360 / point_num  # 根据边数划分角度区域
        r = r_min + (r_max - r_min) * np.random.random()
        for j in range(point_num):
            theta_min = angle * j
            theta_max = angle * (j + 1)
            theta = theta_min if is_regular else theta_min + (theta_max - theta_min) * np.random.random()
            theta = theta * np.pi / 180  # 角度转弧度
            # max_r=min(np.math.fabs(500/np.math.cos(theta)),np.math.fabs(500/np.math.sin(theta)))
            if not is_regular:
                r = r_min + (r_max - r_min) * np.random.random()
            x = r * np.math.cos(theta)
            y = r * np.math.sin(theta)
            poly.append([x, y])
        if is_regular:
            if point_num == 5 or point_num == 7:
                RotationPolygon(360).rotation_specific(poly, angle=[i * 90 for i in range(4)])
            elif point_num == 6:
                RotationPolygon(360).rotation_specific(poly, angle=[0, 90])
            elif point_num == 8:
                RotationPolygon(360).rotation_specific(poly, angle=[0, 45 / 2])
        return poly

    @staticmethod
    def generate_test_data(dataset_name, size):
        data = []
        vectors = []
        poly = []
        for i in tqdm(range(size)):
            polys = []
            for j in range(12):
                polyCheck = False
                while not polyCheck:
                    dice = np.random.random()
                    if dice < 1:
                        shape = np.random.randint(1, 6)
                        poly = GenerateDataVector.generate_special_polygon(shape)
                    elif dice < 0.7:
                        point_num = np.random.randint(3, 9)
                        poly = GenerateDataVector.generate_polygon(point_num, True)
                    else:
                        point_num = np.random.randint(3, 9)
                        poly = GenerateDataVector.generate_polygon(point_num, False)
                    if Polygon(poly).area > 5000:  # 面积过小会导致无法计算NFP
                        polyCheck = True
                polys.append(poly)
            # blf=BottomLeftFill(760,polys)
            # blf.showAll()
            data.append(polys)
            vector = []
            for poly in polys:
                vector.append(vectorFunc(poly, cut_nums=128).vector)
            vectors.append(vector)
        data = np.array(data)
        vectors = np.array(vectors)
        np.save('{}_xy'.format(dataset_name), data)
        np.save('{}'.format(dataset_name), vectors)

    @staticmethod
    def poly2vector(source, save_name):
        data = np.load(source, allow_pickle=True)
        vectors = []
        for index, line in enumerate(tqdm(data)):
            vector = []
            for poly in line:
                vector.append(vectorFunc(poly, cut_nums=128).vector)
            vectors.append(vector)
        vectors = np.array(vectors)
        np.save(save_name, vectors)

    @staticmethod
    def export_dataset(index, export_name):
        data = []
        vectors = []
        polys = get_data()
        data.append(polys)
        vector = []
        for poly in polys:
            vector.append(vectorFunc(poly, cut_nums=128).vector)
        vectors.append(vector)
        data = np.array(data)
        vectors = np.array(vectors)
        np.save('{}_xy'.format(export_name), data)
        np.save('{}'.format(export_name), vectors)