import numpy as np
from numpy.random import RandomState
from sympy import lambdify

class PointsGen:

    def __init__(self, rng: RandomState):
        self.rng = rng

    def mk_points(self, num: int, sympy_expr):

        free_vars = list(sympy_expr.free_symbols)
        # sort variables by name
        free_vars = sorted(free_vars, key=lambda v: int(v.name[1:]))
        
        inps = self.rng.rand(len(free_vars), num)
        f = lambdify(free_vars, sympy_expr, "numpy")
        out = f(*inps)

        points = np.row_stack((out, inps))
        return points
