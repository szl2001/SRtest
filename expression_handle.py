import sympy
from sympy import *
import pandas as pd
from constants import G,c,epsilon0,g,h,k,qe,mew0,NA,F,Bohr

def handle(field, path, save):
    collection = pd.read_csv(path)
    if field == "phy":
        constant = {G,c,epsilon0,g,h,k,qe,mew0,Bohr}
    elif field == "che":
        constant = {NA,k,g,h,F}
    elif field == "bio":
        constant = {}
    else:
        constant = {}

    after = []
    ex = []
    picked = 0
    for i, line in collection.iterrows():
        names = locals()
        equation = line['Formula']
        print(i,equation)
        exp = sympy.sympify(equation)
        exp_w = exp
        n_var = line['variables']
        if isinstance(line[f'v{n_var+1}_name'], str) or not isinstance(line[f'v{n_var}_name'], str):
            print(line[f'v{n_var+1}_name'])
            raise ValueError("Error var number!")

        vars = []
        max_scope = []
        min_scope = []
        wild = []
        scope = dict()
        for j in range(0, int(n_var)):
            vars.append(line[f'v{j+1}_name'])
            #scope[line[f'v{j+1}_name']] = [(line[f'v{j+1}_low'], line[f'v{j+1}_high'], line[f'v{j+1}_type'])]
            if line[f'v{j+1}_type'] == 'I':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],integer=True, positive=True)
                names['w'+str(j)] = sympy.Wild(line[f'v{j+1}_name'],exclude=[sin,cos,sympy.exp,tan,sinh,cosh,tanh,log,Pow],integer=True,positive=True)
            elif line[f'v{j+1}_type'] == 'F':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],real=True,positive=True)
                names['w'+str(j)] = sympy.Wild(line[f'v{j+1}_name'],exclude=[sin,cos,sympy.exp,tan,sinh,cosh,tanh,log,Pow],real=True,positive=True)
            elif line[f'v{j+1}_type'] == 'AI':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],integer=True)
                names['w'+str(j)] = sympy.Wild(line[f'v{j+1}_name'],exclude=[sin,cos,sympy.exp,tan,sinh,cosh,tanh,log,Pow],integer=True)
            elif line[f'v{j+1}_type'] == 'AF':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],real=True)
                names['w'+str(j)] = sympy.Wild(line[f'v{j+1}_name'],exclude=[sin,cos,sympy.exp,tan,sinh,cosh,tanh,log,Pow],real=True)
            elif line[f'v{j+1}_type'] == 'NI':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],integer=True, positive=False)
                names['w'+str(j)] = sympy.Wild(line[f'v{j+1}_name'],exclude=[sin,cos,sympy.exp,tan,sinh,cosh,tanh,log,Pow],integer=True,positive=False)
            elif line[f'v{j+1}_type'] == 'NF':
                names['x'+str(j)] = sympy.Symbol(line[f'v{j+1}_name'],real=True,positive=False)
                names['w'+str(j)] = sympy.Wild(line[f'v{j+1}_name'],exclude=[sin,cos,sympy.exp,tan,sinh,cosh,tanh,log,Pow],real=True,positive=False)
            else:
                raise ValueError("Blank type!")
            
            if line[f'v{j+1}_sample_type'] not in ('u','ulog'):
                raise ValueError("Error sample type!")
            
            max_scope.append((names['x'+str(j)],line[f'v{j+1}_high']))
            min_scope.append((names['x'+str(j)],line[f'v{j+1}_low']))
            
            wild.append(names['w'+str(j)])
            exp_w = exp_w.subs(line[f'v{j+1}_name'], names['w'+str(j)])

        for ch in constant:
            if ch not in vars:
                exp = exp.subs(str(ch),ch.evalf())
                exp_w = exp_w.subs(str(ch),ch.evalf())
        
        if after == []:
            picked = picked + 1
            line['Number'] = picked
            after.append(line)
            ex.append((exp_w, n_var, vars, picked, wild))
        else:
            repeat = 0
            for l in ex:
                eq_w = l[0]
                if n_var != l[1]:
                    continue
                #for j in range(0, int(n_var)):
                #    names['w'+str(j)] = sympy.Wild(l[2][j],exclude=[sin,cos,sympy.exp,tan,sinh,cosh,tanh,log,Pow])
                #print(eq_w)
                d=exp.match(eq_w)

                if d:
                    for j in d.values():
                        #去除复数及常数替换
                        if j.evalf().is_complex:
                            repeat = 0
                            break
                        else:
                            repeat = 1
                    #
                    if repeat == 1:
                        print(l[3])
                        print(':')
                        print(eq_w)
                        print(d)

                        for j in range(0, int(n_var)):
                            exp = exp.subs(line[f'v{j+1}_name'], names['x'+str(j)])
                            d=exp.match(eq_w)

                        tmp_after = after[l[3]-1].copy()
                        for j in range(0, int(l[1])):
                            #var = str(l[4][j])[0:-1]
                            new_min = (d[l[4][j]].subs(min_scope)).evalf()
                            new_max = (d[l[4][j]].subs(max_scope)).evalf()

                            try:
                                if float(new_min) > float(new_max):
                                    n = new_min
                                    new_min = new_max
                                    new_max = n
                            except:
                                for t in range(0, int(l[1])):
                                    if new_min.has(names['x'+str(j)]) and new_max.has(names['x'+str(j)]):
                                        if not names['x'+str(j)].is_positive == None:
                                            if new_max < new_min:
                                                n = new_min
                                                new_min = new_max
                                                new_max = n
                                                break
                                        else:
                                            n1 = (new_min.subs(min_scope)).evalf()
                                            n2 = (new_min.subs(max_scope)).evalf()
                                            n3 = (new_max.subs(max_scope)).evalf()
                                            n4 = (new_max.subs(min_scope)).evalf()
                                            n = [float(n1), float(n2), float(n3), float(n4)]
                                            new_max = n[n.index(max(n))]
                                            new_min = n[n.index(min(n))]
                                            break
                            #l[3][var].append((new_min,new_max))
                            if new_max == new_min:
                                repeat = 0
                                break
                            
                            if d[l[4][j]].is_integer:
                                t = 'I'
                            else:
                                t = 'F'
                            
                            if new_min != 0:
                                st = line[f'v{j+1}_sample_type']
                            else:
                                st = 'u'

                            tmp_after[f'v{j+1}_type'] += ('&' + t)
                            tmp_after[f'v{j+1}_sample_type'] += ('&' + st)
                            tmp_after[f'v{j+1}_low'] = str(tmp_after[f'v{j+1}_low']) + '&'+ str(new_min)
                            tmp_after[f'v{j+1}_high'] = str(tmp_after[f'v{j+1}_high']) + '&'+ str(new_max)
                        
                        if repeat == 1:
                            after[l[3]-1] = tmp_after
                            break
                        else:
                            continue
                
            if repeat == 0:
                picked = picked + 1
                line['Number'] = picked
                after.append(line)
                ex.append((exp_w, n_var, vars, picked, wild))

    eqs = pd.DataFrame(after)
    eqs.to_csv(save)

def add(path, save):
    collection = pd.read_csv(path)
    for i in range(11,1,-1):
        collection.insert(loc=4*i-1,column=f'v{i-1}_sample_type', value='')
    
    collection.to_csv(save,index=None)

if __name__ == "__main__":
    handle('phy','real/phy.csv','real/phy_.csv')
    handle('che','real/che.csv','real/che_.csv')
    handle('bio','real/bio.csv','real/bio_.csv')
    #add('real/bio.csv','real/bio.csv')
    #add('real/phy.csv','real/phy.csv')
    #add('real/che.csv','real/che.csv')
