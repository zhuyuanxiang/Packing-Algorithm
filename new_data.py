import copy
import csv  # 写csv
import json
import random

from shapely.geometry import mapping
from shapely.geometry import Point
from shapely.geometry import Polygon
from tqdm import tqdm

import pandas as pd  # 读csv
from packing_algorithm.config import targets
from tools.geometry_assitant import Delaunay2D
from tools.geometry_assitant import GeometryAssistant
from tools.geometry_assitant import polygonQuickDecomp
from tools.lp_assistant import LPAssistant
from tools.plt_func import PltFunc
from tools.geometry_functions import GeometryFunctions
from tools.polygon import get_data
from tools.nfp import NFP


def show_lp_result():
    fu = pd.read_csv("record/lp_result.csv")
    _len = fu.shape[0]
    for i in range(_len):
        PltFunc.addPolygon(json.loads(fu["polygon"][i]))
    PltFunc.showPlt()


def add_tuple_poly(_arr, _tuple):
    """
    增加tuple格式的多边形，不添加最后一个
    """
    for i, pt in enumerate(_tuple):
        if i == len(_tuple) - 1:
            break
        _arr.append([pt[0], pt[1]])


def cluster():
    """
    手动聚类
    """
    polys = get_data()
    nfp = NFP(polys[13], polys[1])
    new_nfp = LPAssistant.deleteOnline(nfp.nfp)
    # PltFunc.addPolygon(new_nfp)
    poly0 = copy.deepcopy(polys[13])
    poly1 = copy.deepcopy(polys[1])
    # poly2 = copy.deepcopy(polys[1])
    # print(new_nfp)
    GeometryAssistant.slideToPoint(poly1, [100, 50])
    # GeometryAssistant.slideToPoint(poly2,[100,450])
    # PltFunc.addPolygon(poly0)
    # PltFunc.addPolygon(poly1)
    # PltFunc.addPolygon(poly2)
    final_poly = Polygon(poly0).union(Polygon(poly1))
    print(mapping(final_poly))
    _arr = []
    add_tuple_poly(_arr, mapping(final_poly)["coordinates"][0])
    print(_arr)
    PltFunc.addPolygon(_arr)
    PltFunc.showPlt()  # print(_arr)


def remove_overlap():
    _input = pd.read_csv("record/best_result/blaz_clus.csv")
    polys = json.loads(_input["polys"][4])
    width = 750
    right = GeometryAssistant.getPolysRight(polys)
    print("当前利用率:", 810000 / (right * width))
    PltFunc.addLineColor([[right, 0], [right, width]])
    PltFunc.addLineColor([[0, width], [right, width]])

    # GeoFunc.slidePoly(polys[4],129.20122783641358-131.4932401147777,-3.5)
    # GeoFunc.slidePoly(polys[13],4,-4)
    # GeoFunc.slidePoly(polys[22],0,-3.1130634730287)
    # GeoFunc.slidePoly(polys[16],120.0-119.71600103769902,-3.1130634730287)
    # GeoFunc.slidePoly(polys[6],100.0-99.71600103769902,0)
    # GeoFunc.slidePoly(polys[8],-2.424242424242436,0)

    # PltFunc.showPolys(polys)
    # GeoFunc.slidePoly(polys[3],-2.382,0)
    # PltFunc.addPolygon(polys[20])
    # PltFunc.addPolygon(polys[8])
    # PltFunc.addPolygon(polys[5])
    for i, poly in enumerate(polys):
        # print(i)
        # print(poly)
        PltFunc.addPolygon(poly)  # PltFunc.showPlt(width=700,height=700)
    # print(polys[18])
    PltFunc.showPlt(width=1400, height=1400)  # print(polys[4])  # print(polys[6])

    # PltFunc.showPlt(width=1000,height=1000)  # PltFunc.showPolys(polys)  # print(polys)


def test_nfp():
    data = pd.read_csv("data/dagli_nfp.csv")
    for row in range(data.shape[0]):
        nfp = json.loads(data["nfp"][row])
        GeometryFunctions.slide_polygon(nfp, 300, 300)
        PltFunc.addPolygon(nfp)
        PltFunc.showPlt()


def exterior_record():
    data = pd.read_csv("data/fu_nfp.csv")
    # print(ast.literal_eval(res))
    with open("data/exterior/fu_nfp_exterior.csv", "a+") as csvfile:
        writer = csv.writer(csvfile)
        for row in range(data.shape[0]):
            nfp = json.loads(data["nfp"][row])
            bounds = json.loads(data["bounds"][row])
            GeometryFunctions.slide_polygon(nfp, -nfp[0][0], -nfp[0][1])
            new_NFP = Polygon(nfp)
            exterior_pts = {}
            for x in range(int(bounds[0]), int(bounds[2] + 1) + 1):
                for y in range(int(bounds[1]), int(bounds[3] + 1) + 1):
                    if new_NFP.contains(Point(x, y)) == False:
                        target_key = str(int(x)).zfill(4) + str(int(y)).zfill(4)
                        exterior_pts[target_key] = 1
            writer.writerows([[data["i"][row], data["j"][row], data["oi"][row], data["oj"][row], exterior_pts]])


def add_bound(set_name):
    data = pd.read_csv("data/{}_nfp.csv".format(set_name))
    with open("data/{}_nfp.csv".format(set_name), "a+") as csvfile:
        writer = csv.writer(csvfile)
        for row in range(data.shape[0]):
            for row in range(500, 550):
                nfp = json.loads(data["nfp"][row])
                first_pt = nfp[0]
                new_NFP = Polygon(nfp)
                bound = new_NFP.bounds
                # bound = [bound[0]-first_pt[0],bound[1]-first_pt[1],bound[2]-first_pt[0],bound[3]-first_pt[1]]
                pass

            # vertical_direction = PreProccess().getVerticalDirection(json.loads(data["convex_status"][row]),new_NFP)
            # vertical_direction = json.loads(data["vertical_direction"][row])
            new_vertical_direction = []
            # for item in vertical_direction:
            #     if item == []:
            #         new_vertical_direction.append([[],[]])
            #     else:
            #         new_vertical_direction.append(item)
            writer.writerows([[data["i"][row], data["j"][row], data["oi"][row], data["oj"][row],
                               json.loads(data["new_poly_i"][row]), json.loads(data["new_poly_j"][row]),
                               json.loads(data["nfp"][row]), json.loads(data["convex_status"][row]),
                               new_vertical_direction, bound]])


def add_empty_decom(set_name):
    data = pd.read_csv("data/{}_nfp.csv".format(set_name))
    with open("data/{}_nfp.csv".format(set_name), "a+") as csvfile:
        writer = csv.writer(csvfile)
        for row in range(data.shape[0]):
            writer.writerows([[data["i"][row], data["j"][row], data["oi"][row], data["oj"][row],
                               json.loads(data["new_poly_i"][row]), json.loads(data["new_poly_j"][row]),
                               json.loads(data["nfp"][row]), json.loads(data["convex_status"][row]),
                               json.loads(data["vertical_direction"][row]), json.loads(data["bounds"][row]), []]])


def test_nfp_inter():
    set_name = "fu"
    data = pd.read_csv("data/{}_nfp.csv".format(set_name))
    for k in range(100):
        i, j = random.randint(0, data.shape[0]), random.randint(0, data.shape[0])
        nfp_i, nfp_j = json.loads(data["nfp"][i]), json.loads(data["nfp"][j])
        GeometryFunctions.slide_polygon(nfp_i, random.randint(100, 400), random.randint(100, 400))
        GeometryFunctions.slide_polygon(nfp_j, random.randint(100, 400), random.randint(100, 400))
        nfp1_edges, nfp2_edges = GeometryAssistant.getPolyEdges(nfp_i), GeometryAssistant.getPolyEdges(nfp_j)
        inter_points, intersects = GeometryAssistant.interBetweenNFPs(nfp1_edges, nfp2_edges)
        print(intersects, inter_points)
        PltFunc.addPolygonColor(inter_points)
        PltFunc.addPolygon(nfp_i)
        PltFunc.addPolygon(nfp_j)
        PltFunc.showPlt()


def nfp_decomposition():
    """
    nfp凸分解
    """
    # for target in targets:
    #     data = pd.read_csv("data/{}_nfp.csv".format(target['name']))
    #     if not "bounds" in data:
    #         addBound(target['name'])
    #         print(target['name'])
    error = 0
    for target in targets:
        if not 'trousers' in target['name']: continue
        data = pd.read_csv("data/{}_nfp.csv".format(target['name']))
        with open("data/new/{}_nfp.csv".format(target['name']), "w+") as csvfile:
            writer = csv.writer(csvfile)
            csvfile.write(
                'i,j,oi,oj,new_poly_i,new_poly_j,nfp,convex_status,vertical_direction,bounds,nfp_parts' + '\n')
            for row in range(data.shape[0]):
                nfp = json.loads(data["nfp"][row])
                convex_status = json.loads(data["convex_status"][row])
                first_pt = nfp[0]
                GeometryAssistant.slidePoly(nfp, -first_pt[0], -first_pt[1])
                if 0 in convex_status:
                    parts = copy.deepcopy(polygonQuickDecomp(nfp))
                    area = 0
                    for p in parts:
                        poly = Polygon(p)
                        area = area + poly.area
                    if abs(Polygon(nfp).area - area) > 1e-7:
                        # print('{}:{} NFP凸分解错误，面积相差{}'.format(target['name'],row,Polygon(nfp).area-area))
                        parts = []
                        dt = Delaunay2D()
                        for pt in nfp:
                            dt.addPoint(pt)
                        triangles = copy.deepcopy(dt.exportTriangles())
                        area = 0
                        for p in triangles:
                            poly = []
                            for i in p:
                                poly.append(nfp[i])
                            parts.append(poly)
                            poly = Polygon(poly)
                            area = area + poly.area
                        if abs(Polygon(nfp).area - area) > 1e-7:
                            print('{}:{} NFP凸分解错误，面积相差{}'.format(target['name'], row, Polygon(nfp).area - area))
                            # PltFunc.showPolys(parts+[nfp])
                            error = error + 1
                            parts = []
                else:
                    parts = [nfp]
                writer.writerows([[data["i"][row], data["j"][row], data["oi"][row], data["oj"][row],
                                   json.loads(data["new_poly_i"][row]), json.loads(data["new_poly_j"][row]),
                                   json.loads(data["nfp"][row]), json.loads(data["convex_status"][row]),
                                   json.loads(data["vertical_direction"][row]), json.loads(data["bounds"][row]),
                                   parts]])
    print('总错误次数{}'.format(error))


def test_inter():
    # poly1 = [[600.0, 330.6256882548512], [787.2, 330.6256882548512], [935.6793595845954, 351.3573195832804], [996.6, 347.8256882548512], [1183.8000000000002, 347.8256882548512], [1183.8, 897.2256882548512], [996.5999999999999, 897.2256882548512], [935.6793595845953, 893.6940569264219], [787.2, 914.4256882548511], [600.0, 914.4256882548511], [563.1647058823529, 871.0256882548512], [449.7999999999997, 871.0256882548512], [396.5999999999999, 761.0256882548513], [396.5999999999999, 629.2256882548512], [405.71804511278185, 622.5256882548512], [396.5999999999999, 615.8256882548511], [396.5999999999999, 484.0256882548511], [449.7999999999997, 374.0256882548511], [563.1647058823529, 374.0256882548511]]
    # poly2 = [[600.0, 694.3109894869554], [787.2, 694.3109894869554], [935.6793595845954, 715.0426208153846], [996.6, 711.5109894869554], [1183.8000000000002, 711.5109894869554], [1183.8, 1260.9109894869553], [996.5999999999999, 1260.9109894869553], [935.6793595845953, 1257.379358158526], [787.2, 1278.1109894869553], [600.0, 1278.1109894869553], [563.1647058823529, 1234.7109894869554], [449.7999999999997, 1234.7109894869554], [396.5999999999999, 1124.7109894869554], [396.5999999999999, 992.9109894869554], [405.71804511278185, 986.2109894869553], [396.5999999999999, 979.5109894869553], [396.5999999999999, 847.7109894869552], [449.7999999999997, 737.7109894869552], [563.1647058823529, 737.7109894869552]]
    # poly3 = [[1003.6017161352788, 183.9999999999999], [1090.7662002835198, 196.1704589469519], [1163.6017161352788, 183.9999999999999], [1248.5784569581476, 195.86499232728343], [1323.6017161352788, 183.9999999999999], [1480.0609978315142, 205.84583874224708], [1560.2017161352787, 201.19999999999987], [1601.4134360492003, 208.08627710643918], [1720.2017161352787, 201.19999999999987], [1720.2017161352787, 618.8], [1700.2017161352787, 692.3999999999999], [1512.8950242459432, 681.5416410498935], [1461.1013787617937, 687.608896663751], [1303.6017161352788, 709.5999999999999], [1163.6017161352788, 693.1999999999999], [1023.6017161352788, 709.5999999999999], [983.2017161352787, 661.9999999999999], [873.4017161352788, 666.1999999999999], [820.2017161352787, 556.1999999999999], [800.2017161352787, 482.5999999999999], [836.4017161352788, 455.9999999999999], [836.4017161352788, 422.90386740331485], [820.2017161352787, 410.9999999999999], [800.2017161352787, 337.39999999999986], [853.4017161352788, 227.39999999999986], [963.2017161352787, 231.5999999999999]]
    # edges1, edges2 = GeometryAssistant.getPolyEdges(poly1), GeometryAssistant.getPolyEdges(poly2)
    # inter_points, intersects = GeometryAssistant.inter_between_nfps(edges1, edges2)
    # print(intersects, inter_points)
    # PltFunc.addLine([[1183.8000000000002, 347.8256882548512], [1183.8, 897.2256882548512]])
    # PltFunc.addLine([[996.6, 711.5109894869554], [1183.8000000000002, 711.5109894869554]])
    line1 = [[1183.8000000000002, 347.8256882548512], [1183.8, 897.2256882548512]]
    line2 = [[996.6, 711.5109894869554], [1183.8000000000002, 711.5109894869554]]
    print(GeometryAssistant.line_intersection(line1,
                                              line2))  # PltFunc.addPolygon(poly1)  # PltFunc.addPolygon(poly2)  # PltFunc.addPolygonColor(poly3)  # PltFunc.showPlt(width=2500, height=2500)


def test_best():
    index = 0
    _input = pd.read_csv("record/best_result/fu.csv")
    polys = json.loads(_input["polys"][index])
    width = _input["width"][index]
    length = GeometryAssistant.getPolysRight(polys)

    PltFunc.addLineColor([[length, 0], [length, width]])
    PltFunc.addLineColor([[0, width], [length, width]])
    ratio = _input["total_area"][index] / (width * length)
    print("利用比例:", ratio)
    for poly in polys:
        PltFunc.addPolygon(poly)
    PltFunc.showPlt(width=2000, height=2000)


def get_keys(target):
    """
    对Key预处理
    """
    precision = 10
    data = pd.read_csv("data/{}_nfp.csv".format(target['name']))
    with open("data/new/{}_key.csv".format(target['name']), "w+") as csvfile:
        writer = csv.writer(csvfile)
        csvfile.write('i,j,oi,oj,grid,digital,exterior' + '\n')
        for row in tqdm(range(data.shape[0])):
            nfp = json.loads(data["nfp"][row])
            nfp_parts = json.loads(data["nfp_parts"][row])
            convex_status = json.loads(data["convex_status"][row])
            first_pt = nfp[0]
            GeometryAssistant.slidePoly(nfp, -first_pt[0], -first_pt[1])
            grid = dict()
            exterior = dict()
            digital = dict()
            for x in range(-500, 500, precision):
                for y in range(-500, 500, precision):
                    if not GeometryAssistant.boundsContain(Polygon(nfp).bounds, [x, y]):
                        continue
                    grid_key = str(int(x / precision)).zfill(5) + str(int(y / precision)).zfill(5)
                    further_calc = False
                    if not Polygon(nfp).contains(Point([x, y])):
                        dist = Point([x, y]).distance(Polygon(nfp))
                        if dist > 7.5:
                            grid[grid_key] = -1
                        else:
                            further_calc = True
                    else:
                        depth = GeometryAssistant.get_point_nfp_pd([x, y], convex_status, nfp, 0.000001)
                        if depth > 7.5:
                            grid[grid_key] = depth
                        else:
                            further_calc = True
                    if further_calc:
                        for m in range(x - 5, x + 5):
                            for n in range(y - 5, y + 5):
                                digital_key = str(int(m)).zfill(6) + str(int(n)).zfill(6)
                                if digital_key in exterior.keys() or digital_key in digital.keys():
                                    continue
                                if not Polygon(nfp).contains(Point([m, n])):
                                    exterior[digital_key] = 1
                                else:
                                    depth = GeometryAssistant.get_point_nfp_pd([m, n], convex_status, nfp, 0.000001)
                                    digital[digital_key] = depth
            writer.writerows([[data["i"][row], data["j"][row], data["oi"][row], data["oj"][row], json.dumps(grid),
                               json.dumps(digital), json.dumps(exterior)]])


if __name__ == '__main__':
    # removeOverlap()
    # testBest()
    # addEmptyDecom("swim")
    # testInter()
    # testNFP()
    # testNFPInter()
    # print(str(int(-1005/10)*10).zfill(5))
    # addBound()
    # PreProccess(14)
    # nfpDecomposition()
    # removeOverlap()
    # for target in targets:
    #     if target['name'] in ['shapes0']:
    #         getKeys(target)
    pass
