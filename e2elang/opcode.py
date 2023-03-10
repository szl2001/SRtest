from enum import unique, auto
from exprtree.expr import BinaryOp, UnaryOp, Variable
from constants import G,c,epsilon0,g,h,k,qe,mew0,NA,F,Bohr
from sympy import pi


@unique
class E2EBiOp(BinaryOp):
    add = auto()
    mul = auto()
    sub = auto()
    div = auto()
    pow = auto()


@unique
class E2EUnOp(UnaryOp):
    inv = auto()
    abs = auto()
    sqrt = auto()
    sin = auto()
    cos = auto()
    tan = auto()
    asin = auto()
    acos = auto()
    atan = auto()
    sinh = auto()
    cosh = auto()
    tanh = auto()
    lg = auto()
    ln = auto()
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
    E2EBiOp.div: "div",
    E2EBiOp.pow: "pow"
}

unary_op_map = {
    E2EUnOp.abs: "abs",
    E2EUnOp.exp: "exp",
    E2EUnOp.inv: "inv",
    E2EUnOp.sqrt: "sqrt",
    E2EUnOp.lg: "lg",
    E2EUnOp.ln: "ln",
    E2EUnOp.sin: "sin",
    E2EUnOp.cos: "cos",
    E2EUnOp.tan: "tan",
    E2EUnOp.acos: "arccos",
    E2EUnOp.asin: "arcsin",
    E2EUnOp.atan: "arctan",
    E2EUnOp.sinh: "sinh",
    E2EUnOp.cosh: "cosh",
    E2EUnOp.tanh: "tanh"
}

real_biop_map = {
    "+": E2EBiOp.add,
    "*": E2EBiOp.mul,
    "-": E2EBiOp.sub,
    "/": E2EBiOp.div,
    "**": E2EBiOp.pow
}

real_unop_map = {
    "abs": E2EUnOp.abs,
    "exp": E2EUnOp.exp,
    "inv": E2EUnOp.inv,
    "sqrt": E2EUnOp.sqrt,
    "lg": E2EUnOp.lg,
    "ln": E2EUnOp.ln,
    "sin": E2EUnOp.sin,
    "cos": E2EUnOp.cos,
    "tan": E2EUnOp.tan,
    "arccos": E2EUnOp.acos,
    "arcsin": E2EUnOp.asin,
    "arctan": E2EUnOp.atan,
    "sinh": E2EUnOp.sinh,
    "cosh": E2EUnOp.cosh,
    "tanh": E2EUnOp.tanh
}

var_map = dict([(v, f"x{v.value}") for v in list(E2EVar)])

const_map = {
    "G": G,
    "c": c,
    "epsilon0": epsilon0,
    "g": g,
    "h": h,
    "k": k,
    "qe": qe,
    "mew0": mew0,
    "Bohr": Bohr,
    "NA": NA,
    "F": F,
    "pi": pi
}
