from enum import unique, auto
from exprtree.expr import BinaryOp, UnaryOp, Variable


@unique
class E2EBiOp(BinaryOp):
    add = auto()
    mul = auto()
    sub = auto()
    pow = auto()


@unique
class E2EUnOp(UnaryOp):
    inv = auto()
    abs = auto()
    sqrt = auto()
    sin = auto()
    cos = auto()
    tan = auto()
    atan = auto()
    log = auto()
    exp = auto()


@unique
class E2EVar(Variable):
    x1 = auto()
    x2 = auto()
    x3 = auto()
    x4 = auto()
    x5 = auto()
    x6 = auto()
    x7 = auto()
    x8 = auto()
    x9 = auto()
    x10 = auto()


binary_op_map = {
    E2EBiOp.add: "add",
    E2EBiOp.mul: "mul",
    E2EBiOp.sub: "sub",
    E2EBiOp.pow: "pow"
}

unary_op_map = {
    E2EUnOp.abs: "abs",
    E2EUnOp.atan: "atan",
    E2EUnOp.cos: "cos",
    E2EUnOp.exp: "exp",
    E2EUnOp.inv: "inv",
    E2EUnOp.log: "log",
    E2EUnOp.sin: "sin",
    E2EUnOp.sqrt: "sqrt",
    E2EUnOp.tan: "tan"
}

var_map = dict([(v, f"x{v.value}") for v in list(E2EVar)])
