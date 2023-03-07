import sympy
import pandas as pd
import numpy as np
import math
import random
from constants import G,c,epsilon0,g,h,k,qe,mew0,NA,F,Bohr

def sample(path, n, save):
    collection = pd.read_csv(path)
    sample_result = []
    for i, line in collection.iterrows():
        r = dict()

        pre_data = pre_handle(line, n)
        X, Y = get_points(pre_data[0], pre_data[1], pre_data[2], pre_data[3], pre_data[4])

        r['X'] = X
        r['Y'] = Y
        r['EQ'] = pre_data[0]
        sample_result.append(r)

    res = pd.DataFrame(sample_result)
    res.to_csv(save)

def pre_handle(line, n):
    names = locals()

    eq = line['Formula']
    exp = sympy.sympify(eq)
    n_var = line['variables']
    vars = []
    scope = dict()
    n_v = len(str.split(line['v1_type'], '&'))
    ulog_num = 0
    ulog_span = 0

    for i in range(0, n_v):
        scope[f'V_{i+1}'] = []

    for j in range(0, int(n_var)):
        if n_v == 1:
            if line[f'v{j+1}_type'] == 'I':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],integer=True)
            elif line[f'v{j+1}_type'] == 'F':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],real=True)
        else:
            names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],real=True)
        
        vars.append(line[f'v{j+1}_name'])
        
        min_scope = str.split(line[f'v{j+1}_low'], '&')
        max_scope = str.split(line[f'v{j+1}_high'], '&')
        sample_scope = str.split(line[f'v{j+1}_sample_type'], '&')
        type_scope = str.split(line[f'v{j+1}_type'], '&')
        #分离合并范围
        for i in range(0, n_v):
            scope[f'V_{i+1}'].append((min_scope[i],max_scope[i],type_scope[i],sample_scope[i]))
            if sample_scope[i] == 'ulog':
                ulog_num += 1
                ulog_span += sympy.log(max_scope[i]/min_scope[i],10).evalf()

    u_span = round(ulog_span/ulog_num)
    v = [np.prod([sympy.log(scope[f'V_{i+1}'][j][1]/scope[f'V_{i+1}'][j][0],10).evalf() if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]) for i in range(0,n_v)]
    n_points = [round(p/sum(v)*n) for p in v]
    return exp, vars, scope, n_points, u_span
        
def get_points(exp, vars, scope, n, u_span):
    n_v = len(n)
    n_var = len(scope['V_1'])
    X = []
    Y = []

    for i in range(0,n_v):
        limit=[]
        #提取变量大小关系
        for j in range(0,n_var):
            for p in (0,1):
                if not sympy.sympify(scope[f'V_{i+1}'][j][p]).is_real:
                    if scope[f'V_{i+1}'][j][p] not in vars:
                        raise ValueError("Error scope!")
                    else:
                        index = vars.index(scope[f'V_{i+1}'][j][p])
                        limit.append((j, index) if p else (index, j))
                        scope[f'V_{i+1}'][j][p] = scope[f'V_{i+1}'][index][1]

        #SALIENT VARIABLE HOMOGENIZATION ALGORITHM
        v = [math.ceil(sympy.log(scope[f'V_{i+1}'][j][1]/scope[f'V_{i+1}'][j][0],10).evalf()) if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]
        V = np.prod(v)
        Volumn = V
        C = [0] * Volumn
        points = []
        while len(points) < n[i]: 
            error = 0
            #随机选取样点
            loc, point = get_point(i, scope, n_var, u_span)
            #处理limit
            for l in limit:
                if point[l[0]] > point[l[1]]:
                    error = 1
                    break
            if error == 1:
                continue
            #处理NAN、INF
            constant = {G,c,epsilon0,g,h,k,qe,mew0,Bohr,NA,F}
            for ch in constant:
                if ch not in vars:
                    exp = exp.subs(str(ch),ch.evalf())
            try:
                for j in range(0, n_var):
                    exp = exp.subs(vars[j], point[j])
            except:
                raise ValueError("Error calculate!")
            
            if sympy.sympify(exp) == sympy.nan or sympy.sympify(exp) == sympy.oo:
                continue
            else:
                Y.append(sympy.sympify(exp))

            #根据分布概率取点
            C[loc] += 1
            p_m = min(a/sum(C) for a in C)
            p_curr = C[loc]/sum(C)
            p = (p_m + 0.1)/(p_curr + 0.1)
            if random.uniform(0,1) <= p:
                points.append(point)
            
        X += points
    
    return X, Y

#限定范围内按分布取一个点
def get_point(i, scope, n_var, u_span):
    v = [math.ceil(sympy.log(scope[f'V_{i+1}'][j][1]/scope[f'V_{i+1}'][j][0],10).evalf()) if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]
    V = np.prod(v)
    point = []
    loc = 0
    for j in range(0,n_var):
        V /= v[j]
        if scope[f'V_{i+1}'][j][3] == 'ulog':
            s = sympy.Pow(10, random.uniform(0,v[j]))
            loc += (int(s) - 1) * V
            sample_value = sympy.sympify(scope[f'V_{i+1}'][j][0]) * s
            if scope[f'V_{i+1}'][j][2] == 'I':
                sample_value = int(sample_value)
        elif scope[f'V_{i+1}'][j][3] == 'u' and scope[f'V_{i+1}'][j][2] == 'I':
            sample_value = random.randint(scope[f'V_{i+1}'][j][0], scope[f'V_{i+1}'][j][1])
            index = math.ceil((sample_value - scope[f'V_{i+1}'][j][0]) * u_span/(scope[f'V_{i+1}'][j][1] - scope[f'V_{i+1}'][j][0]))
            loc += (int(index) - 1) * V
        elif scope[f'V_{i+1}'][j][3] == 'u' and scope[f'V_{i+1}'][j][2] == 'F':
            sample_value = random.uniform(scope[f'V_{i+1}'][j][0], scope[f'V_{i+1}'][j][1])
            index = math.ceil((sample_value - scope[f'V_{i+1}'][j][0]) * u_span/(scope[f'V_{i+1}'][j][1] - scope[f'V_{i+1}'][j][0]))
            loc += (int(index) - 1) * V

        point.append(sample_value)
    return loc, point

if __name__ == "__main__":
    sample('real/phy_.csv', )