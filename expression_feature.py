import sympy
from sympy import *
import pandas as pd
import re
import numpy as np
from constants import G,c,epsilon0,g,h,k,qe,mew0,NA,F,Bohr,alpha,me
from e2elang.opcode import const_map

def get_features(field, path, save):
    def isfloat(str):
        try:
            float(str)
            return 1
        except:
            return 0

    names = locals()

    ops = ['+','-','*','/','**','sqrt','exp','sin','cos','tan','sinh','cosh','tanh','ln','lg','asin','acos','atan', 'abs']
    const = ['G','c','epsilon0','g','h','k','qe','mew0','NA','F','Bohr', 'pi', 'alpha', 'me']
    collection = pd.read_csv(path)
    if field == "phy":
        constant = {G,c,epsilon0,g,h,k,qe,mew0,Bohr,alpha,me}
    elif field == "che":
        constant = {NA,k,g,h,F}
    elif field == "bio":
        constant = {}
    else:
        constant = {}

    len_d = [0]
    biop = [0]
    unop = [0]
    vars_num = [0]
    biop_coff = []
    unop_coff = []
    pow_max = 0
    fre = dict.fromkeys(ops+const,0)
    number_num = 0

    ana = ['exp', 'lg', 'ln','sqrt','**']
    for n in ana:
        names[n+'_fre'] = dict.fromkeys(ops+const+['const', 'var'],0)
        names[n+'_len'] = [0]
        names[n+'_num_max'] = 0
    sample_dis = dict(ulog=0, u=0)

    for n in ops:
        names[n+'_num_max'] = 0

    for i, line in collection.iterrows():
        """表达式赋值"""
        equation = line['Formula']
        #print(i,equation)
        exp = sympy.sympify(equation)
        n_var = line['variables']
        vars = []
        l = 0
        bi = 0
        un = 0
        for j in range(0, int(n_var)):
            vars.append(line[f'v{j+1}_name'])
            sample_scope = str.split(line[f'v{j+1}_sample_type'], '&')
            for s in sample_scope:
                sample_dis[s] += 1

        """操作符与常数频率、表达式(操作符)长度分析"""
        for op in ops:
            if op == '*':
                a = equation.count(op,0,len(equation)) - 2*equation.count('**',0,len(equation))
            elif op in ops[7:10]:
                a = equation.count(op,0,len(equation)) - equation.count(ops[ops.index(op)+3],0,len(equation)) - equation.count(ops[ops.index(op)+8],0,len(equation))
            else:
                a =  equation.count(op,0,len(equation))
            fre[op] += a
            if a > names[op+'_num_max']:
                names[op+'_num_max'] = a
            l += a
            if op in ops[0:5]:
                bi += a
            else:
                un += a
        biop_coff.append(bi/int(n_var))
        unop_coff.append(un/int(n_var))
        
        sub = [equation]
        for op in ops+const+['(', ')']:
            tmp_sub = []
            for substr in sub:
                tmp_sub += str.split(substr, op)
            sub = tmp_sub
        number_num += sum([1 if isfloat(substr) and substr not in const and substr not in vars else 0 for substr in sub])

        for con in const:
            exp = exp.subs(con, const_map[con])
            if con not in vars and exp.has(const_map[con]):
                a =  equation.count(con,0,len(equation))
                #print(equation, a, vars)
                fre[con] += a

        if l >= len(len_d):
            len_d += [0] * (l-len(len_d))
            len_d.append(1)
            print(l,equation)
        else:
            len_d[l] += 1

        if bi >= len(biop):
            biop += [0] * (bi-len(biop))
            biop.append(1)
        elif bi != 0:
            biop[bi] += 1

        if un >= len(unop):
            unop += [0] * (un-len(unop))
            unop.append(1)
        elif un != 0:
            unop[un] += 1

        if n_var >= len(vars_num):
            vars_num += [0] * (n_var-len(vars_num))
            vars_num.append(1)
        else:
            vars_num[n_var] += 1

        """特殊操作符内长度、频率统计"""
        for n in ana:
            for substr in str.split(equation, n)[1:]:
                #print(equation)
                r = 0
                ind = 0
                ana_len = 0

                if n == '**':
                    if substr[0] != '(':
                        for op in ops:
                            substr = str.split(substr, op)[0]
                        substr = str.split(substr, ')')[0]
                        substr = '$' + substr 
                        ind = len(substr)

                for ch in substr:
                    if ch == '(':
                        r += 1
                    elif ch == ')':
                        r -= 1
                    elif ch in ops:
                        ana_len += 1

                    if r == 0:
                        break
                    else:
                        ind += 1
                #print(substr[1:ind])
                if not sympify(substr[1:ind]).is_real:
                    for op in ops:
                        a =  substr[1:ind].count(op)
                        names[n+'_fre'][op] += a
                    for con in const :
                        if con not in vars and exp.has(const_map[con]):
                            a =  substr[1:ind].count(con)
                            names[n+'_fre'][con] += a
                    for v in vars:
                        if substr[1:ind].count(v):
                            names[n+'_fre']['var'] += 1
                            break
                else:
                    ana_len = 0
                    names[n+'_fre']['const'] += 1
                    if n == '**' and pow_max < sympify(substr[1:ind]):
                        pow_max = sympify(substr[1:ind])
                
                if ana_len >= len(names[n+'_len']):
                    names[n+'_len'] += [0] * (ana_len-len(names[n+'_len']))
                    names[n+'_len'].append(1)
                else:
                    names[n+'_len'][ana_len] += 1
                


    #fre['*'] -= 2 * fre['**']
    #fre['sin'] -= (fre['asin'] + fre['sinh'])
    #fre['cos'] -= (fre['acos'] + fre['cosh'])
    #fre['tan'] -= (fre['atan'] + fre['tanh'])
    ave_len = sum(j*len_d[j] for j in range(len(len_d)))/(i+1)
    max_len = len(len_d) - 1
    min_len = np.flatnonzero(len_d)[0]
    const_num = sum(fre[c] for c in const)

    result = dict()
    result['field'] = field
    result['eq_num'] = len(collection)
    result['vars_num'] = vars_num
    result['const_num'] = const_num
    result['number_num'] = number_num
    result['sample_distribution'] = sample_dis
    result['len'] = len_d
    result['ave_len'] = ave_len
    result['max_len'] = max_len
    result['min_len'] = min_len
    result['biop'] = biop
    result['unop'] = unop
    result['biop_coff'] = biop_coff
    result['unop_coff'] = unop_coff
    result['fre'] = fre

    for n in ana:
        result[n+'_len'] = names[n+'_len']
        result[n+'_fre'] = names[n+'_fre']
    for n in ops:
        result[n+'_num_max'] = names[n+'_num_max']
    
    result['pow_max'] = pow_max

    print(result)
    res = pd.Series(result).to_frame()
    print(res)
    res.to_csv(save)

def get_features_eq(eq):
    features = dict()
    ops = ['**','sqrt','exp','sin','cos','tan','sinh','cosh','tanh','ln','lg','asin','acos','atan', 'abs']
    #exp = sympy.sympify(eq)
    print(eq)
    
    try:
        """number of variables"""
        if eq.find('X') >= 0:
            var_x = 'X'
        elif eq.find('x_') >= 0:
            var_x = 'x_'
        elif eq.find('x[') >= 0:
            var_x = 'x['
        elif eq.find('x') >= 0 or sympify(eq).is_real:
            var_x = 'x'
        else:
            var_x = 'x'
            print(eq)
        #raise ValueError('Undefine x!\n')
    except:
        eq = eq.replace('|', '')
        if eq.find('aq') >= 0:
            eq = eq.replace('aq', '/')
        if eq.find('plog') >= 0:
            eq = eq.replace('plog', 'log')

        if eq.find('X') >= 0:
            var_x = 'X'
        elif eq.find('x_') >= 0:
            var_x = 'x_'
        elif eq.find('x[') >= 0:
            var_x = 'x['
        elif eq.find('x') >= 0 or sympify(eq).is_real:
            var_x = 'x'
        else:
            var_x = 'x'
            print(eq)
    
    var_num = 0
    var = set()
    for substr in eq.split(var_x)[1:]:
        if substr[0].isdigit() and (len(substr) == 1 or not substr[1].isdigit()):
            var.add(var_x + substr[0] if var_x != 'x[' else var_x + substr[0] + ']')
    
    var_num = len(var)
    if var_x != 'x':
        for i in range(var_num):
            eq = eq.replace(list(var)[i], f'x{i}')

    features['var_num'] = var_num

    if eq.find('[') >= 0 or eq.find(']'):
        eq = eq.replace('[', '(')
        eq = eq.replace(']', ')')
    
    """op"""
    ana = ['exp', 'lg', 'ln','sqrt','**']
    for n in ops:
        if n in ana:
            features[n+'_var'] = False
            if n == "**":
                features[n+'_max'] = 0
            if eq.find(n) >= 0:
                features[n+'_num'] = len(eq.split(n)) - 1
                for substr in eq.split(n)[1:]:
                    ind = 0
                    if substr[0] != '(':
                        for op in ops:
                            substr = str.split(substr, op)[0]
                        substr = str.split(substr, ')')[0]
                        substr = str.split(substr, ']')[0]
                        substr = '$' + substr 
                        ind = len(substr)
                    else:
                        r = 0
                        for ch in substr:
                            if ch == '(':
                                r += 1
                            elif ch == ')':
                                r -= 1

                            if r == 0:
                                break
                            else:
                                ind += 1
                    print(n)
                    print(substr, substr[1:ind])
                    print(eq)
                    try:
                        if not substr[ind-1] in ops + ['(', ')']:
                            sympify(substr[1:ind])
                    except:
                        return None
                    if substr[ind-1] in ops + ['(', ')']  or not sympify(substr[1:ind]).is_real:
                        features[n+'_var'] = True
                        break
                    elif n == "**" and sympify(substr[1:ind]) > features[n+'_max']:
                        features[n+'_max'] = sympify(substr[1:ind])

            else:
                features[n+'_num'] = 0
        else:
            if n == '*':
                features[n+'_num'] = eq.count(n,0,len(eq)) - 2*eq.count('**',0,len(eq))
            elif n in ops[3:6]:
                features[n+'_num'] = eq.count(n,0,len(eq)) - eq.count(ops[ops.index(n)+3],0,len(eq)) - eq.count(ops[ops.index(n)+8],0,len(eq))
            else:
                features[n+'_num'] =  eq.count(n,0,len(eq))

    return features

if __name__ == "__main__":
    get_features('phy','real/phy_.csv','real/feature/phy_fea.csv')
    get_features('che','real/che_.csv','real/feature/che_fea.csv')
    get_features('bio','real/bio_.csv','real/feature/bio_fea.csv')



    