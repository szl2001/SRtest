import sympy
import pandas as pd
import numpy as np
import math
import random
from constants import G,c,epsilon0,g,h,k,qe,mew0,NA,F,Bohr,alpha,me

def sample(path, field, n, save):
    collection = pd.read_csv(f'real/{field}_.csv')
    global point_generated
    point_generated = 0 # 0 for test, 2023 for train
    sample_result = []
    ulog_num = 0
    ulog_span = 0
    for i, line in collection.iterrows():
        pre_data = span_cal(line)
        ulog_num += pre_data[0]
        ulog_span += pre_data[1]
    
    u_span = round(ulog_span/ulog_num)
    #print(u_span)
    collection = pd.read_csv(path)
    for i, line in collection.iterrows():
        r = dict()

        pre_data = pre_handle(line, n, u_span)
        X, Y, expr = get_points_ran(pre_data[0], pre_data[1], pre_data[2], pre_data[3], u_span)
        

        r['vars'] = pre_data[1]
        r['X'] = X
        r['Y'] = Y
        r['EQ'] = pre_data[0]
        r['expr'] = expr
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
                while not (sympy.sympify(max_scope[j][i]).is_real and sympy.sympify(min_scope[j][i]).is_real):
                    max_scope[j][i] = sympy.sympify(max_scope[j][i]).subs(max_s)
                    min_scope[j][i] = sympy.sympify(min_scope[j][i]).subs(min_s)

                ulog_num += 1
                ulog_span += sympy.log(sympy.sympify(max_scope[j][i]).subs(max_s)/sympy.sympify(min_scope[j][i]).subs(min_s),10).evalf()
                #print(line['Number'])
                #print(max_s,min_s)
                #print(ulog_span)

    return ulog_num, ulog_span

def pre_handle(line, n, u_span):
    names = locals()

    eq = line['Formula']
    eq = eq.replace('lg', '1/log(10,2)*log')
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

    #print(line['Number'])
    #print(vars)
    #print(scope)
    #for j in range(0,n_var):
    #    print(scope[f'V_{i+1}'][j][1], scope[f'V_{i+1}'][j][0])
    tmp_scope = scope.copy()
    for i in range(0,n_v):
        for j in range(0,n_var):
            while not (sympy.sympify(tmp_scope[f'V_{i+1}'][j][1]).is_real and sympy.sympify(tmp_scope[f'V_{i+1}'][j][0]).is_real):
                    tmp_scope[f'V_{i+1}'][j][1] = sympy.sympify(tmp_scope[f'V_{i+1}'][j][1]).subs(max_s[f'V_{i+1}'])
                    tmp_scope[f'V_{i+1}'][j][0] = sympy.sympify(tmp_scope[f'V_{i+1}'][j][0]).subs(min_s[f'V_{i+1}'])
    v = [np.prod([sympy.log(float(sympy.sympify(tmp_scope[f'V_{i+1}'][j][1]).subs(max_s[f'V_{i+1}']))/float(sympy.sympify(tmp_scope[f'V_{i+1}'][j][0]).subs(min_s[f'V_{i+1}'])),10).evalf() if tmp_scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]) for i in range(0,n_v)]
    v = [abs(a) for a in v]
    n_points = [round(p/sum(v)*n) for p in v]
    #调整数量
    while sum(n_points) != n:
        sum_n = sum(n_points)
        for index in range(len(n_points)):
            if n_points[index] > round((sum_n - n)/len(n_points)):
                n_points[index] -= round((sum_n - n)/len(n_points))
            if abs(sum(n_points) - n) < 2:
                n_points[n_points.index(max(n_points))] -= (sum(n_points) - n)

    return eq, vars, scope, n_points
        
def get_points(eq, vars, scope, n, u_span):
    global point_generated
    
    exp = sympy.sympify(eq)
    names = locals()
    n_v = len(n)
    n_var = len(scope['V_1'])
    X = []
    Y = []

    expr = exp
    constant = {G,c,epsilon0,g,h,k,qe,mew0,Bohr,NA,F,alpha,me}
    
    for j in range(0, int(n_var)):
        names['x'+str(j)] = sympy.Symbol(vars[j])

    for ch in constant:
        if str(ch) not in vars:
            expr = expr.subs(str(ch),ch.evalf())
    
    for j in range(0, int(n_var)):
        expr = expr.subs(names['x'+str(j)],f'x{j+1}')
    
    for i in range(0,n_v):
        limit=[]
        max_s = []
        min_s = []
        #提取变量大小关系
        for j in range(0,n_var):
            for p in (0,1):
                if not sympy.sympify(scope[f'V_{i+1}'][j][p]).is_real:
                    while sympy.sympify(scope[f'V_{i+1}'][j][p]).has(names['x'+str(q)] for q in range(0,n_var)):
                        for q in range(0,n_var):
                            if sympy.sympify(scope[f'V_{i+1}'][j][p]).has(names['x'+str(q)]):
                                limit.append((j, q, '<',scope[f'V_{i+1}'][j][p]) if p else (j, q, '>',scope[f'V_{i+1}'][j][p]))
                                n_l = sympy.sympify(scope[f'V_{i+1}'][j][p]).subs(min_s).evalf()
                                n_h = sympy.sympify(scope[f'V_{i+1}'][j][p]).subs(max_s).evalf()
                                scope[f'V_{i+1}'][j][p] = n_h if p else n_l

                                #print(scope[f'V_{i+1}'][j][p], vars)
                                break
                                
                    if not sympy.sympify(scope[f'V_{i+1}'][j][p]).is_real:
                        raise ValueError("Error scope!")    
                  
            max_s.append((vars[j],scope[f'V_{i+1}'][j][1]))
            min_s.append((vars[j],scope[f'V_{i+1}'][j][0]))

        #for j in range(0,n_var): 
        #    while not (sympy.sympify(scope[f'V_{i+1}'][j][1]).is_real and sympy.sympify(scope[f'V_{i+1}'][j][0]).is_real):
        #        scope[f'V_{i+1}'][j][1] = sympy.sympify(scope[f'V_{i+1}'][j][1]).subs(max_s)
        #        scope[f'V_{i+1}'][j][0] = sympy.sympify(scope[f'V_{i+1}'][j][0]).subs(min_s)          

        #SALIENT VARIABLE HOMOGENIZATION ALGORITHM
        #print(scope[f'V_{i+1}'], scope[f'V_{i+1}'])
        v = [math.ceil(sympy.log(float(sympy.sympify(scope[f'V_{i+1}'][j][1]).subs(max_s))/float(sympy.sympify(scope[f'V_{i+1}'][j][0]).subs(min_s)),10).evalf()) if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]
        v = [math.ceil(sympy.log(abs(v[j]),4).evalf()) if (sympy.log(abs(v[j]),4).evalf() > 1 and scope[f'V_{i+1}'][j][3] == 'ulog') else v[j] for j in range(0,n_var)]
        v = [abs(a) for a in v]
        #print(v)
        V = np.prod(v)
        #print(v)
        Volumn = V
        C = [0] * Volumn
        points = []
        try_num = 0
        while len(points) < n[i]: 
            error = 0
            #随机选取样点
            loc, point = get_point(i, scope, n_var, u_span)
            point_generated += 1

            #处理limit
            for l in limit:
                error = point[l[0]] > sympy.sympify(l[3]).subs(vars[l[1]], point[l[1]]).evalf() if l[2] == '<' else point[l[0]] < sympy.sympify(l[3]).subs(vars[l[1]], point[l[1]]).evalf()
                if error == 1: 
                    break
            if error == 1:
                continue

            #处理NAN、INF
            exp_c = exp
            for ch in constant:
                if str(ch) not in vars:
                    exp_c = exp_c.subs(str(ch),ch.evalf())

            try:
                for j in range(0, n_var):
                    exp_c = exp_c.subs(vars[j], point[j])
            except:
                raise ValueError("Error calculate!")
            
            if sympy.sympify(exp_c).evalf() == sympy.nan or sympy.sympify(exp_c).evalf() == sympy.oo or sympy.sympify(exp_c).evalf() == -sympy.oo \
                or sympy.sympify(exp_c).evalf() == sympy.zoo or sympy.sympify(exp_c).evalf().has(sympy.I):
                try_num += 1
                if try_num ==100*n[i]:
                    print(exp)
                    print(sympy.sympify(exp))
                    print(sympy.sympify(exp.subs(vars[2], point[2])))
                    print(sympy.sympify(exp_c).evalf())
                    print(len(Y))
                    print(n[i],n)
                    print(vars,point)
                    raise ValueError("too mang times!")
                continue
            

            #根据分布概率取点
            if loc < 0 or loc > V:
                print(V, loc)
                raise ValueError("Error loc!")
            C[loc] += 1
            p_m = min(a/sum(C) for a in C)
            p_curr = C[loc]/sum(C)
            p = (p_m + 0.1)/(p_curr + 0.1)
            random.seed(point_generated)
            if random.uniform(0,1) <= p:
                y = sympy.sympify(exp_c).evalf()
                if y.is_real:
                    if abs(y) < 1e100:
                        Y.append(sympy.sympify(exp_c).evalf())
                    else:
                        continue
                else:
                    print(str(exp))
                    print(vars,point,scope)
                    print(y)
                    raise ValueError("Nan y!")
                
                points.append(point)
            
        X += points
    
    return X, Y, str(expr)

#限定范围内按分布取一个点
def get_point(i, scope, n_var, u_span):
    global point_generated
    random.seed(point_generated)
    v = [math.ceil(sympy.log(float(sympy.sympify(scope[f'V_{i+1}'][j][1]))/float(sympy.sympify(scope[f'V_{i+1}'][j][0])),10).evalf()) if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]
    v = [(v[j], math.ceil(sympy.log(abs(v[j]),4).evalf())) if (sympy.log(abs(v[j]),4).evalf() > 1 and scope[f'V_{i+1}'][j][3] == 'ulog') else v[j] for j in range(0,n_var)]
    V = np.prod([abs(v[j][1]) if isinstance(v[j],tuple) else abs(v[j]) for j in range(0,n_var)])
    point = []
    loc = 0
    for j in range(0,n_var):      
        max_s = float(sympy.sympify(scope[f'V_{i+1}'][j][1]))
        min_s = float(sympy.sympify(scope[f'V_{i+1}'][j][0]))
        if isinstance(v[j],tuple):
            V /= abs(v[j][1])
        else:
            V /= abs(v[j])
        #print(v,V)
        if scope[f'V_{i+1}'][j][3] == 'ulog':
            s = random.uniform(0,v[j][0]) if isinstance(v[j],tuple) else random.uniform(0,v[j])
            
            loc += (math.ceil(s*v[j][1]/v[j][0]) - 1) * V if isinstance(v[j],tuple) else int(abs(s)) * V
            sample_value = sympy.sympify(min_s) * sympy.Pow(10, s)
            #print(s, sample_value, loc)

            if scope[f'V_{i+1}'][j][2] == 'I':
                sample_value = int(sample_value)
            elif scope[f'V_{i+1}'][j][2] == 'NI' or scope[f'V_{i+1}'][j][2] == 'AI':
                raise ValueError("ulog has no NI or AI!")
        elif scope[f'V_{i+1}'][j][3] == 'u' and (scope[f'V_{i+1}'][j][2] == 'I' or scope[f'V_{i+1}'][j][2] == 'NI' or scope[f'V_{i+1}'][j][2] == 'AI'):
            sample_value = random.randint(min_s, max_s) 
            index = math.ceil((sample_value - min_s) * u_span/(max_s - min_s))
            #print(index,loc)
            loc += (int(index) - 1) * V if index > 0 else 0
        elif scope[f'V_{i+1}'][j][3] == 'u' and (scope[f'V_{i+1}'][j][2] == 'F' or scope[f'V_{i+1}'][j][2] == 'NF' or scope[f'V_{i+1}'][j][2] == 'AF'):
            sample_value = random.uniform(min_s, max_s)
            index = math.ceil((sample_value - min_s) * u_span/(max_s - min_s))
            loc += (int(index) - 1) * V if index > 0 else 0
            #print(index,loc)

        point.append(sample_value)
    return loc, point


def get_points_ran(eq, vars, scope, n, u_span):
    global point_generated
    
    exp = sympy.sympify(eq)
    names = locals()
    n_v = len(n)
    n_var = len(scope['V_1'])
    X = []
    Y = []

    expr = exp
    constant = {G,c,epsilon0,g,h,k,qe,mew0,Bohr,NA,F,alpha,me}
    
    for j in range(0, int(n_var)):
        names['x'+str(j)] = sympy.Symbol(vars[j])

    for ch in constant:
        if str(ch) not in vars:
            expr = expr.subs(str(ch),ch.evalf())
    
    for j in range(0, int(n_var)):
        expr = expr.subs(names['x'+str(j)],f'x{j+1}')
    
    expr = expr.evalf()
    
    for i in range(0,n_v):
        limit=[]
        max_s = []
        min_s = []
        #提取变量大小关系
        for j in range(0,n_var):
            for p in (0,1):
                if not sympy.sympify(scope[f'V_{i+1}'][j][p]).is_real:
                    while sympy.sympify(scope[f'V_{i+1}'][j][p]).has(names['x'+str(q)] for q in range(0,n_var)):
                        for q in range(0,n_var):
                            if sympy.sympify(scope[f'V_{i+1}'][j][p]).has(names['x'+str(q)]):
                                limit.append((j, q, '<',scope[f'V_{i+1}'][j][p]) if p else (j, q, '>',scope[f'V_{i+1}'][j][p]))
                                n_l = sympy.sympify(scope[f'V_{i+1}'][j][p]).subs(min_s).evalf()
                                n_h = sympy.sympify(scope[f'V_{i+1}'][j][p]).subs(max_s).evalf()
                                scope[f'V_{i+1}'][j][p] = n_h if p else n_l

                                #print(scope[f'V_{i+1}'][j][p], vars)
                                break
                                
                    if not sympy.sympify(scope[f'V_{i+1}'][j][p]).is_real:
                        raise ValueError("Error scope!")    
                  
            max_s.append((vars[j],scope[f'V_{i+1}'][j][1]))
            min_s.append((vars[j],scope[f'V_{i+1}'][j][0]))

        #for j in range(0,n_var): 
        #    while not (sympy.sympify(scope[f'V_{i+1}'][j][1]).is_real and sympy.sympify(scope[f'V_{i+1}'][j][0]).is_real):
        #        scope[f'V_{i+1}'][j][1] = sympy.sympify(scope[f'V_{i+1}'][j][1]).subs(max_s)
        #        scope[f'V_{i+1}'][j][0] = sympy.sympify(scope[f'V_{i+1}'][j][0]).subs(min_s)          

        #SALIENT VARIABLE HOMOGENIZATION ALGORITHM
        #print(scope[f'V_{i+1}'], scope[f'V_{i+1}'])

        points = []
        try_num = 0
        while len(points) < n[i]: 
            error = 0
            #随机选取样点
            point = get_point_ran(i, scope, n_var, u_span)
            point_generated += 1

            #处理limit
            for l in limit:
                error = point[l[0]] > sympy.sympify(l[3]).subs(vars[l[1]], point[l[1]]).evalf() if l[2] == '<' else point[l[0]] < sympy.sympify(l[3]).subs(vars[l[1]], point[l[1]]).evalf()
                if error == 1: 
                    break
            if error == 1:
                continue

            #处理NAN、INF
            exp_c = exp
            for ch in constant:
                if str(ch) not in vars:
                    exp_c = exp_c.subs(str(ch),ch.evalf())

            try:
                for j in range(0, n_var):
                    exp_c = exp_c.subs(vars[j], point[j])
            except:
                raise ValueError("Error calculate!")
            
            try_num += 1
            if try_num ==100*n[i]:
                print(exp)
                print(sympy.sympify(exp))
                print(exp_c)
                print(sympy.sympify(exp_c).evalf())
                print(len(Y))
                print(n[i],n)
                print(vars,point)
                raise ValueError("too mang times!")
            if sympy.sympify(exp_c).evalf() == sympy.nan or sympy.sympify(exp_c).evalf() == sympy.oo or sympy.sympify(exp_c).evalf() == -sympy.oo \
                or sympy.sympify(exp_c).evalf() == sympy.zoo or sympy.sympify(exp_c).evalf().has(sympy.I):
                continue
            

            #根据分布概率取点
            y = sympy.sympify(exp_c).evalf()
            if y.is_real:
                if abs(y) < 1e101 and abs(y) > 1e-50:
                    Y.append(sympy.sympify(exp_c).evalf())
                else:
                    continue
            else:
                print(str(exp))
                print(vars,point,scope)
                print(y)
                raise ValueError("Nan y!")
            
            points.append(point)
            
        X += points
    
    return X, Y, str(expr)

#限定范围内按分布取一个点
def get_point_ran(i, scope, n_var, u_span):
    global point_generated
    random.seed(point_generated)
    v = [math.ceil(sympy.log(float(sympy.sympify(scope[f'V_{i+1}'][j][1]))/float(sympy.sympify(scope[f'V_{i+1}'][j][0])),10).evalf()) if scope[f'V_{i+1}'][j][3] == 'ulog' else u_span for j in range(0,n_var)]

    point = []
    for j in range(0,n_var):      
        max_s = float(sympy.sympify(scope[f'V_{i+1}'][j][1]))
        min_s = float(sympy.sympify(scope[f'V_{i+1}'][j][0]))
        #print(v,V)
        if scope[f'V_{i+1}'][j][3] == 'ulog':
            s = random.uniform(0,v[j])
            sample_value = sympy.sympify(min_s) * sympy.Pow(10, s)
            #print(s, sample_value, loc)

            if scope[f'V_{i+1}'][j][2] == 'I':
                sample_value = int(sample_value)
            elif scope[f'V_{i+1}'][j][2] == 'NI' or scope[f'V_{i+1}'][j][2] == 'AI':
                raise ValueError("ulog has no NI or AI!")
        elif scope[f'V_{i+1}'][j][3] == 'u' and (scope[f'V_{i+1}'][j][2] == 'I' or scope[f'V_{i+1}'][j][2] == 'NI' or scope[f'V_{i+1}'][j][2] == 'AI'):
            sample_value = random.randint(min_s, max_s) 
            #print(index,loc)
        elif scope[f'V_{i+1}'][j][3] == 'u' and (scope[f'V_{i+1}'][j][2] == 'F' or scope[f'V_{i+1}'][j][2] == 'NF' or scope[f'V_{i+1}'][j][2] == 'AF'):
            sample_value = random.uniform(min_s, max_s)
            #print(index,loc)

        point.append(sample_value)
    return point

if __name__ == "__main__":
    for field in (["phy", "bio", "che"]):
        sample(f'real/{field}_.csv', field, 200, f'points/{field}1.csv')
        sample(f'real/{field}_.csv', field, 1000, f'points/train_{field}1.csv')
    #sample('real/phy_.csv', 'phy', 1000, 'points/phy1.csv')
    #sample('real/bio_.csv', 'bio', 1000, 'points/bio1.csv')
    #sample('real/che_.csv', 'che', 1000, 'points/che1.csv')