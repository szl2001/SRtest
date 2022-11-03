from abc import ABC, abstractclassmethod
from typing import Any
from exprtree.expr import BinaryOp, UnaryOp, Variable

class Visitor(ABC):

    @abstractclassmethod
    def visit_binary_op(self, ty, left, right):
        pass

    @abstractclassmethod
    def visit_unary_op(self, ty, left):
        pass

    @abstractclassmethod
    def visit_var(self, ty):
        pass

    @abstractclassmethod
    def visit_float(self, ty):
        pass
    
    def visit(self, node) -> Any:
        ty = node.ty
        if isinstance(ty, BinaryOp):
            left = self.visit(node.lchild)
            right = self.visit(node.rchild)
            return self.visit_binary_op(ty, left, right)
        elif isinstance(ty, UnaryOp):
            left = self.visit(node.lchild)
            return self.visit_unary_op(ty, left)
        elif isinstance(ty, Variable):
            return self.visit_var(ty)
        elif isinstance(ty, float):
            return self.visit_float(ty)
        else:
            raise NotImplementedError(f"Unknown node type: {ty}")

   
