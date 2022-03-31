"""
本文件包括与DRL训练和测试的相关辅助函数
"""
import json
import multiprocessing
import os
import time
from multiprocessing import Pool
from shutil import copyfile

import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from tqdm import tqdm
from init_seq import InitSeq

from packing_algorithm.config import targets
from packing_algorithm.tools import BottomLeftFill
from tools.geometry_functions import GeometryFunctions
from tools.newnfpassistant import NewNfpAssistant
from tools.nfp_assistant import NFPAssistant
from tools.plt_func import PltFunc
from tools.poly_list_processor import PolyListProcessor
from tools.sequence import GA


def get_nfp(polys, save_name, index):
    # print('record/{}/{}.csv'.format(save_name,index))
    NFPAssistant(polys, get_all_nfp=True, store_nfp=True, store_path='record/{}/{}.csv'.format(save_name, index))


def get_all_nfp(data_source, save_name):
    os.makedirs('record/{}'.format(save_name))
    data = np.load(data_source, allow_pickle=True)
    p = Pool()
    for index, polys in enumerate(data):
        p.apply_async(get_nfp, args=(polys, save_name, index))
    p.close()
    p.join()


def nfp_check(dataset_name, new_name):
    os.makedirs('record/{}'.format(new_name))
    print('Files with wrong NFPs are listed below:')
    xy = np.load('{}_xy.npy'.format(dataset_name), allow_pickle=True)
    vec = np.load('{}.npy'.format(dataset_name), allow_pickle=True)
    xy_new = []
    vec_new = []
    index_new = 0
    for i, polys in enumerate(tqdm(xy)):
        valid = False
        nfp_path = 'record/{}/{}.csv'.format(dataset_name, i)
        if not os.path.exists(nfp_path):
            continue
        df = pd.read_csv(nfp_path, header=None)
        try:
            for line in range(df.shape[0]):
                nfp = json.loads(df[2][line])
                differ = Polygon([[-1000, -1000], [3000, -1000], [3000, 3000], [-1000, 3000]]).difference(Polygon(nfp))
            valid = True
        except:
            print(i)
        if valid:
            xy_new.append(xy[i])
            vec_new.append(vec[i])
            copyfile('record/{}/{}.csv'.format(dataset_name, i), 'record/{}/{}.csv'.format(new_name, index_new))
            index_new = index_new + 1
    print('数据集有效容量 {}'.format(len(vec_new)))
    np.save('{}_xy.npy'.format(new_name), np.array(xy_new))
    np.save('{}.npy'.format(new_name), np.array(vec_new))


def blf_with_sequence(test_path, width, seq_path=None, ga_algo=False):
    if seq_path is not None:
        # ToDo: 取出文件失败的问题处理
        f = open(seq_path, 'r')
        seqs = f.readlines()
    data = np.load(test_path, allow_pickle=True)
    test_name = test_path.split('_xy')[0]
    height = []
    # ToDo: 将遗传算法从 BLF 中摘出
    if ga_algo:
        p = Pool()
    multi_res = []
    for i, line in enumerate(tqdm(data)):
        polys_final = []
        if seq_path is not None:  # 指定序列
            seq = seqs[i].split(' ')
        else:  # 随机序列
            seq = np.array(range(len(line)))
            np.random.shuffle(seq)
        for j in range(len(line)):
            if seq_path is not None:
                index = int(seq[j])
            else:
                index = seq[j]
            polys_final.append(line[index])
        nfp_asst = NFPAssistant(polys_final, load_history=True, history_path='record/{}/{}.csv'.format(test_name, i))
        # nfp_asst=None
        if ga_algo:  # 遗传算法
            polys_GA = PolyListProcessor.getPolyObjectList(polys_final, [0])
            multi_res.append(p.apply_async(GA, args=(width, polys_GA, nfp_asst)))
        else:
            blf = BottomLeftFill(width, polys_final, NFPAssistant=nfp_asst)
            # blf.showAll()
            height.append(blf.get_length())
    if ga_algo:
        p.close()
        p.join()
        for res in multi_res:
            height.append(res.get().global_lowest_length)
    return height


def get_benchmark(source, width=760):
    random = blf_with_sequence(source, width)
    random = np.array(random)
    # np.savetxt('random.CSV',random)
    print('random...OK', np.mean(random))

    # 与现有启发式比较
    data = np.load(source, allow_pickle=True)
    test_name = source.split('_xy')[0]
    height = []
    for i, line in enumerate(tqdm(data)):
        nfp_path = 'record/{}/{}.csv'.format(test_name, i)
        min_height = InitSeq(width, line, nfp_load=nfp_path).get_best()
        height.append(min_height)
    decrease = np.array(height)
    print('heuristic...OK', np.mean(decrease))

    # predict=blf_with_sequence(source,seq_path='outputs/0406/fu1500/sequence-0.csv')  # predict=np.array(predict)  #
    # np.savetxt('predict.CSV',predict)  # print('predict...OK')

    # ga=blf_with_sequence(source,decrease=None,GA_algo=True)  # if single:  print('GA',ga)  # else:  #
    # ga=np.array(ga)  #     np.savetxt('GA.CSV',ga)  #     print('GA...OK')


def get_all_init():
    # 获取所有数据集的最优初始解
    for index, target in enumerate(targets):
        set_name = target["name"]
        width = target["width"]
        scale = target["scale"]
        if set_name not in ['trousers']: continue
        print(width)
        # 加载原始数据并缩放
        df = pd.read_csv("data/" + set_name + ".csv")
        polygons = []
        polys_type = []
        for i in range(0, df.shape[0]):
            for j in range(0, df['num'][i]):
                polys_type.append(i)
                poly = json.loads(df['polygon'][i])
                GeometryFunctions.normal_data(poly, scale)
                polygons.append(poly)
        total_area = 0
        for poly in polygons:
            total_area = total_area + Polygon(poly).area
        allowed_rotation = target["allowed_rotation"]
        allowed_rotation_list = np.array(range(allowed_rotation)).tolist()
        nfp_ass = NewNfpAssistant(set_name, allowed_rotation=allowed_rotation)
        ratio, best_criteria, polys, indexs = InitSeq(width, polygons, nfp_asst=nfp_ass).get_best()
        polys_final = [[]] * len(polys)
        for i in range(len(indexs)):
            polys_final[indexs[i]] = polys[i]
        PltFunc.showPolys(polys_final)
        with open("record/lp_initial.csv", "a+") as f:
            result = str([index + 110, set_name, 0.1, 1, str(allowed_rotation_list),
                          set_name + '较优初始解({:.2%},{})'.format(ratio, best_criteria), width, total_area,
                          max(polys_type) + 1, str(polys_type), str([0] * len(polygons)), str(polys_final)])
            result = result[1:len(result) - 1]
            f.write(result)
            f.write('\n')


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', True)
    start = time.time()
    # GenerateData_vector.export_dataset(4,'dighe1')
    # GenerateData_vector.export_dataset(5,'dighe2')
    # nfp_check('fu999_val','reg9999_val')
    # GenerateData_vector.generate_test_data('fu999_val',999)
    # get_all_nfp('fu999_val_xy.npy','fu999_val')
    # GenerateData_vector.generate_test_data('reg10000',10000)
    # get_all_nfp('reg10000_xy.npy','reg10000')
    # get_benchmark('reg2379_xy.npy')
    get_all_init()
    # data=np.load('fu_val_xy.npy',allow_pickle=True)[0]
    # InitSeq(760,data,nfp_load='record/fu_val/0.csv').get_best()
    # InitSeq(760,data,nfp_load='record/fu_10_val/0.csv').get_best()
    end = time.time()
    print('Running time:', end - start)
