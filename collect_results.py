import json

def read_res(dir, file, ml, field):
    res_path = '{}/{}'.format(dir, file)
    print(res_path)
    if field:
        r = read_res_json(res_path)
        r2 = dict(ml=ml,field=field,R2=r)
        return r2
    elif field == None:
        r2_phy, r2_che, r2_bio = read_res_none_field(res_path)
        r2_phy = dict(ml=ml,field="phy", R2=r2_phy)
        r2_che = dict(ml=ml,field="che", R2=r2_che)
        r2_bio = dict(ml=ml,field="bio", R2=r2_bio)
        return r2_phy, r2_che, r2_bio
    
    #print(file.split('.'[0] + ':\n'))
    #print(r2)

def read_res_json(res_path):
    with open(res_path, 'r') as f:
        r2 = []
        j = json.load(f)
        for i in range(len(j)):
            print(j[i])
            r2.append((float(j[i]['r2_test']), j[i]['expr'], j[i]['symbolic_model'],j[i]['model_size'],j[i]['process_time']))

        r2.sort(key=lambda x: x[0])
        r2 = [(i, r2[i][0], r2[i][1], r2[i][2], r2[i][3], r2[i][4],) for i in range(len(r2))]
    
    return r2

def read_res_none_field(res_path):
    with open(res_path, 'r') as f:
        r2_phy = []
        r2_che = []
        r2_bio = []

        j = json.load(f)
        for i in range(len(j)):
            print(j[i])
    
            if i <= 90:
                r2_phy.append((float(j[i]['r2_test']), j[i]['expr'], None,float(j[i]['model_size']),float(j[i]['process_time'])))
            elif i <= 152:
                r2_bio.append((float(j[i]['r2_test']), j[i]['expr'], None,float(j[i]['model_size']),float(j[i]['process_time'])))
            else:
                r2_che.append((float(j[i]['r2_test']), j[i]['expr'], None,float(j[i]['model_size']),float(j[i]['process_time'])))

        r2_phy.sort(key=lambda x: x[0])
        r2_bio.sort(key=lambda x: x[0])
        r2_che.sort(key=lambda x: x[0])
        r2_phy = [(i, r2_phy[i][0], r2_phy[i][1], r2_phy[i][2], r2_phy[i][3], r2_phy[i][4]) for i in range(len(r2_phy))]
        r2_che = [(i, r2_che[i][0], r2_che[i][1], r2_che[i][2], r2_che[i][3], r2_che[i][4]) for i in range(len(r2_che))]
        r2_bio = [(i, r2_bio[i][0], r2_bio[i][1], r2_bio[i][2], r2_bio[i][3], r2_bio[i][4]) for i in range(len(r2_bio))]

    return r2_phy, r2_che, r2_bio

if __name__ == '__main__':
    name = locals()
    save_phy = 'results_phy.json'
    save_che = 'results_che.json'
    save_bio = 'results_bio.json'
    for field in ("phy", "che", "bio"):
        with open(name["save_"+field], 'w+') as f:
            f.write('[\n')

    ml ={"AdaBoostRegressor", "AFPRegressor", "BSRRegressor", "DSRRegressor", "EHCRegressor", "EPLEXRegressor", "FE_AFPRegressor", "FEATRegressor", "FFXRegressor", "GPGOMEARegressor", "gplearn", "OperonRegressor", "sembackpropgp"}
    for m in ml:
        for field in ("phy", "che", "bio"):
            r2 = read_res(f'/lustre/S/liyutai/srbench/results/{m}', 'results_' +field+'.json', m, field)
            print(r2)
            with open(name["save_"+field], 'a') as f:
                json.dump(r2, f, indent=4)
                f.write(',\n')

    all = {"KernelRidge", "LGBMRegressor", "LinearRegression", "MLPRegressor", "RandomForestRegressor", "XGBRegressor"}
    for m in all:
        for field in ("phy", "che", "bio"):
            r2 = read_res(f'/lustre/S/liyutai/srbench/results_sym_data/{m}', 'results_' +field+'.json', m, field)
            print(r2)
            with open(name["save_"+field], 'a') as f:
                json.dump(r2, f, indent=4)
                f.write(',\n')

    for field in ("phy", "che", "bio"):
        r2 = read_res('/lustre/S/liyutai/end2end', 'results_' +field+'.json', "end2end", field)
        #r2 = json.dumps(r2)
        with open(name["save_"+field], 'a') as f:
            json.dump(r2, f, indent=4)
            f.write(',\n')

    r2_phy, r2_che, r2_bio = read_res('/lustre/S/liyutai/symbolicgpt', 'XYE_9Var_20-250Points_512EmbeddingSize_SymbolicGPT_GPT_PT_EMB_SUM_EQ_Padding_NOT_VAR_MINIMIZE.json', 'symbolicgpt', field=None)
    for field in ("phy", "che", "bio"):
        with open(name["save_"+field], 'a') as f:
            json.dump(name["r2_"+field], f, indent=4)
            f.write('\n]')
    
