import sympy
import pandas as pd
import numpy as np
import math
import random
from constants import G,c,epsilon0,g,h,k,qe,mew0,NA,F,Bohr

def sample(path, n, save):
    collection = pd.read_csv(path)
    sample_result = []
    ulog_num = 0
    ulog_span = 0
    for i, line in collection.iterrows():
        pre_data = span_cal(line)
        ulog_num += pre_data[0]
        ulog_span += pre_data[1]
    
    u_span = round(ulog_span/ulog_num)
    print(u_span)
    for i, line in collection.iterrows():
        r = dict()

        pre_data = pre_handle(line, n, u_span)
        X, Y = get_points(pre_data[0], pre_data[1], pre_data[2], pre_data[3], u_span)

        r['X'] = X
        r['Y'] = Y
        r['EQ'] = pre_data[0]
        sample_result.append(r)

    res = pd.DataFrame(sample_result)
    res.to_csv(save)

def span_cal(line):

    n_var = line['variables']
    n_v = len(str.split(line['v1_type'], '&'))
    ulog_num = 0
    ulog_span = 0
    #print(line['Number'])
    
    #分离合并范围
    for i in range(0, n_v):
        max_s = []
        min_s = []
        min_scope =[]
        max_scope = []
        for j in range(0, int(n_var)):
            min_scope.append(str.split(str(line[f'v{j+1}_low']), '&'))
            max_scope.append(str.split(str(line[f'v{j+1}_high']), '&'))
            max_s.append((line[f'v{j+1}_name'],max_scope[j][i]))
            min_s.append((line[f'v{j+1}_name'],min_scope[j][i]))
        
        for j in range(0, int(n_var)):
            sample_scope = str.split(line[f'v{j+1}_sample_type'], '&')
            #print(line[f'v{j+1}_name'])
            if sample_scope[i] == 'ulog':
                if sympy.sympify(min_scope[j][i]).subs(min_s).evalf() == 0:
                    print(line['Number'])
                    raise ValueError("ulog min 0!")
                ulog_num += 1
                ulog_span += sympy.log(sympy.sympify(max_scope[j][i]).subs(max_s)/sympy.sympify(min_scope[j][i]).subs(min_s),10).evalf()

    return ulog_num, ulog_span

def pre_handle(line, n, u_span):
    names = locals()

    eq = line['Formula']
    exp = sympy.sympify(eq)
    n_var = line['variables']
    vars = []
    scope = dict()
    max_s = dict()
    min_s = dict()
    n_v = len(str.split(line['v1_type'], '&'))

    for i in range(0, n_v):
        scope[f'V_{i+1}'] = []
        max_s[f'V_{i+1}'] = []
        min_s[f'V_{i+1}'] = []

    for j in range(0, int(n_var)):
        if n_v == 1:
            if line[f'v{j+1}_type'] == 'I':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],integer=True)
            elif line[f'v{j+1}_type'] == 'F':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],real=True)
        else:
            names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],real=True)
        
        vars.append(line[f'v{j+1}_name'])
        #print(type(line[f'v{j+1}_low']))
        min_scope = str.split(str(line[f'v{j+1}_low']), '&')
        max_scope = str.split(str(line[f'v{j+1}_high']), '&')
        sample_scope = str.split(line[f'v{j+1}_sample_type'], '&')
        type_scope = str.split(line[f'v{j+1}_type'], '&')
        #分离合并范围

        for i in range(0, n_v):
            scope[f'V_{i+1}'].append([min_scope[i],max_scope[i],type_scope[i],sample_scope[i]])
            max_s[f'V_{i+1}'].append((line[f'v{j+1}_name'],sympy.sympify(max_scope[i])))
            min_s[f'V_{i+1}'].append((line[f'v{j+1}_name'],sympy.sympify(min_scope[i])))

    print(line['Number'])
    print(vars)
    print(scope)
    #for j in range(0,n_var):
    #    print(scope[f'V_{i+1}'][j][1], scope[f'V_{i+1}'][j][0])
    v = [np.prod([sympy.log(float(sympy.sympify(scope[f'V_{i+1}'][j][1]).subs(max_s[f'V_{i+1}']))/float(sympy.sympify(scope[f'V_{i+1}'][j][0]).subs(min_s[f'V_{i+1}'])),10).evalf() if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]) for i in range(0,n_v)]
    n_points = [round(p/sum(v)*n) for p in v]
    return exp, vars, scope, n_points
        
def get_points(exp, vars, scope, n, u_span):
    names = locals()
    n_v = len(n)
    n_var = len(scope['V_1'])
    X = []
    Y = []

    for j in range(0, int(n_var)):
        names['x'+str(j)] = sympy.Symbol(vars[j])

    for i in range(0,n_v):
        limit=[]
        max_s = []
        min_s = []
        #提取变量大小关系
        for j in range(0,n_var):
            for p in (0,1):
                if not sympy.sympify(scope[f'V_{i+1}'][j][p]).is_real:
                    for q in range(0,n_var):
                        if sympy.sympify(scope[f'V_{i+1}'][j][p]).has(names['x'+str(q)]):
                            limit.append((j, q) if p else (q, j))
                            scope[f'V_{i+1}'][j][p] = scope[f'V_{i+1}'][q][p]
                            print(scope[f'V_{i+1}'][j][p], vars)
                            print(type(scope[f'V_{i+1}'][j][p]), type(vars[0]), scope[f'V_{i+1}'][j][p] == vars[0])
                            break
                            
                    if not sympy.sympify(scope[f'V_{i+1}'][j][p]).is_real:
                        raise ValueError("Error scope!")                    
                        
            max_s.append((vars[j],scope[f'V_{i+1}'][j][1]))
            min_s.append((vars[j],scope[f'V_{i+1}'][j][0]))

        #SALIENT VARIABLE HOMOGENIZATION ALGORITHM
        print(scope[f'V_{i+1}'][j][1], scope[f'V_{i+1}'][j][0])
        v = [math.ceil(sympy.log(float(sympy.sympify(scope[f'V_{i+1}'][j][1]).subs(max_s))/float(sympy.sympify(scope[f'V_{i+1}'][j][0]).subs(min_s)),10).evalf()) if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]
        V = np.prod(v)
        print(v)
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
            exp_c = exp
            for ch in constant:
                if ch not in vars:
                    exp_c = exp_c.subs(str(ch),ch.evalf())
            try:
                for j in range(0, n_var):
                    exp_c = exp_c.subs(vars[j], point[j])
            except:
                raise ValueError("Error calculate!")
            
            if sympy.sympify(exp_c) == sympy.nan or sympy.sympify(exp_c) == sympy.oo:
                continue

            #根据分布概率取点
            #print(V)
            #print(loc)
            if loc < 0:
                raise ValueError("Error loc!")
            C[loc] += 1
            p_m = min(a/sum(C) for a in C)
            p_curr = C[loc]/sum(C)
            p = (p_m + 0.1)/(p_curr + 0.1)
            if random.uniform(0,1) <= p:
                points.append(point)
                Y.append(sympy.sympify(exp_c).evalf())
            
        X += points
    
    return X, Y

#限定范围内按分布取一个点
def get_point(i, scope, n_var, u_span):
    v = [math.ceil(sympy.log(float(sympy.sympify(scope[f'V_{i+1}'][j][1]))/float(sympy.sympify(scope[f'V_{i+1}'][j][0])),10).evalf()) if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]
    V = np.prod(v)
    point = []
    loc = 0
    for j in range(0,n_var):      
        max_s = float(sympy.sympify(scope[f'V_{i+1}'][j][1]))
        min_s = float(sympy.sympify(scope[f'V_{i+1}'][j][0]))
        V /= v[j]
        #print(v,V)
        if scope[f'V_{i+1}'][j][3] == 'ulog':
            s = random.uniform(0,v[j])
            #print(s)
            loc += (int(s) - 1) * V if s >= 1 else 0
            sample_value = sympy.sympify(min_s) * sympy.Pow(10, s)
            if scope[f'V_{i+1}'][j][2] == 'I':
                sample_value = int(sample_value)
            elif scope[f'V_{i+1}'][j][2] == 'NI' or scope[f'V_{i+1}'][j][2] == 'AI':
                raise ValueError("ulog has no NI or AI!")
        elif scope[f'V_{i+1}'][j][3] == 'u' and (scope[f'V_{i+1}'][j][2] == 'I' or scope[f'V_{i+1}'][j][2] == 'NI' or scope[f'V_{i+1}'][j][2] == 'AI'):
            sample_value = random.randint(min_s, max_s)
            index = math.ceil((sample_value - min_s) * u_span/(max_s - min_s))
            #print(index)
            loc += (int(index) - 1) * V if index >= 1 else 0
        elif scope[f'V_{i+1}'][j][3] == 'u' and (scope[f'V_{i+1}'][j][2] == 'F' or scope[f'V_{i+1}'][j][2] == 'NF' or scope[f'V_{i+1}'][j][2] == 'AF'):
            sample_value = random.uniform(min_s, max_s)
            index = math.ceil((sample_value - min_s) * u_span/(max_s - min_s))
            #print(index)
            loc += (int(index) - 1) * V if index >= 1 else 0

        #print(loc)
        point.append(sample_value)
    return loc, point

if __name__ == "__main__":
    sample('real/phy_.csv', 10, 'points/phy.csv')
    #sample('real/bio_.csv', 10, 'points/bio.csv')
    sample('real/che_.csv', 10, 'points/che.csv')