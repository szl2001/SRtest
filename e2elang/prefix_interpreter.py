from e2elang.opcode import binary_op_map, unary_op_map, var_map
from exprtree.expr import Node

def reverse_map(m):
    return {v: k for k, v in m.items()}


rev_biop = reverse_map(binary_op_map)
rev_unop = reverse_map(unary_op_map)
rev_var = reverse_map(var_map)

# Convert to ExprTree, then convert to sympy expression
class PrefixIntepreter:

    def __init__(self, floatDecoder):
        self.floatDecoder = floatDecoder


    def parse_prefix(self, strs):
        if len(strs) == 0:
            return None

        ty = strs.pop(0)
        if ty in rev_biop:
            lchild = self.parse_prefix(strs)
            rchild = self.parse_prefix(strs)
            assert lchild is not None
            assert rchild is not None
            return Node(rev_biop[ty], lchild, rchild)
        elif ty in rev_unop:
            lchild = self.parse_prefix(strs)
            assert lchild is not None
            return Node(rev_unop[ty], lchild)
        elif ty in rev_var:
            return Node(rev_var[ty])
        else:
            return Node(self.floatDecoder.decode([ty]))
