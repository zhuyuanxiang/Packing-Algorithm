"""
该文件实现了主要基于序列的排样算法
-----------------------------------
Created on Wed Dec 11, 2019
@author: seanys,prinway
-----------------------------------
"""
import json

import pandas as pd
from shapely.geometry import Polygon

from packing_algorithm.config import datasets
from packing_algorithm.tools import BottomLeftFill
from tools.geometry_functions import GeometryFunctions
from tools.newnfpassistant import NewNfpAssistant


def get_data_new(dataset_name, dataset_scale):
    print(dataset_name)
    print("缩放", dataset_scale, "倍")

    df = pd.read_csv("../data/" + dataset_name + ".csv")
    polygons = []
    polygons_type = []
    for i in range(0, df.shape[0]):
        for j in range(0, df['num'][i]):
            # if i not in [14,15]:continue
            polygons_type.append(i)
            polygon = json.loads(df['polygon'][i])
            GeometryFunctions.normal_data(polygon, dataset_scale)
            polygons.append(polygon)
    print(polygons_type)
    return polygons


def main():
    index = 8
    dataset = datasets[index]
    dataset_name = dataset["name"]
    dataset_allowed_rotation = dataset["allowed_rotation"]
    dataset_width = dataset["width"]
    dataset_scale = dataset["scale"]

    # global polygons, poly, index
    polygons = get_data_new(dataset_name, dataset_scale)
    total_area = 0
    for polygon in polygons:
        total_area = total_area + Polygon(polygon).area
    print("total_area:", total_area)
    print("number:", len(polygons))
    print([0 for i in range(len(polygons))])
    # 计算NFP时间
    # nfp_ass = packing.NFPAssistant(polys,store_nfp=False,get_all_nfp=True,load_history=True)
    nfp_assistant = NewNfpAssistant(dataset_name, allowed_rotation=dataset_allowed_rotation)
    # nfp_ass=None
    # nfp_ass.getDirectNFP(polys[10],polys[12])
    bfl = BottomLeftFill(dataset_width, polygons, vertical=False, NFPAssistant=nfp_assistant)
    print(bfl.polygons)
    bfl.show_all()


if __name__ == '__main__':
    main()
