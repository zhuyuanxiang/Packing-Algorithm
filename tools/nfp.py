# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> nfp.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 14:40
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import copy

from shapely.geometry import LineString
from shapely.geometry import mapping
from shapely.geometry import Point
from shapely.geometry import Polygon

from packing_algorithm.config import bias
from tools.geometry_functions import GeometryFunctions
from tools.plt_func import PltFunc


class NFP(object):
    """
    参考论文：Burke E K, Hellier R S R, Kendall G, et al.
    Complete and robust no-fit polygon generation for the irregular stock cutting problem[J].
    European Journal of Operational Research, 2007, 179(1): 27-49.
    """
    def __init__(self, poly1, poly2, **kw):
        self.stationary = copy.deepcopy(poly1)
        self.sliding = copy.deepcopy(poly2)
        start_point_index = GeometryFunctions.check_bottom(self.stationary)
        self.start_point = [poly1[start_point_index][0], poly1[start_point_index][1]]
        self.locus_index = GeometryFunctions.check_top(self.sliding)
        # 如果不加list则original_top是指针
        self.original_top = list(self.sliding[self.locus_index])
        GeometryFunctions.slideToPoint(self.sliding, self.sliding[self.locus_index], self.start_point)
        self.start = True  # 判断是否初始
        self.nfp = []
        self.rectangle = False
        if 'rectangle' in kw:
            if kw["rectangle"]:
                self.rectangle = True
        self.error = 1
        self.main()
        if 'show' in kw:
            if kw["show"]:
                self.showResult()

    def main(self):
        self.last_slide = [0, 0]  # 记录上一阶段平移情况
        i = 0
        if self.rectangle:  # 若矩形则直接快速运算 点的index为左下角开始逆时针旋转
            width = self.sliding[1][0] - self.sliding[0][0]
            height = self.sliding[3][1] - self.sliding[0][1]
            self.nfp.append([self.stationary[0][0], self.stationary[0][1]])
            self.nfp.append([self.stationary[1][0] + width, self.stationary[1][1]])
            self.nfp.append([self.stationary[2][0] + width, self.stationary[2][1] + height])
            self.nfp.append([self.stationary[3][0], self.stationary[3][1] + height])
        else:
            while not self.judgeEnd() and i < 500:  # 大于等于500会自动退出的，一般情况是计算出错
                # while i < 11:
                # print("########第",i,"轮##########")
                touching_edges = self.detectTouching()
                all_vectors = self.potentialVector(touching_edges)
                if len(all_vectors) == 0:
                    print("没有潜在向量")
                    self.error = -2  # 没有可行向量
                    break

                vector = self.feasibleVector(all_vectors, touching_edges)
                if not vector:
                    print("潜在向量均不可行")
                    self.error = -5  # 没有计算出可行向量
                    break

                self.trimVector(vector)
                if vector == [0, 0]:
                    print("未进行移动")
                    self.error = -3  # 未进行移动
                    break

                self.last_slide = [vector[0], vector[1]]

                GeometryFunctions.slide_polygon(self.sliding, vector[0], vector[1])
                self.nfp.append([self.sliding[self.locus_index][0], self.sliding[self.locus_index][1]])
                i = i + 1
                inter = Polygon(self.sliding).intersection(Polygon(self.stationary))
                if GeometryFunctions.compute_intersect_area(inter) > 1:
                    print("出现相交区域")
                    self.error = -4  # 出现相交区域
                    break  # print("")

        if i == 500:
            print("超出计算次数")
            self.error = -1  # 超出计算次数

    # 检测相互的连接情况
    def detectTouching(self):
        touch_edges = []
        stationary_edges, sliding_edges = self.getAllEdges()
        # print(stationary_edges)
        # print(sliding_edges)
        for edge1 in stationary_edges:
            for edge2 in sliding_edges:
                inter = GeometryFunctions.intersection(edge1, edge2)
                if inter:
                    # print("edge1:",edge1)
                    # print("edge2:",edge2)
                    # print("inter:",inter)
                    # print("")
                    pt = [inter[0], inter[1]]  # 交叉点
                    edge1_bound = (
                            GeometryFunctions.almostEqual(edge1[0], pt) or GeometryFunctions.almostEqual(edge1[1],
                                                                                                         pt))  # 是否为边界
                    edge2_bound = (
                            GeometryFunctions.almostEqual(edge2[0], pt) or GeometryFunctions.almostEqual(edge2[1],
                                                                                                         pt))  # 是否为边界
                    stationary_start = GeometryFunctions.almostEqual(edge1[0], pt)  # 是否开始
                    orbiting_start = GeometryFunctions.almostEqual(edge2[0], pt)  # 是否开始
                    touch_edges.append({"edge1": edge1, "edge2": edge2, "vector1": self.edgeToVector(edge1),
                                        "vector2": self.edgeToVector(edge2), "edge1_bound": edge1_bound,
                                        "edge2_bound": edge2_bound, "stationary_start": stationary_start,
                                        "orbiting_start": orbiting_start, "pt": [inter[0], inter[1]], "type": 0})
        return touch_edges


    def potentialVector(self, touching_edges):
        """
        获得潜在的可转移向量
        """
        all_vectors = []
        for touching in touching_edges:
            aim_edge = []
            # 情况1
            if touching["edge1_bound"] == True and touching["edge2_bound"] == True:
                # 如果是两条边都是开始的
                if touching["stationary_start"] == True and touching["orbiting_start"] == True:
                    right, left, parallel = self.judgePosition(touching["edge1"], touching["edge2"])
                    touching["type"] = 0
                    if left:
                        aim_edge = [touching["edge2"][1], touching["edge2"][0]]  # 反方向
                    if right:
                        aim_edge = touching["edge1"]
                # 如果一个开始一个结束
                if touching["stationary_start"] == True and touching["orbiting_start"] == False:
                    right, left, parallel = self.judgePosition(touching["edge1"],
                                                               [touching["edge2"][1], touching["edge2"][0]])
                    touching["type"] = 1
                    if right:
                        aim_edge = touching["edge1"]
                # 如果一个结束一个开始
                if touching["stationary_start"] == False and touching["orbiting_start"] == True:
                    right, left, parallel = self.judgePosition([touching["edge1"][1], touching["edge1"][0]],
                                                               touching["edge2"])
                    touching["type"] = 2
                    if right:
                        aim_edge = [touching["edge2"][1], touching["edge2"][0]]  # 反方向
                if touching["stationary_start"] == False and touching["orbiting_start"] == False:
                    touching["type"] = 3

            # 情况2
            if touching["edge1_bound"] == False and touching["edge2_bound"] == True:
                aim_edge = [touching["pt"], touching["edge1"][1]]
                touching["type"] = 4

            # 情况3
            if touching["edge1_bound"] == True and touching["edge2_bound"] == False:
                aim_edge = [touching["edge2"][1], touching["pt"]]
                touching["type"] = 5

            if aim_edge:
                vector = self.edgeToVector(aim_edge)
                if not self.detectExisting(all_vectors, vector):  # 删除重复的向量降低计算复杂度
                    all_vectors.append(vector)
        return all_vectors

    def detectExisting(self, vectors, judge_vector):
        for vector in vectors:
            if GeometryFunctions.almostEqual(vector, judge_vector):
                return True
        return False

    def edgeToVector(self, edge):
        return [edge[1][0] - edge[0][0], edge[1][1] - edge[0][1]]

    # 选择可行向量
    def feasibleVector(self, all_vectors, touching_edges):
        """
        该段代码需要重构，过于复杂
        """
        feasible_vectors = []
        # print("\nall_vectors:",all_vectors)
        for vector in all_vectors:
            feasible = True
            # outputInfo(vector)
            # print("\nvector:",vector,"\n")
            for touching in touching_edges:
                vector1, vector2 = [], []
                # 判断方向并进行转向
                if touching["stationary_start"]:
                    vector1 = touching["vector1"]
                else:
                    vector1 = [-touching["vector1"][0], -touching["vector1"][1]]
                if touching["orbiting_start"]:
                    vector2 = touching["vector2"]
                else:
                    vector2 = [-touching["vector2"][0], -touching["vector2"][1]]
                vector12_product = GeometryFunctions.crossProduct(vector1, vector2)  # 叉积，大于0在左侧，小于0在右侧，等于0平行
                vector_vector1_product = GeometryFunctions.crossProduct(vector1, vector)  # 叉积，大于0在左侧，小于0在右侧，等于0平行
                vector_vector2_product = GeometryFunctions.crossProduct(vector2, vector)  # 叉积，大于0在左侧，小于0在右侧，等于0平行
                # print("vector:",vector)
                # print("type:",touching["type"])
                # print("vector12_product:",vector12_product)
                # print("vector1:",vector1)
                # print("vector2:",vector2)
                # print("vector_vector1_product:",vector_vector1_product)
                # print("vector_vector2_product:",vector_vector2_product)
                # 最后两种情况
                if touching["type"] == 4 and (vector_vector1_product * vector12_product) < 0:
                    feasible = False
                if touching["type"] == 5 and (vector_vector2_product * (-vector12_product)) > 0:
                    feasible = False
                # 正常的情况处理
                if vector12_product > 0:
                    if vector_vector1_product < 0 and vector_vector2_product < 0:
                        feasible = False
                if vector12_product < 0:
                    if vector_vector1_product > 0 and vector_vector2_product > 0:
                        feasible = False
                # 平行情况，需要用原值逐一判断
                if vector12_product == 0:
                    inter = GeometryFunctions.newLineInter(touching["edge1"], touching["edge2"])
                    # print(touching["edge1"])
                    # print(touching["edge2"])
                    # print("inter['geom_type']:",inter["geom_type"])
                    # print(inter)
                    # print(touching)
                    if inter["geom_type"] == "LineString":
                        if inter["length"] > 0.01:
                            # 如果有相交，则需要在左侧
                            if (touching["orbiting_start"] == True and vector_vector2_product < 0) or (
                                    touching["orbiting_start"] == False and vector_vector2_product > 0):
                                feasible = False
                    else:
                        # 在同向的时候可能发生（一头一尾）
                        if touching["orbiting_start"] != touching["stationary_start"] and vector_vector1_product == 0:
                            # 如果是指向该点的，则不可以逆向
                            if touching["stationary_start"] == False and touching["vector1"][0] * vector[0] < 0:
                                feasible = False
                            # 如果是远离该点的，则不可以同向
                            if touching["stationary_start"] == True and touching["vector1"][0] * vector[0] > 0:
                                feasible = False  # print(feasible)
            if feasible:
                feasible_vectors.append(vector)
        # 设置目标最终结果
        final_vector = feasible_vectors[0]
        # 如果有多个向量，需要判断是否和上一阶段平移相同
        if len(feasible_vectors) > 1:
            for vector in feasible_vectors:
                if not self.judgeSimilar([-vector[0], -vector[1]], self.last_slide):
                    final_vector = vector
                    break
        return final_vector

    def judgeSimilar(self, vec1, vec2):
        """
        判断两个向量是否相似
        """
        # 如果有等于零，则判断是否符合条件
        if vec1[0] == 0 or vec2[0] == 0 or vec1[1] == 0 or vec2[1] == 0:
            if (vec1[0] == 0 and vec2[0] == 0) or (vec1[1] == 0 and vec2[1] == 0):
                return True
            else:
                return False
        # 否则则进行比例判断
        if abs(vec1[0] / vec2[0] - vec1[1] / vec2[1]) < bias:
            return True
        return False

    # 削减过长的向量
    def trimVector(self, vector):
        stationary_edges, sliding_edges = self.getAllEdges()
        new_vectors = []
        for pt in self.sliding:
            for edge in stationary_edges:
                line_vector = LineString([pt, [pt[0] + vector[0], pt[1] + vector[1]]])
                end_pt = [pt[0] + vector[0], pt[1] + vector[1]]
                line_polygon = LineString(edge)
                inter = line_vector.intersection(line_polygon)
                if inter.geom_type == "Point":
                    inter_mapping = mapping(inter)
                    inter_coor = inter_mapping["coordinates"]
                    # if (end_pt[0]!=inter_coor[0] or end_pt[1]!=inter_coor[1]) and (pt[0]!=inter_coor[0] or pt[1]!=inter_coor[1]):
                    if (abs(end_pt[0] - inter_coor[0]) > 0.01 or abs(end_pt[1] - inter_coor[1]) > 0.01) and (
                            abs(pt[0] - inter_coor[0]) > 0.01 or abs(pt[1] - inter_coor[1]) > 0.01):
                        # print("start:",pt)
                        # print("end:",end_pt)
                        # print("inter:",inter)
                        # print("")
                        new_vectors.append([inter_coor[0] - pt[0], inter_coor[1] - pt[1]])

        for pt in self.stationary:
            for edge in sliding_edges:
                line_vector = LineString([pt, [pt[0] - vector[0], pt[1] - vector[1]]])
                end_pt = [pt[0] - vector[0], pt[1] - vector[1]]
                line_polygon = LineString(edge)
                inter = line_vector.intersection(line_polygon)
                if inter.geom_type == "Point":
                    inter_mapping = mapping(inter)
                    inter_coor = inter_mapping["coordinates"]
                    # if (end_pt[0]!=inter_coor[0] or end_pt[1]!=inter_coor[1]) and (pt[0]!=inter_coor[0] or pt[1]!=inter_coor[1]):
                    if (abs(end_pt[0] - inter_coor[0]) > 0.01 or abs(end_pt[1] - inter_coor[1]) > 0.01) and (
                            abs(pt[0] - inter_coor[0]) > 0.01 or abs(pt[1] - inter_coor[1]) > 0.01):
                        # print("start:",pt)
                        # print("end:",end_pt)
                        # print("inter:",inter)
                        # print("")
                        new_vectors.append([pt[0] - inter_coor[0], pt[1] - inter_coor[1]])

        # print(new_vectors)
        for vec in new_vectors:
            if abs(vec[0]) < abs(vector[0]) or abs(vec[1]) < abs(vector[1]):
                # print(vec)
                vector[0] = vec[0]
                vector[1] = vec[1]

    # 获得两个多边形全部边
    def getAllEdges(self):
        return GeometryFunctions.getPolyEdges(self.stationary), GeometryFunctions.getPolyEdges(self.sliding)

    # 判断是否结束
    def judgeEnd(self):
        sliding_locus = self.sliding[self.locus_index]
        main_bt = self.start_point
        # 首先是如果直接划过去了
        if len(self.nfp) >= 3 and GeometryFunctions.almostContain([self.nfp[-2], self.nfp[-1]], main_bt):
            self.nfp[-1] = [main_bt[0], main_bt[1]]
            return True
        # 其次是如果是正好移到位置
        if abs(sliding_locus[0] - main_bt[0]) < 0.1 and abs(sliding_locus[1] - main_bt[1]) < 0.1:
            if self.start:
                self.start = False
                # print("判断是否结束：否")
                return False
            else:
                # print("判断是否结束：是")
                return True
        else:
            # print("判断是否结束：否")
            return False

    # 显示最终结果
    def showResult(self):
        GeometryFunctions.slide_polygon(self.sliding, 200, 200)
        GeometryFunctions.slide_polygon(self.stationary, 200, 200)
        GeometryFunctions.slide_polygon(self.nfp, 200, 200)
        PltFunc.addPolygon(self.sliding)
        PltFunc.addPolygon(self.stationary)
        PltFunc.addPolygonColor(self.nfp)
        PltFunc.showPlt()

    # 计算渗透深度
    def getDepth(self):
        """
        计算poly2的checkTop到NFP的距离
        Source: https://stackoverflow.com/questions/36972537/distance-from-point-to-polygon-when-inside
        """
        d1 = Polygon(self.nfp).distance(Point(self.original_top))
        # if point in inside polygon, d1=0
        # d2: distance from the point to nearest boundary
        if d1 == 0:
            d2 = Polygon(self.nfp).boundary.distance(Point(self.original_top))
            # print('d2:',d2)
            return d2
        else:
            return 0

    def judgePosition(self, edge1, edge2):
        x1 = edge1[1][0] - edge1[0][0]
        y1 = edge1[1][1] - edge1[0][1]
        x2 = edge2[1][0] - edge2[0][0]
        y2 = edge2[1][1] - edge2[0][1]
        res = x1 * y2 - x2 * y1
        right = False
        left = False
        parallel = False
        # print("res:",res)
        if res == 0:
            parallel = True
        elif res > 0:
            left = True
        else:
            right = True
        return right, left, parallel


def main(name):
    print(f'Hi, {name}')
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
