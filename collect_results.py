import json

def read_res(dir, file, ml, field):
    res_path = '{}/{}'.format(dir, file)
    if file.endswith('.json'):
        r = read_res_json(res_path)
        r2 = dict(ml=ml,field=field,R2=r)
        return r2
    elif file.endswith('.txt'):
        r2_phy, r2_che, r2_bio = read_res_txt(res_path)
        r2_phy = dict(ml=ml,field="phy", r2=r2_phy)
        r2_che = dict(ml=ml,field="che", r2=r2_che)
        r2_bio = dict(ml=ml,field="bio", r2=r2_bio)
        return r2_phy, r2_che, r2_bio
    else:
        raise ValueError("Error file type!\n")
    
    #print(file.split('.'[0] + ':\n'))
    #print(r2)

def read_res_json(res_path):
    with open(res_path, 'r') as f:
        r2 = []
        for line in f.readlines():
            j = json.loads(line)
            r2.append(j['r2_test'])

        r2.sort()
        r2 = [(i, r2[i]) for i in range(len(r2))]
    
    return r2

def read_res_txt(res_path):
    with open(res_path, 'r') as f:
        r2_phy = []
        r2_che = []
        r2_bio = []
        case = 0
        for line in f.readlines():
            if 'r2:' not in line:
                continue
    
            if case <= 90:
                r2_phy.append(float(line.split(' ')[1].split('\n')[0]))
            elif case <= 221:
                r2_che.append(float(line.split(' ')[1].split('\n')[0]))
            else:
                r2_bio.append(float(line.split(' ')[1].split('\n')[0]))

        r2_phy.sort()
        r2_bio.sort()
        r2_che.sort()
        r2_phy = [(i, r2_phy[i]) for i in range(len(r2_phy))]
        r2_che = [(i, r2_che[i]) for i in range(len(r2_che))]
        r2_bio = [(i, r2_bio[i]) for i in range(len(r2_bio))]

    return r2_phy, r2_che, r2_bio

if __name__ == '__main__':
    save = 'results.json'
    ml ={"AdaBoostRegressor", "AFPRegressor", "BSRRegressor", "DSRRegressor", "EHCRegressor", "EPLEXRegressor", "FE_AFPRegressor", "FEATRegressor", "FFXRegressor", "GPGOMEARegressor", "gplearn", "MRGPRegressor", "OperonRegressor", "sembackpropgp"}
    for m in ml:
        for field in ("phy", "che", "bio"):
            r2 = read_res(f'/lustre/S/liyutai/srbench/results/{m}', 'results_' +field+'.json', ml, field)
            with open(save, 'w+') as f:
                json.dump(r2, f, indent=4)
                f.write('\n')

    for field in ("phy", "che", "bio"):
        r2 = read_res('/lustre/S/liyutai/end2end', 'results_' +field+'.json', "end2end", field)
        with open(save, 'w+') as f:
            json.dump(r2, f, indent=4)
            f.write('\n')

    r2_phy, r2_che, r2_bio = read_res('/lustre/S/liyutai/symbolicgpt', 'XYE_9Var_20-250Points_512EmbeddingSize_SymbolicGPT_GPT_PT_EMB_SUM_EQ_Padding_NOT_VAR_MINIMIZE', 'symbolicgpt', field=None)
    with open(save, 'w+') as f:
            json.dump(r2_phy, f, indent=4)
            f.write('\n')
            json.dump(r2_che, f, indent=4)
            f.write('\n')
            json.dump(r2_bio, f, indent=4)
            f.write('\n')
    
