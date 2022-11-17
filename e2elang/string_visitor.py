from itertools import chain
from e2elang.opcode import binary_op_map, unary_op_map, var_map
from floatconvert.float_converter import FloatConverter
from exprtree.visitor import Visitor


class StringVisitor(Visitor):

    def __init__(self, floatEncoder: FloatConverter, mode="prefix"):
        super().__init__()
        self.floatEncoder = floatEncoder

        assert mode in ["prefix", "postfix"]
        self.mode = mode

    def visit_binary_op(self, ty, left, right):
        if self.mode == "prefix":
            return chain([binary_op_map[ty]], left, right)
        else:
            return chain(left, right, [binary_op_map[ty]])

    def visit_unary_op(self, ty, left):
        if self.mode == "prefix":
            return chain([unary_op_map[ty]], left)
        else:
            return chain(left, [unary_op_map[ty]])

    def visit_var(self, ty):
        return [var_map[ty]]

    def visit_float(self, ty):
        return [self.floatEncoder.encode(ty)]

    def tokens(self):
        return list(chain(binary_op_map.values(),
                          unary_op_map.values(),
                          var_map.values(),
                          self.floatEncoder.tokens()))
