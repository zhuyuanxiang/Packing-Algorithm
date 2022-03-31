# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> nfp_arc.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 14:41
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
def main(name):
    print(f'Hi, {name}')
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class NFPArc(object):
    """
    基于Arc的NFP计算
    参考文献：Burke E K, Hellier R S R, Kendall G, et al. Irregular packing using the line and arc no-fit polygon[J]. Operations Research, 2010, 58(4-part-1): 948-970.
    """

    def __init__(self):
        pass