class Id:

    def encode(self, x):
        return x

from e2elang.opcode import E2EBiOp, E2EUnOp, E2EVar
from floatconvert.fp16_base10_converter import FP16Base10Converter
fp = FP16Base10Converter()
from e2elang.srasm_visitor import SRasmVisitor
vis = SRasmVisitor(fp)
from main import generate_expr
a = generate_expr(1)
ans = vis.visit(a[0][0])
for i, x in enumerate(ans):
    print(i, end=" ")
    print(x)

from e2elang.string_visitor import StringVisitor
str_vis = StringVisitor(fp)
prefix = list(str_vis.visit(a[0][0]))
print(prefix)

from e2elang.sympy_vistor import SympyVisitor
sym_vis = SympyVisitor()
sym0 = sym_vis.visit(a[0][0])
# print(sym0)

from e2elang.srasm_interpreter import SRasmInterpreter
srasm_inter = SRasmInterpreter(fp)
points = a[0][1][0]
# print(points)
y = points[0]
xs = points[1:]
xs = xs.astype("float64")
vars = []
for x in xs:
    vars.append(x)
# print(len(vars))
srasm_inter.init_vars(vars)
srasm_inter.execute(ans)
nodex = srasm_inter.to_sympy_expr(ans)
res = srasm_inter.get_result()


print("SRasm")
import numpy as np
close = np.isclose(res, y)
# print(close)
print(np.sum(close))
from sklearn.metrics import r2_score
print(r2_score(res, y))

from e2elang.prefix_interpreter import PrefixIntepreter

pre_inter = PrefixIntepreter(fp)
node = pre_inter.parse_prefix(prefix)
sym1 = sym_vis.visit(node)
# print(sym1)
# print(sym0)
sym2 = sym_vis.visit(nodex)

from sympy import lambdify
def evals(sym):
    free_vars = list(sym.free_symbols)
    # sort variables by name
    free_vars = sorted(free_vars, key=lambda v: int(v.name[1:]))
    f = lambdify(free_vars, sym, "numpy")
    return f(*xs)

print("Prefix")
yy = evals(sym1)
close = np.isclose(yy, y)
# print(close)
print(np.sum(close))
print(r2_score(yy, y))

print("SRasm to Sympy")
y3 = evals(sym2)
close = np.isclose(y3, y)
# print(close)
print(np.sum(close))
print(r2_score(y3, y))

print(res)
print(y)
print(yy)
print(y3)

print(sym1)
print(sym2)

str_expr = str(sym1)

q = "lambda x1, x2, x3, x4, x5, x6, x7, x8, x9, x10: " + str_expr
q = eval(q)
y4 = q(*xs)

print("Y4 & y")
close = np.isclose(y4, y)
# print(close)
print(np.sum(close))
print(r2_score(y4, y))

print("Y4 & res")
close = np.isclose(y4, res)
# print(close)
print(np.sum(close))
print(r2_score(y4, res))

print("test")

def visit(node):
    if node.ty == E2EBiOp.add:
        return '(' + visit(node.lchild) + '+' + visit(node.rchild) + ')'
    elif node.ty == E2EBiOp.mul:
        return '(' + visit(node.lchild) + '*' + visit(node.rchild) + ')'
    elif node.ty == E2EBiOp.sub:
        return '(' + visit(node.lchild) + '-' + visit(node.rchild) + ')'
    elif node.ty == E2EUnOp.inv:
        return '(1/' + visit(node.lchild) + ')'
    elif node.ty == E2EUnOp.sqr:
        return '(' + visit(node.lchild) + '**2)'
    elif isinstance(node.ty, E2EVar):
        return f"x{node.ty.value}"
    else:
        return str(node.ty)

vis_node_str = visit(node)
print(vis_node_str)
print(visit(nodex))
    
q = "lambda x1, x2, x3, x4, x5, x6, x7, x8, x9, x10: " + vis_node_str
q = eval(q)
y5 = q(*xs)
print("Y5 & res")
close = np.isclose(y5, res)
# print(close)
print(np.sum(close))
print(r2_score(y5, res))

env = []
def visit2(node):
    if node.ty == E2EBiOp.add:
        val = visit2(node.lchild) + visit2(node.rchild)
    elif node.ty == E2EBiOp.mul:
        val = visit2(node.lchild) * visit2(node.rchild)
    elif node.ty == E2EBiOp.sub:
        val = visit2(node.lchild) - visit2(node.rchild)
    elif node.ty == E2EUnOp.inv:
        val = 1 / visit2(node.lchild)
    elif node.ty == E2EUnOp.sqr:
        val = visit2(node.lchild) ** 2
    elif isinstance(node.ty, E2EVar):
        return xs[node.ty.value-1]
    else:
        val = node.ty
    env.append(val)
    return val

y6 = visit2(node)
print("Y6 & res")
close = np.isclose(y6, res)
# print(close)
print(np.sum(close))
print(r2_score(y6, res))

penv = srasm_inter.env[10:]
print(len(penv))
print(len(env))
assert len(penv) == len(env)
#for i, (x, y) in enumerate(zip(penv, env)):
#    print(i, end=" ")
#    print(x == y)