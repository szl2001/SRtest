from enum import Enum
from typing import Union, Optional

class BinaryOp(Enum):
    pass


class UnaryOp(Enum):
    pass


class Variable(Enum):
    pass


Opcode = Union[BinaryOp, UnaryOp, Variable, float]


class Node:
    """
    A wrapper of operator's Type
    """
    
    def __init__(self, ty: Optional[Opcode], lchild=None, rchild=None):
        self.ty = ty
        self.lchild = lchild
        self.rchild = rchild
        self.parent = None

    def link_left(self, node):
        self.lchild = node
        node.parent = self

    def link_right(self, node):
        self.rchild = node
        node.parent = self

    def insert_before(self, unary_node):
        parent = self.parent
        unary_node.link_left(self)
        if parent is not None:
            unary_node.parent = parent
            if parent.lchild is self:
                parent.lchild = unary_node
            else:
                parent.rchild = unary_node
