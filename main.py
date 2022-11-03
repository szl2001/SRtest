import numpy as np
from data_gen import GenConfig, TreeGen
from e2elang.opcode import E2EBiOp, E2EUnOp, E2EVar
from e2elang.string_visitor import StringVisitor
from e2elang.sympy_vistor import SympyVisitor
from floatconvert.fp16_converter import FP16Converter
from points_gen import PointsGen
import pickle

from multiprocessing import Pool

def generate_expr(num: int):
    rng = np.random.default_rng()
    cfg = GenConfig(
        list(E2EVar),
        {E2EBiOp.add: 1, E2EBiOp.sub: 1, E2EBiOp.mul: 1},
        {E2EUnOp.inv: 25, E2EUnOp.abs: 5, E2EUnOp.sqr: 15,
         E2EUnOp.sqrt: 15, E2EUnOp.sin: 5, E2EUnOp.cos: 5,
         E2EUnOp.tan: 1, E2EUnOp.atan: 1, E2EUnOp.log: 1,
         E2EUnOp.exp: 5})

    tree_generator = TreeGen(cfg, rng)
    points_generator = PointsGen(rng)
    fp16_converter = FP16Converter()
    str_vis = StringVisitor(floatEncoder=fp16_converter)
    sym_vis = SympyVisitor()

    datasets = []
    for _ in range(num):
        input_dim = rng.integers(1, 10)
        tree = tree_generator.sample_tree(input_dim)
        # print(tree)

        # strs = str_vis.visit(tree)
        # print(" ".join(list(strs)))

        sym_expr = sym_vis.visit(tree)
        num_points = 200
        points = [points_generator.mk_points(
            num_points, sym_expr) for _ in range(10)]
        # print(points)

        datasets.append((tree, points))
    return datasets

def worker(task_id):
    data = generate_expr(5)
    with open(f"data{task_id}.pkl", "wb") as f:
        pickle.dump(data, f)

def main():
    pool = Pool(32)
    pool.map(worker, range(10))
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
