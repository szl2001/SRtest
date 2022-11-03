from enum import unique, auto
from exprtree.expr import BinaryOp, UnaryOp, Variable


@unique
class E2EBiOp(BinaryOp):
    add = auto()
    mul = auto()
    sub = auto()


@unique
class E2EUnOp(UnaryOp):
    inv = auto()
    abs = auto()
    sqr = auto()
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
