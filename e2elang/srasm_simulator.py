# Interpret step by step
import numpy as np

biop_map = {
    "add": np.add,
    "mul": np.multiply,
    "sub": np.subtract,
    "div": np.divide,
    "pow": np.power
}

unop_map = {
    "abs":  np.abs,
    "exp":  np.exp,
    "sqrt": np.sqrt,
    "inv":  lambda x: 1 / x,
    "ln":  np.log,
    "lg": np.log10,
    "sin":  np.sin,
    "cos":  np.cos,
    "tan":  np.tan,
    "asin":  np.arcsin,
    "acos":  np.arccos,
    "atan":  np.arctan,
    "sinh":  np.sinh,
    "cosh":  np.cosh,
    "tanh":  np.tanh
}

def execute(instr, mem, floatDecoder):
    op, operand0, operand1 = instr
    if op[0] == 'x' or op == "<PAD>":
        return
    if op in biop_map:
        val = biop_map[op](mem[operand0], mem[operand1])
    elif op in unop_map:
        val = unop_map[op](mem[operand0])
    else:
        num = floatDecoder.decode([op])
        val = np.full_like(mem[0], num)
    mem.append(val)
       