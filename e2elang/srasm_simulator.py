# Interpret step by step
import numpy as np

biop_map = {
    "add": np.add,
    "mul": np.multiply,
    "sub": np.subtract
}

unop_map = {
    "abs":  np.abs,
    "atan": np.arctan,
    "cos":  np.cos,
    "exp":  np.exp,
    "inv":  lambda x: 1 / x,
    "log":  np.log,
    "sin":  np.sin,
    "sqr":  np.square,
    "sqrt": np.sqrt,
    "tan":  np.tan
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
       