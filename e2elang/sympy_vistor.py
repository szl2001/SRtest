from e2elang.opcode import E2EBiOp, E2EUnOp, E2EVar
from exprtree.visitor import Visitor

import sympy as sp


class SympyVisitor(Visitor):

    def __init__(self):
        super().__init__()

        var = list(E2EVar)
        self.var_map = dict([(v, sp.Symbol(f"x{v.value}")) for v in var])


    def visit_binary_op(self, ty, left, right):
        if ty == E2EBiOp.add:
            return left + right
        elif ty == E2EBiOp.mul:
            return left * right
        elif ty == E2EBiOp.sub:
            return left - right
        elif ty == E2EBiOp.div:
            return left / right
        elif ty == E2EBiOp.pow:
            return left ** right
        else:
            raise NotImplementedError(f"Unknown Binary Opcode: {ty}")

    def visit_unary_op(self, ty, left):
        if ty == E2EUnOp.Abs:
            return sp.Abs(left)
        elif ty == E2EUnOp.exp:
            return sp.exp(left)
        elif ty == E2EUnOp.sqrt:
            return sp.sqrt(left)
        elif ty == E2EUnOp.inv:
            return 1 / left
        elif ty == E2EUnOp.ln:
            return sp.log(left)
        elif ty == E2EUnOp.lg:
            return sp.log(left, 10)
        elif ty == E2EUnOp.sin:
            return sp.sin(left)
        elif ty == E2EUnOp.cos:
            return sp.cos(left)
        elif ty == E2EUnOp.tan:
            return sp.tan(left)
        elif ty == E2EUnOp.asin:
            return sp.asin(left)
        elif ty == E2EUnOp.acos:
            return sp.acos(left)
        elif ty == E2EUnOp.atan:
            return sp.atan(left)
        elif ty == E2EUnOp.sinh:
            return sp.sinh(left)
        elif ty == E2EUnOp.cosh:
            return sp.cosh(left)
        elif ty == E2EUnOp.tanh:
            return sp.tanh(left)
        else:
            raise NotImplementedError(f"Unknown Unary Opcode: {ty}")

    def visit_var(self, ty):
        return self.var_map[ty]

    def visit_float(self, ty):
        return ty