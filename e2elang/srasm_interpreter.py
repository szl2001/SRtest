# Interpret step by step
from e2elang.opcode import E2EBiOp, E2EUnOp
from e2elang.opcode import binary_op_map, unary_op_map, var_map
import numpy as np

from exprtree.expr import Node


def reverse_map(m):
    return {v: k for k, v in m.items()}


rev_biop = reverse_map(binary_op_map)
rev_unop = reverse_map(unary_op_map)
rev_var = reverse_map(var_map)


class SRasmInterpreter:

    def __init__(self, floatDecoder):
        self.floatDecoder = floatDecoder

    def execute_one(self, instr):

        def dispatch_biop(op, lchild, rchild):
            if op == E2EBiOp.add:
                return lchild + rchild
            elif op == E2EBiOp.mul:
                return lchild * rchild
            elif op == E2EBiOp.sub:
                return lchild - rchild
            elif op == E2EBiOp.div:
                return lchild/rchild
            elif op == E2EBiOp.pow:
                return np.power(lchild, rchild)

        def dispatch_unop(op, lchild):
            if op == E2EUnOp.abs:
                return np.abs(lchild)
            elif op == E2EUnOp.exp:
                return np.exp(lchild)
            elif op == E2EUnOp.inv:
                return 1 / lchild
            elif op == E2EUnOp.sqrt:
                return np.sqrt(lchild)
            elif op == E2EUnOp.lg:
                return np.log10(lchild)
            elif op == E2EUnOp.ln:
                return np.log(lchild)
            elif op == E2EUnOp.sin:
                return np.sin(lchild)
            elif op == E2EUnOp.cos:
                return np.cos(lchild)
            elif op == E2EUnOp.tan:
                return np.tan(lchild)
            elif op == E2EUnOp.asin:
                return np.arcsin(lchild)
            elif op == E2EUnOp.acos:
                return np.arccos(lchild)
            elif op == E2EUnOp.atan:
                return np.arctan(lchild)
            elif op == E2EUnOp.sinh:
                return np.sinh(lchild)
            elif op == E2EUnOp.cosh:
                return np.cosh(lchild)
            elif op == E2EUnOp.tanh:
                return np.tanh(lchild)

        op = instr[0]
        if op in rev_biop:
            val = dispatch_biop(rev_biop[op],
                                self.env[instr[1]],
                                self.env[instr[2]])
        elif op in rev_unop:
            assert instr[1] == instr[2]
            val = dispatch_unop(rev_unop[op], self.env[instr[1]])
        elif op in rev_var:
            idx = rev_var[op].value
            # print(idx)
            val = self.vars[rev_var[op].value]
        elif op == "Y":
            val = self.vars[0]
        else:
            num = self.floatDecoder.decode([op])
            val = np.full_like(self.env[0], num)

        self.env.append(val)

    def init_vars(self, vars):
        self.vars = vars
        self.env = []

    def get_result(self):
        return self.env[-1]

def to_sympy_expr(instrs, floatDecoder):
    ans = []
    for instr in instrs:
        op = instr[0]
        if op in rev_biop:
            left, right = instr[1], instr[2]
            ans.append(Node(rev_biop[op], ans[left], ans[right]))
        elif op in rev_unop:
            left = instr[1]
            ans.append(Node(rev_unop[op], ans[left]))
        elif op in rev_var:
            ans.append(Node(rev_var[op]))
        elif op == "Y":
            ans.append(Node(None))
        else:
            ans.append(Node(floatDecoder.decode([op])))
    return ans[-1]