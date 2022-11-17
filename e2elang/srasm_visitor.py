from itertools import chain
from e2elang.opcode import E2EBiOp, E2EUnOp, E2EVar
from e2elang.opcode import binary_op_map, unary_op_map, var_map
from floatconvert.float_converter import FloatConverter

# Maybe we need a Reverse State Monad?


class SRasmVisitor:

    def __init__(self, floatEncoder: FloatConverter):
        super().__init__()
        self.floatEncoder = floatEncoder

    def visit(self, node):
        vars = []
        nodes = []

        def helper(node):
            if node is None:
                return
            if isinstance(node.ty, E2EVar):
                if node.ty not in vars:
                    vars.append(node.ty)
            else:
                helper(node.lchild)
                helper(node.rchild)
                nodes.append(node)

        helper(node)

        def getId(n):
            if isinstance(n.ty, E2EVar):
                return vars.index(n.ty)
            else:
                return nodes.index(n) + len(vars)

        instrs = []
        for v in vars:
            instrs.append((var_map[v], -1, -1))
        for n in nodes:
            ty = n.ty
            if isinstance(ty, E2EBiOp):
                instr = (binary_op_map[ty], getId(n.lchild), getId(n.rchild))
            elif isinstance(ty, E2EUnOp):
                leftId = getId(n.lchild)
                instr = (unary_op_map[ty], leftId, leftId)
            elif isinstance(ty, E2EVar):
                assert False, "VarNode should not exist here"
            else:
                instr = (self.floatEncoder.encode(ty), -1, -1)

            instrs.append(instr)

        return instrs

    def tokens(self):
        return list(chain(binary_op_map.values(),
                          unary_op_map.values(),
                          var_map.values(),
                          self.floatEncoder.tokens()))
