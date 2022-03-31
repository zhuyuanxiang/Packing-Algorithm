# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> output_func.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-09-06 18:28
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import time
from datetime import datetime


def main(name):
    print(f'Hi, {name}', datetime.now())
    pass
    
if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)


class OutputFunc(object):
    """输出不同颜色字体"""

    @staticmethod
    def outputWarning(prefix, _str):
        """输出红色字体"""
        _str = prefix + str(time.strftime("%H:%M:%S", time.localtime())) + " " + str(_str)
        print("\033[0;31m", _str, "\033[0m")

    @staticmethod
    def outputAttention(prefix, _str):
        """输出绿色字体"""
        _str = prefix + str(time.strftime("%H:%M:%S", time.localtime())) + " " + str(_str)
        print("\033[0;32m", _str, "\033[0m")

    @staticmethod
    def outputInfo(prefix, _str):
        """输出浅黄色字体"""
        _str = prefix + str(time.strftime("%H:%M:%S", time.localtime())) + " " + str(_str)
        print("\033[0;33m", _str, "\033[0m")