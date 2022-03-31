# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> line_string.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-06 18:01
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from datetime import datetime

from shapely.geometry import LineString
from shapely.geometry import mapping


def main(name):
    print(f'Hi, {name}', datetime.now())
    line1 = LineString([(0, 0), (1, 1)])
    line2 = LineString([(0, 1), (1, 0)])
    line3 = LineString([(0, 0), (1, 1)])

    print("area=", line1.area)
    print("length=", line1.length)
    print("bounds=", line1.bounds)
    print("coordinates=", list(line1.coords))
    point_of_intersection2 = line1.intersection(line2)
    print(point_of_intersection2)
    print(mapping(point_of_intersection2)['coordinates'][0])
    point_of_intersection3 = line1.intersection(line3)
    print(point_of_intersection3)
    print(mapping(point_of_intersection3)['coordinates'][0])

    print("line1.intersection(line2)=", line1.intersection(line2))
    print("line1.intersection(line3)=", line1.intersection(line3))
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
