import json
import os
import random
import time

import pandas as pd

from packing_algorithm.config import log_config
from test import try_nfp
from tools.geometry_functions import GeometryFunctions
from tools.plt_func import PltFunc


def outputWarning(_str):
    """
    输出红色字体
    """
    _str = str(time.strftime("%H:%M:%S", time.localtime())) + " " + str(_str)
    print("\033[0;31m", _str, "\033[0m")


def outputAttention(_str):
    """
    输出绿色字体
    """
    _str = str(time.strftime("%H:%M:%S", time.localtime())) + " " + str(_str)
    print("\033[0;32m", _str, "\033[0m")


def outputInfo(_str):
    """
    输出浅黄色字体
    """
    _str = str(time.strftime("%H:%M:%S", time.localtime())) + " " + str(_str)
    print("\033[0;33m", _str, "\033[0m")


def polygon_func_check(polygons):
    for poly in polygons:
        PltFunc.addPolygon(poly)
    PltFunc.showPlt(width=2500, height=2500)


def get_data(_index=2):
    index = _index
    # index = 12 # shapes
    # index = 5 # dighe2
    # index = 13 # shirts
    # index = 11 # marques
    """
    报错数据集有（空心）：han, jakobs1, jakobs2 
    """
    '''形状过多暂时未处理：shapes、shirt、swim、trousers'''
    name = ["ga", "albano", "blaz", "blaz2", "dighe1", "dighe2", "fu", "han", "jakobs1", "jakobs2", "mao", "marques",
            "shapes", "shirts", "swim", "trousers", "convex", "simple", "ali2", "ali3"]
    print("开始处理", name[index], "数据集")
    '''暂时没有考虑宽度，全部缩放来表示'''
    scale = [100, 0.5, 50, 100, 10, 10, 20, 10, 20, 20, 0.5, 10, 50, 20, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1]
    print("缩放", scale[index], "倍")
    user_name = os.getlogin()
    if user_name == 'Prinway' or user_name == 'mac':
        df = pd.read_csv("data/" + name[index] + ".csv")
    else:
        df = pd.read_csv("data/" + name[index] + ".csv")
    polygons = []
    polys_type = []
    for i in range(0, df.shape[0]):
        # for i in range(0,4):
        for j in range(0, df['num'][i]):
            polys_type.append(i)
            poly = json.loads(df['polygon'][i])
            GeometryFunctions.normal_data(poly, scale[index])
            polygons.append(poly)
    print(polys_type)
    return polygons


def get_convex(**kw):
    if os.getlogin() == 'Prinway':
        df = pd.read_csv("record/convex.csv")
    else:
        df = pd.read_csv("/Users/sean/Documents/Projects/data/convex.csv")
    polygons = []
    poly_index = []
    if 'num' in kw:
        for i in range(kw["num"]):
            poly_index.append(random.randint(0, 7000))
    elif 'certain' in kw:
        poly_index = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
    else:
        poly_index = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
    # poly_index=[5579, 2745, 80, 6098, 3073, 8897, 4871, 4266, 3477, 3266, 8016, 4563, 1028, 10842, 1410, 7254, 5953, 82, 1715, 300]
    for i in poly_index:
        poly = json.loads(df['polygon'][i])
        polygons.append(poly)
    if 'with_index' in kw:
        return poly_index, polygons
    return polygons


if __name__ == '__main__':
    log_config()
    try_nfp()
    # P = Polygon([[0,0],[100,0],[100,100],[100,0],[200,0],[200,200],[0,200]])
    # print(P)
    # getData()
    # polygonFuncCheck()
    # PltFunc.addPolygonColor(((0, 580), (480, 580), (480, 200), (0, 200), (0, 580)))
    # PltFunc.addPolygon(((248.47, 860), (448.47, 940), (648.47, 940), (648.47, 560), (248.47, 560)))
    # PltFunc.addPolygon(((604.326, 180), (200, 180), (200, 760), (604.326, 760), (604.326, 180)))
    # PltFunc.addPolygonColor([[234.286,560],[360,560],[380,560],[380,723.959],[380,723.959],[380,460],[234.286,460],[234.286,560]])
    # PltFunc.addPolygon([[-80,580,],[200,580,],[200,400,],[-80,400,]])
    # PltFunc.addPolygon(((480, 200), (480, 380), (200, 380), (200, 760), (1e+08, 760), (1e+08, 200), (480, 200)))
    # PltFunc.showPlt()
    pass
