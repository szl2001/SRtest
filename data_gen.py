from dataclasses import dataclass
from itertools import chain
from typing import List, Tuple, Dict
from e2elang.opcode import E2EBiOp
from exprtree.expr import Node, BinaryOp, UnaryOp, Variable
from numpy.random import Generator
from constants import Constants
import numpy as np
import math


@dataclass
class GenConfig:
    vars: List[Variable]
    binary_op_distribution: Dict[BinaryOp, int]
    unary_op_distribution: Dict[UnaryOp, int]
    const_distribution: Dict[Constants ,int]
    max_binary_ops_coff: float
    max_binary_ops: int
    ave_binary_ops: int
    max_unary_ops: int

    affine_mantissa: Tuple[float, float] = (0.0, 1.0)
    affine_exponent: Tuple[float, float] = (-50.0, 50.0)

    # max_binary_ops = input_dim + max_binary_ops_extra


class TreeGen:

    def __init__(self, cfg: GenConfig, rng: Generator):
        self.cfg = cfg
        self.rng = rng

        def normalize(arr: List[int]):
            return np.array(arr) / np.sum(arr)

        self.binary_op_set = list(self.cfg.binary_op_distribution.keys())
        self.binary_op_dist = normalize(list(self.cfg.binary_op_distribution.values()))
        self.unary_op_set = list(self.cfg.unary_op_distribution.keys())
        self.unary_op_dist = normalize(list(self.cfg.unary_op_distribution.values()))

    def mk_random_binary_op(self) -> Node:
        idx = self.rng.choice(len(self.binary_op_set), p=self.binary_op_dist)
        return Node(self.binary_op_set[idx])

    def mk_random_unary_op(self) -> Node:
        idx = self.rng.choice(len(self.unary_op_set), p=self.unary_op_dist)
        return Node(self.unary_op_set[idx])

    def uniform(self, low, high):
        return self.rng.random() * (high - low) + low

    def affine_random(self):
        mantissa = self.uniform(*self.cfg.affine_mantissa)
        exponent = self.uniform(*self.cfg.affine_exponent)
        sign = self.rng.choice([-1, 1])
        return sign * mantissa * (10 ** exponent)

    def affine_transform(self, node: Node):
        mul_const = Node(self.affine_random())
        mul_node = Node(E2EBiOp.mul, rchild=mul_const)
        node.insert_before(mul_node)
        add_const = Node(self.affine_random())
        add_node = Node(E2EBiOp.add, rchild=add_const)
        mul_node.insert_before(add_node)

    def sample_binary_tree(self, nodes_num: int):
        if nodes_num == 0:
            empty_node = Node(None)
            return empty_node, [], [empty_node]
        else:
            node: Node = self.mk_random_binary_op()
            lnodes_num = self.rng.integers(0, nodes_num)
            rnodes_num = nodes_num - lnodes_num - 1
            lchild, lnodes, empty_lnodes = self.sample_binary_tree(lnodes_num)
            rchild, rnodes, empty_rnodes = self.sample_binary_tree(rnodes_num)
            node.link_left(lchild)
            node.link_right(rchild)
            return node, chain([node], lnodes, rnodes), chain(empty_lnodes, empty_rnodes)

    def sample_tree(self, input_dim: int):
        max_binary_ops = max(min(math.ceil(input_dim * self.cfg.max_binary_ops_coff), self.cfg.max_binary_ops), input_dim + int(self.cfg.ave_binary_ops))
        binary_ops_num = self.rng.integers(input_dim - 1, max_binary_ops + 1)
        binary_tree, binary_op_nodes, var_nodes = self.sample_binary_tree(
            binary_ops_num)
        binary_op_nodes, var_nodes = list(binary_op_nodes), list(var_nodes)
        for i, node in enumerate(var_nodes):
            if i >= input_dim:
                node.ty = self.cfg.vars[self.rng.integers(input_dim)]
            else:
                node.ty = self.cfg.vars[i]

        sentinel_node = Node(None)
        sentinel_node.link_left(binary_tree)

        nodes = binary_op_nodes + var_nodes
        unary_ops_num = self.rng.integers(0, self.cfg.max_unary_ops + 1)
        unary_op_nodes = []
        for i in self.rng.choice(len(nodes), unary_ops_num):
            unary_node = self.mk_random_unary_op()
            nodes[i].insert_before(unary_node)
            unary_op_nodes.append(unary_node)

        for node in chain(var_nodes, unary_op_nodes):
            self.affine_transform(node)

        return sentinel_node.lchild
