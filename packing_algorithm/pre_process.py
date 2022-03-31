# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> pre_process.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 11:01
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import copy
import csv
import json
import math

from shapely import affinity
from shapely.geometry import mapping
from shapely.geometry import Point
from shapely.geometry import Polygon

import pandas as pd
from config import targets
from tools.geometry_functions import GeometryFunctions
from tools.lp_assistant import LPAssistant
from tools.nfp import NFP


class PreProccess(object):
    """
    预处理NFP以及NFP divided函数
    """

    def __init__(self, index):
        self.set_name = targets[index]["name"]
        self.min_angle = 360 / targets[index]["allowed_rotation"]
        self.zoom = targets[index]["scale"]
        self.orientation()
        self.main()

    def orientation(self):
        fu = pd.read_csv("data/" + self.set_name + ".csv")
        _len = fu.shape[0]
        min_angle = self.min_angle
        rotation_range = [j for j in range(int(360 / self.min_angle))]
        with open("data/" + self.set_name + "_orientation.csv", "a+") as csvfile:
            writer = csv.writer(csvfile)
            for i in range(_len):
                Poly_i = Polygon(self.normData(json.loads(fu["polygon"][i])))
                all_poly = []
                for oi in rotation_range:
                    new_Poly_i = self.newRotation(Poly_i, oi, min_angle)
                    new_poly_i = self.getPoint(new_Poly_i)
                    all_poly.append(new_poly_i)
                if len(rotation_range) == 4:
                    ver_sym, hori_sym = 0, 0
                    if Polygon(all_poly[0]).intersection(Polygon(all_poly[2])).area == Polygon(all_poly[0]).area:
                        ver_sym = 1
                    if Polygon(all_poly[1]).intersection(Polygon(all_poly[3])).area == Polygon(all_poly[1]).area:
                        hori_sym = 1
                    all_poly.append(ver_sym)
                    all_poly.append(hori_sym)
                elif len(rotation_range) == 2:
                    ver_sym = 0
                    if Polygon(all_poly[0]).intersection(Polygon(all_poly[1])).area == Polygon(all_poly[0]).area:
                        ver_sym = 1
                    all_poly.append(ver_sym)

                writer.writerows([all_poly])

    def main(self):
        fu = pd.read_csv("data/" + self.set_name + ".csv")
        _len = fu.shape[0]
        min_angle = self.min_angle
        rotation_range = [j for j in range(int(360 / self.min_angle))]
        with open("data/" + self.set_name + "_nfp.csv", "a+") as csvfile:
            writer = csv.writer(csvfile)
            for i in range(_len):
                # for i in range(2,3):
                Poly_i = Polygon(self.normData(json.loads(fu["polygon"][i])))  # 固定形状
                for j in range(_len):
                    # for j in range(3,4):
                    Poly_j = Polygon(self.normData(json.loads(fu["polygon"][j])))  # 移动的形状
                    for oi in rotation_range:
                        new_poly_i = self.rotation(Poly_i, oi, min_angle)
                        self.slideToOrigin(new_poly_i)
                        for oj in rotation_range:
                            print(i, j, oi, oj)
                            new_poly_j = self.rotation(Poly_j, oj, min_angle)
                            nfp = NFP(new_poly_i, new_poly_j)
                            new_nfp = LPAssistant.deleteOnline(nfp.nfp)
                            convex_status = self.get_convex_status(new_nfp)
                            vertical_direction = PreProccess.get_vertical_direction(convex_status, new_nfp)
                            first_pt = new_nfp[0]
                            new_NFP = Polygon(new_nfp)
                            bounds = new_NFP.bounds
                            bounds = [bounds[0] - first_pt[0], bounds[1] - first_pt[1], bounds[2] - first_pt[0],
                                      bounds[3] - first_pt[1]]
                            writer.writerows([[i, j, oi, oj, new_poly_i, new_poly_j, new_nfp, convex_status,
                                               vertical_direction, bounds]])

    def get_convex_status(self, nfp):
        """
        判断凹点还是凸点
        """
        if len(nfp) == 3:
            return [1, 1, 1]
        convex_status = []
        for i in range(len(nfp)):
            nfp_after_del = copy.deepcopy(nfp)
            del nfp_after_del[i]
            if Polygon(nfp_after_del).contains(Point(nfp[i])):
                convex_status.append(0)
            else:
                convex_status.append(1)
        return convex_status

    @staticmethod
    def get_vertical_direction(convex_status, nfp):
        """
        获得某个凹点的两个垂线
        """
        target_NFP, extend_nfp = Polygon(nfp), nfp + nfp
        vertical_direction = []
        for i, status in enumerate(convex_status):
            # 如果不垂直，则需要计算垂线了
            if status == 0:
                vec1 = PreProccess.rotationDirection(
                    [extend_nfp[i][0] - extend_nfp[i - 1][0], extend_nfp[i][1] - extend_nfp[i - 1][1]])
                vec2 = PreProccess.rotationDirection(
                    [extend_nfp[i + 1][0] - extend_nfp[i][0], extend_nfp[i + 1][1] - extend_nfp[i][1]])
                vertical_direction.append([vec1, vec2])
            else:
                vertical_direction.append([[], []])
        return vertical_direction

    @staticmethod
    def rotationDirection(vec):
        theta = math.pi / 2
        new_x = vec[0] * math.cos(theta) - vec[1] * math.sin(theta)
        new_y = vec[0] * math.sin(theta) + vec[1] * math.cos(theta)
        return [new_x, new_y]

    def slideToOrigin(self, poly):
        bottom_pt, min_y = [], 999999999
        for pt in poly:
            if pt[1] < min_y:
                min_y = pt[1]
                bottom_pt = [pt[0], pt[1]]
        GeometryFunctions.slide_polygon(poly, -bottom_pt[0], -bottom_pt[1])

    def normData(self, poly):
        new_poly, num = [], self.zoom
        for pt in poly:
            new_poly.append([pt[0] * num, pt[1] * num])
        return new_poly

    def rotation(self, Poly, orientation, min_angle):
        if orientation == 0:
            return self.getPoint(Poly)
        new_Poly = affinity.rotate(Poly, min_angle * orientation)
        return self.getPoint(new_Poly)

    def newRotation(self, Poly, orientation, min_angle):
        if orientation == 0:
            return Poly
        new_Poly = affinity.rotate(Poly, min_angle * orientation)
        return new_Poly

    def getPoint(self, shapely_object):
        mapping_res = mapping(shapely_object)
        coordinates = mapping_res["coordinates"][0]
        new_poly = []
        for pt in coordinates:
            new_poly.append([pt[0], pt[1]])
        return new_poly

    def normFile(self):
        data = pd.read_csv("../data/mao_orientation.csv")
        with open("../data/mao_orientation.csv", "a+") as csvfile:
            writer = csv.writer(csvfile)
            for row in range(data.shape[0]):
                o_1 = self.normData(json.loads(data["o_1"][row]))
                o_2 = self.normData(json.loads(data["o_2"][row]))
                o_3 = self.normData(json.loads(data["o_3"][row]))
                writer.writerows([[o_0, o_1, o_2, o_3]])
