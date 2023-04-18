import json
from expression_feature import get_features_eq
import pandas as pd
import numpy as np

def score(results, save, eva_p):
    perf = []
    eva = []
    with open(results, 'r+') as f:
        res = json.load(f)
        for i in range(len(res)):
            ml_res = res[i]
            perf_ml = dict()
            acc_score = []
            struct_score = []
            field = ml_res['field']
            model_size = []
            time = []
            eq_num = len(ml_res['R2'])
            print(ml_res)
            for r2 in ml_res['R2']:
                if r2[1] <= 0.9:
                    acc_score.append(0)
                elif r2[1] <= 0.95:
                    acc_score.append(0.1)
                elif r2[1] <= 0.99:
                    acc_score.append(0.5)
                else:
                    acc_score.append(1)

                if len(r2) > 2:
                    model_size.append(r2[4])
                    time.append(r2[5])

                    true = r2[2]
                    pred = r2[3]
                    if pred == 'not implemented' or pred == None:
                        struct_score.append(0)
                        continue

                    ops = ['**','sqrt','exp','sin','cos','tan','sinh','cosh','tanh','ln','lg','asin','acos','atan', 'abs']
                    ana = ['exp', 'lg', 'ln','sqrt','**']
                    true_fea = get_features_eq(true)
                    pred_fea = get_features_eq(pred)
                    if not true_fea or not pred_fea:
                        struct_score.append(0)
                        continue
                    p = pd.read_csv(f'/lustre/S/liyutai/srmaker/real/feature/{field}_fea.csv')
                    tmp = p.values
                    tmp = list(map(list, zip(*tmp)))
                    tmp = pd.DataFrame(tmp)
                    tmp.columns = tmp.loc[0]
                    total_fea = tmp.drop(tmp.index[0])
                    print(total_fea)
                    fre = eval(total_fea['fre'].values[0])
                    var_max = len(eval(total_fea['vars_num'].values[0])) - 1

                    true_fea['var_num'] = true_fea['var_num']/var_max
                    pred_fea['var_num'] = pred_fea['var_num']/var_max
                
                    for n in ops:
                        max = float(total_fea[n+'_num_max'].values[0])
                        if max != 0:
                            true_fea[n+'_num'] = true_fea[n+'_num']/max
                            pred_fea[n+'_num'] = pred_fea[n+'_num']/max
                        elif true_fea[n+'_num'] > max or pred_fea[n+'_num'] > max:
                            if pred_fea[n+'_num'] != 0:
                                true_fea[n+'_num'] = 0
                                pred_fea[n+'_num'] = 1

                        if n == '**':
                            pow_max = float(total_fea['pow_max'].values[0])
                            if pow_max != 0:
                                true_fea[n+'_max'] = true_fea[n+'_max']/pow_max
                                pred_fea[n+'_max'] = pred_fea[n+'_max']/pow_max
                            elif true_fea[n+'_max'] != 0 or pred_fea[n+'_max'] != 0:
                                raise ValueError(f"over {n}_max!")
                    
                    print(true, pred)
                    print(true_fea)
                    print(pred_fea)

                    true_fea_num = np.array(list(true_fea.values()))
                    pred_fea_num = np.array(list(pred_fea.values()))

                    diffsq = (true_fea_num - pred_fea_num)**2

                    if diffsq.any() > 1:
                        print(diffsq)
                        raise ValueError("sq>1")
                    elif diffsq[0] *0.5 + 0.5*sum(diffsq[1:])/len(diffsq[1:]) > 1:
                        print(diffsq)
                        raise ValueError("sum>1")

                    struct_score.append(float(1 - (diffsq[0] *0.5 + 0.5*sum(diffsq[1:])/len(diffsq[1:]))))
                else:
                    model_size.append(1000000)
                    time.append(1000000)
                    struct_score.append(0)

            score = list(0.7 * np.array(acc_score) + 0.3 * np.array(struct_score))
            perf_ml['ml'] = ml_res['ml']
            perf_ml['field'] = ml_res['field']
            perf_ml['eq_num'] = len(ml_res['R2'])
            perf_ml['acc_score'] = acc_score
            perf_ml['struct_score'] = struct_score
            perf_ml['score'] = score
            perf_ml['total_acc_score'] = sum(acc_score)
            perf_ml['total_struct_score'] = sum(struct_score)
            perf_ml['total_score'] = sum(score)
            perf_ml['evaluation'] = sum(score)/eq_num * 100
            perf_ml['model_size'] = sum(model_size)/eq_num
            perf_ml['time'] = sum(time)/eq_num
            perf.append(perf_ml)
            eva.append(dict(ml=ml_res['ml'], eq_num=eq_num,field=ml_res['field'], acc=sum(acc_score), struct=sum(struct_score), score=sum(score), evaluation= sum(score)/eq_num*100, size=sum(model_size)/eq_num, time=sum(time)/eq_num))
        
    with open(save, 'w+') as out:
        #print(perf)
        json.dump(perf, out)

    eva.sort(key=lambda x: x['evaluation'])
    e = pd.DataFrame(eva)
    e.to_csv(eva_p.split('.json')[0]+'.csv')
    with open(eva_p, 'w+') as out:
        json.dump(eva, out)
        out.write('\neva:')
        json.dump([(x['ml'],x['evaluation']) for x in eva], out)
        out.write('\nacc:')
        eva.sort(key=lambda x: x['acc'])
        json.dump([(x['ml'], x['acc']) for x in eva], out)
        out.write('\nstruct:')
        eva.sort(key=lambda x: x['struct'])
        json.dump([(x['ml'], x['struct']) for x in eva if x['struct']!=0], out)

def sort(results, save):
    perf = []
    with open(results, 'r+') as f:
        res = json.load(f)
        interval = 0.01
        for i in range(len(res)):
            ml_res = res[i]
            perf_ml = dict()
            r_num = [0]*int(1+1/interval)
            model_size = []
            time = []
            eq_num = len(ml_res['R2'])
            corrected = 0
            for r2 in ml_res['R2']:
                if r2[1] > 0.99:
                    corrected += 1
                r = 1 - r2[1]
                if r > 1:
                    r_num[-1] += 1
                else:
                    r_num[int(r/interval)] += 1

                model_size.append(r2[4])
                time.append(r2[5])

            subr2 = np.array([sum(r_num[0:i+1])/eq_num for i in range(len(r_num))])
            x = np.array([i*interval for i in range(len(r_num))])
            cof = list(np.polyfit(x,subr2,5))

            perf_ml['ml'] = ml_res['ml']
            perf_ml['field'] = ml_res['field']
            perf_ml['eq_num'] = len(ml_res['R2'])
            perf_ml['model_size'] = sum(model_size)/eq_num
            perf_ml['time'] = sum(time)/eq_num
            perf_ml['corrected'] = corrected
            perf_ml['cof'] = cof
            perf_ml['cdf'] = list(subr2)
            perf.append(perf_ml)

    perf.sort(key=lambda x: x['corrected'])
    with open(save, 'w+') as out:
        #print(perf)
        json.dump(perf, out)


if __name__ == "__main__":
    for field in ('phy', 'che', 'bio'):
        #score(f'/lustre/S/liyutai/srmaker/results_{field}.json',f'/lustre/S/liyutai/srmaker/score_{field}.json', f'/lustre/S/liyutai/srmaker/eva_{field}.json')
        sort(f'/lustre/S/liyutai/srmaker/results_{field}.json',f'/lustre/S/liyutai/srmaker/sort_{field}.json')