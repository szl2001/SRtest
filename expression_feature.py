import sympy
from sympy import *
import pandas as pd
import re
import numpy as np
from constants import G,c,epsilon0,g,h,k,qe,mew0,NA,F,Bohr

def get_features(field, path, save):
    names = locals()

    ops = ['+','-','*','/','**','sqrt','exp','sin','cos','tan','sinh','cosh','tanh','ln','lg']
    const = ['G','c','epsilon0','g','h','k','qe','mew0','NA','F','Bohr']
    collection = pd.read_csv(path)
    if field == "phy":
        constant = {G,c,epsilon0,g,h,k,qe,mew0,Bohr}
    elif field == "che":
        constant = {NA,k,g,h,F}
    elif field == "bio":
        constant = {}
    else:
        constant = {}

    len_d = [0]
    vars_num = [0]
    fre = dict.fromkeys(ops+const,0)

    ana = ['exp', 'lg', 'ln','sqrt','**']
    for n in ana:
        names[n+'_fre'] = dict.fromkeys(ops+const+['const', 'var'],0)
        names[n+'_len'] = [0]
    sample_dis = dict(ulog=0, u=0)
    
    for i, line in collection.iterrows():
        """表达式赋值"""
        equation = line['Formula']
        #print(i,equation)
        exp = sympy.sympify(equation)
        n_var = line['variables']
        vars = []
        l = 0
        for j in range(0, int(n_var)):
            vars.append(line[f'v{j+1}_name'])
            sample_scope = str.split(line[f'v{j+1}_sample_type'], '&')
            for s in sample_scope:
                sample_dis[s] += 1

        """操作符与常数频率、表达式(操作符)长度分析"""
        for op in ops:
            a =  equation.count(op,0,len(equation))
            fre[op] += a
            l += a
        
        for con in const:
            if con not in vars:
                a =  equation.count(con,0,len(equation))
                fre[con] += a

        if l >= len(len_d):
            len_d += [0] * (l-len(len_d))
            len_d.append(1)
        else:
            len_d[l] += 1

        if n_var >= len(vars_num):
            vars_num += [0] * (n_var-len(vars_num))
            vars_num.append(1)
        else:
            vars_num[n_var] += 1

        """特殊操作符内长度、频率统计"""
        for n in ana:
            for substr in str.split(equation, n)[1:]:
                print(equation)
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
                print(substr[1:ind])
                if not sympify(substr[1:ind]).is_real:
                    for op in ops:
                        a =  substr[1:ind].count(op)
                        names[n+'_fre'][op] += a
                    for con in const:
                        if con not in vars:
                            a =  substr[1:ind].count(con)
                            names[n+'_fre'][con] += a
                    for v in vars:
                        if substr[1:ind].count(v):
                            names[n+'_fre']['var'] += 1
                            break
                else:
                    ana_len = 0
                    names[n+'_fre']['const'] += 1
                
                if ana_len >= len(names[n+'_len']):
                    names[n+'_len'] += [0] * (ana_len-len(names[n+'_len']))
                    names[n+'_len'].append(1)
                else:
                    names[n+'_len'][ana_len] += 1
                


    fre['*'] -= 2 * fre['**']
    ave_len = sum(j*len_d[j] for j in range(len(len_d)))/(i+1)
    max_len = len(len_d) - 1
    min_len = np.flatnonzero(len_d)[0]
    const_num = sum(fre[c] for c in const)

    result = dict()
    result['field'] = field
    result['vars_num'] = vars_num
    result['const_num'] = const_num
    result['sample_distribution'] = sample_dis
    result['len'] = len_d
    result['ave_len'] = ave_len
    result['max_len'] = max_len
    result['min_len'] = min_len
    result['fre'] = fre

    for n in ana:
        result[n+'_len'] = names[n+'_len']
        result[n+'_fre'] = names[n+'_fre']

    print(result)
    res = pd.Series(result).to_frame()
    print(res)
    res.to_csv(save)

if __name__ == "__main__":
    get_features('phy','real/phy_.csv','real/feature/phy_fea_.csv')
    get_features('che','real/che_.csv','real/feature/che_fea_.csv')
    get_features('bio','real/bio_.csv','real/feature/bio_fea_.csv')



    