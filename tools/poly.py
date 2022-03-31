# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> poly.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 14:41
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""


class Poly(object):
    """
    用于后续的Poly对象
    """

    def __init__(self, num, poly, allowed_rotation):
        self.num = num
        self.poly = poly
        self.cur_poly = poly
        self.allowed_rotation = [0, 180]
