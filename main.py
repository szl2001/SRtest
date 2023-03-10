import numpy as np
from data_gen import GenConfig, TreeGen
from e2elang.opcode import E2EBiOp, E2EUnOp, E2EVar
from e2elang.string_visitor import StringVisitor
from e2elang.sympy_vistor import SympyVisitor
from floatconvert.fp16_converter import FP16Converter
from points_gen import PointsGen
import pickle
import pandas as pd
from e2elang.opcode import real_biop_map, real_unop_map, const_map
from constants import G,c,epsilon0,g,h,k,qe,mew0,NA,F,Bohr

from multiprocessing import Pool

def test(field):
    feature = pd.read_csv(f'real/feature/{field}_fea.csv')
    feature = feature.set_index('Unnamed: 0',drop=True).T
    bi_dis, un_dis, sp_str_dis, var_dis = get_dis(feature)
    bi_coff, bi_max, un_max, ave_biop = get_op_num(feature)
    cfg = GenConfig(
        list(E2EVar),
        bi_dis, un_dis, sp_str_dis, bi_coff, bi_max, ave_biop, un_max)
    print(bi_dis, un_dis, sp_str_dis, cfg)

def generate_expr(num: int, field):
    rng = np.random.default_rng(3245)
    feature = pd.read_csv(f'real/feature/{field}_fea.csv')
    feature = feature.set_index('Unnamed: 0',drop=True).T
    bi_dis, un_dis, sp_str_dis, var_dis = get_dis(feature)
    bi_coff, bi_max, un_max = get_op_num(feature)
    cfg = GenConfig(
        list(E2EVar),
        bi_dis, un_dis, sp_str_dis, bi_coff, bi_max, un_max)

    tree_generator = TreeGen(cfg, rng)
    points_generator = PointsGen(rng)
    fp16_converter = FP16Converter()
    str_vis = StringVisitor(floatEncoder=fp16_converter)
    sym_vis = SympyVisitor()

    datasets = []
    for _ in range(num):
        input_dim = rng.integers(1, 10)
        input_dim = 10
        tree = tree_generator.sample_tree(input_dim)
        # print(tree)
        # strs = str_vis.visit(tree)
        # print(" ".join(list(strs)))

        sym_expr = sym_vis.visit(tree)
        points = [points_generator.mk_points(200, sym_expr) for _ in range(10)]
        # print(points)

        datasets.append((tree, points))
    return datasets


def worker(task_id):
    data = generate_expr(1000)
    with open(f"data{task_id}.pkl", "wb") as f:
        pickle.dump(data, f)

def get_dis(feature):
    biop_dis = dict()
    for op in E2EBiOp.__members__.items():
        biop_dis[op[1]] = 0
    unop_dis = dict()
    for op in E2EUnOp.__members__.items():
        unop_dis[op[1]] = 0

    fre = eval(feature['fre'][0])
    constant = {G,c,epsilon0,g,h,k,qe,mew0,Bohr,NA,F}
    const_dis = dict.fromkeys(constant,0)

    for op in fre:
        if op in real_biop_map:
            biop_dis[real_biop_map[op]] = fre[op]
        elif op in real_unop_map:
            unop_dis[real_unop_map[op]] = fre[op]
        elif op in const_map:
            const_dis[const_map[op]] = fre[op]
        else:
            raise ValueError("unknown op or const!")
    return biop_dis, unop_dis, const_dis, eval(feature['vars_num'][0])

def get_op_num(feature):

    biop_coff = eval(feature['biop_coff'][0])
    biop_len = eval(feature['biop'][0])
    ave_biop = sum([i*biop_len[i] for i in range(0, len(biop_len))])
    unop_len = eval(feature['unop'][0])

    return max(biop_coff), len(biop_len) - 1, len(unop_len) - 1, ave_biop

def main():
    pool = Pool(32)
    pool.map(worker, range(100))
    pool.close()
    pool.join()


if __name__ == "__main__":
    #main()
    test("bio")
