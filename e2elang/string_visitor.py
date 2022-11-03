from itertools import chain
from e2elang.opcode import E2EBiOp, E2EUnOp, E2EVar

from floatconvert.float_converter import FloatConverter
from exprtree.visitor import Visitor


class StringVisitor(Visitor):

    def __init__(self, floatEncoder: FloatConverter, mode="prefix"):
        super().__init__()
        self.floatEncoder = floatEncoder
        self.binary_op_map = {
            E2EBiOp.add: "add",
            E2EBiOp.mul: "mul",
            E2EBiOp.sub: "sub"
        }
        self.unary_op_map = {
            E2EUnOp.abs: "abs",
            E2EUnOp.atan: "atan",
            E2EUnOp.cos: "cos",
            E2EUnOp.exp: "exp",
            E2EUnOp.inv: "inv",
            E2EUnOp.log: "log",
            E2EUnOp.sin: "sin",
            E2EUnOp.sqr: "sqr",
            E2EUnOp.sqrt: "sqrt",
            E2EUnOp.tan: "tan"
        }
        var = list(E2EVar)
        self.var_map = dict([(v, f"x{v.value}") for v in var])

        assert mode in ["prefix", "postfix"]
        self.mode = mode

    def visit_binary_op(self, ty, left, right):
        if self.mode == "prefix":
            return chain([self.binary_op_map[ty]], left, right)
        else:
            return chain(left, right, [self.binary_op_map[ty]])

    def visit_unary_op(self, ty, left):
        if self.mode == "prefix":
            return chain([self.unary_op_map[ty]], left)
        else:
            return chain(left, [self.unary_op_map[ty]])

    def visit_var(self, ty):
        return [self.var_map[ty]]

    def visit_float(self, ty):
        return [self.floatEncoder.encode(ty)]

    def tokens(self):
        return list(chain(self.binary_op_map.values(),
                          self.unary_op_map.values(),
                          self.var_map.values(),
                          self.floatEncoder.tokens))
