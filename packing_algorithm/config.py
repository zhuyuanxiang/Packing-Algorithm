# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> config.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 10:59
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
import logging

target_clus_index_00 = {"index": 0, "name": "blaz", "scale": 50, "allowed_rotation": 2, "width": 750}
target_clus_index_01 = {"index": 1, "name": "shapes2_clus", "scale": 1, "allowed_rotation": 2, "width": 750}
target_clus_index_02 = {"index": 2, "name": "shapes0", "scale": 20, "allowed_rotation": 1, "width": 800}
target_clus_index_03 = {"index": 3, "name": "marques", "scale": 10, "allowed_rotation": 2, "width": 1040}
target_clus_index_04 = {"index": 4, "name": "mao", "scale": 1, "allowed_rotation": 4, "width": 2550}
target_clus_index_05 = {"index": 5, "name": "shirts", "scale": 20, "allowed_rotation": 2, "width": 800}
target_clus_index_06 = {"index": 6, "name": "albano", "scale": 0.2, "allowed_rotation": 2, "width": 980}
target_clus_index_07 = {"index": 7, "name": "shapes1", "scale": 20, "allowed_rotation": 2, "width": 800}
target_clus_index_08 = {"index": 8, "name": "dagli_clus", "scale": 20, "allowed_rotation": 2, "width": 1200}
target_clus_index_09 = {"index": 9, "name": "jakobs1_clus", "scale": 20, "allowed_rotation": 4, "width": 800}
target_clus_index_10 = {"index": 10, "name": "trousers", "scale": 10, "allowed_rotation": 2, "width": 790}
target_clus_index_11 = {"index": 11, "name": "jakobs2_clus", "scale": 10, "allowed_rotation": 4, "width": 700}
target_clus_index_12 = {"index": 12, "name": "swim_clus", "scale": 0.2, "allowed_rotation": 2, "width": 1150.4}
target_clus_index_13 = {"index": 13, "name": "fu", "scale": 20, "allowed_rotation": 4, "width": 760}
target_clus_index_14 = {"index": 14, "name": "dagli", "scale": 20, "allowed_rotation": 2, "width": 1200}
target_clus_index_15 = {"index": 15, "name": "dighe1", "scale": 10, "allowed_rotation": 1, "width": 1000}
target_clus_index_16 = {"index": 16, "name": "dighe2", "scale": 10, "allowed_rotation": 1, "width": 1000}

targets_index_00 = {"index": 0, "name": "albano", "scale": 0.2, "allowed_rotation": 2, "width": 980}
targets_index_01 = {"index": 1, "name": "blaz", "scale": 50, "allowed_rotation": 2, "width": 750}
targets_index_02 = {"index": 2, "name": "dagli", "scale": 20, "allowed_rotation": 2, "width": 1200}
targets_index_03 = {"index": 3, "name": "dighe1", "scale": 10, "allowed_rotation": 1, "width": 1000}
targets_index_04 = {"index": 4, "name": "dighe2", "scale": 10, "allowed_rotation": 1, "width": 1000}
targets_index_05 = {"index": 5, "name": "fu", "scale": 20, "allowed_rotation": 4, "width": 760}
targets_index_06 = {"index": 6, "name": "jakobs1", "scale": 20, "allowed_rotation": 4, "width": 800}
targets_index_07 = {"index": 7, "name": "jakobs2", "scale": 10, "allowed_rotation": 4, "width": 700}
targets_index_08 = {"index": 8, "name": "mao", "scale": 1, "allowed_rotation": 4, "width": 2550}
targets_index_09 = {"index": 9, "name": "marques", "scale": 10, "allowed_rotation": 4, "width": 1040}
targets_index_10 = {"index": 10, "name": "shapes0", "scale": 20, "allowed_rotation": 1, "width": 800}
targets_index_11 = {"index": 11, "name": "shapes1", "scale": 20, "allowed_rotation": 2, "width": 800}
targets_index_12 = {"index": 12, "name": "shirts", "scale": 20, "allowed_rotation": 2, "width": 800}
targets_index_13 = {"index": 13, "name": "swim", "scale": 0.2, "allowed_rotation": 2, "width": 1150.4}
targets_index_14 = {"index": 14, "name": "trousers", "scale": 10, "allowed_rotation": 2, "width": 790}
targets_index_15 = {"index": 15, "name": "blaz_clus", "scale": 50, "allowed_rotation": 2, "width": 750}
targets_index_16 = {"index": 16, "name": "dagli_clus", "scale": 20, "allowed_rotation": 2, "width": 1200}

targets_clus = [target_clus_index_00, target_clus_index_01, target_clus_index_02, target_clus_index_03,
                target_clus_index_04, target_clus_index_05, target_clus_index_06, target_clus_index_07,
                target_clus_index_08, target_clus_index_09, target_clus_index_10, target_clus_index_11,
                target_clus_index_12, target_clus_index_13, target_clus_index_14, target_clus_index_15,
                target_clus_index_16]
targets = [targets_index_00, targets_index_01, targets_index_02, targets_index_03, targets_index_04, targets_index_05,
           targets_index_06, targets_index_07, targets_index_08, targets_index_09, targets_index_10, targets_index_11,
           targets_index_12, targets_index_13, targets_index_14, targets_index_15, targets_index_16]

# cite:An algorithm for the strip packing problem using collision free region and exact fitting placement.pdf
# ToDo: 将几个数据集合并
datasets = [{"index": 0, "name": "albano", "scale": 0.2, "allowed_rotation": 2, "width": 980},
            {"index": 1, "name": "blaz", "scale": 10, "allowed_rotation": 2, "width": 150},
            {"index": 2, "name": "dagli", "scale": 20, "allowed_rotation": 2, "width": 1200},
            {"index": 3, "name": "dighe1", "scale": 10, "allowed_rotation": 1, "width": 1000},
            {"index": 4, "name": "dighe2", "scale": 10, "allowed_rotation": 1, "width": 1000},
            {"index": 5, "name": "fu", "scale": 20, "allowed_rotation": 4, "width": 760},
            {"index": 6, "name": "jakobs1", "scale": 20, "allowed_rotation": 4, "width": 800},
            {"index": 7, "name": "jakobs2", "scale": 10, "allowed_rotation": 4, "width": 700},
            {"index": 8, "name": "mao", "scale": 1, "allowed_rotation": 4, "width": 2550},
            {"index": 9, "name": "marques", "scale": 10, "allowed_rotation": 2, "width": 1040},
            {"index": 10, "name": "shapes0", "scale": 20, "allowed_rotation": 1, "width": 800},
            {"index": 11, "name": "shapes1", "scale": 20, "allowed_rotation": 2, "width": 800},
            {"index": 12, "name": "shapes2", "scale": 1, "allowed_rotation": 2, "width": 750},
            {"index": 13, "name": "shirts", "scale": 20, "allowed_rotation": 2, "width": 800},
            {"index": 14, "name": "swim", "scale": 0.2, "allowed_rotation": 2, "width": 1150.4},
            {"index": 15, "name": "trousers", "scale": 10, "allowed_rotation": 2, "width": 790},
            {"index": 16, "name": "blaz_clus", "scale": 50, "allowed_rotation": 2, "width": 750},
            {"index": 17, "name": "dagli_clus", "scale": 20, "allowed_rotation": 2, "width": 1200}]

bias = 0.000001


def main(name):
    print(f'Hi, {name}')
    pass


if __name__ == "__main__":
    __author__ = 'zYx.Tom'
    main(__author__)
log_format = "%(asctime)s %(filename)s-line%(lineno)d:%(levelname)s:%(message)s"
date_format = "%d-%M-%Y %H:%M:%S"


def log_config():
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)