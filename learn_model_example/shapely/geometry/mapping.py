# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> mapping.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-06 17:50
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from shapely.geometry import mapping
from shapely.geometry import shape


class GeoThing(object):
    def __init__(self, d):
        self.__geo_interface__ = d


def main(name):
    print(f'Hi, {name}')

    data = {"type": "Point", "coordinates": (0.0, 0.0)}
    geom = shape(data)
    print("type=", geom.geom_type, ",co-ordinates=", list(geom.coords))

    thing = GeoThing(data)
    geom = shape(thing)
    print("type=", geom.geom_type, ",co-ordinates=", list(geom.coords))

    # The GeoJSON-like mapping of a geometric object can be obtained using shapely.geometry.mapping().
    map = mapping(thing)
    print("type=", map['type'], ",co-ordinates=", map['coordinates'])
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
