# from multiprocessing import Pool
from tools.nfp import NFP


def getNFP(poly1, poly2):  # 这个函数必须放在class外面否则多进程报错
    nfp = NFP(poly1, poly2).nfp
    return nfp


