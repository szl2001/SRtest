import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from adjustText import adjust_text

def graphy(record, save, field):
    if field == "phy":
        field = "Physics"
    elif field == "che":
        field = "Chemistry"
    elif field == "bio":
        field = "Biology"
    plt.figure(figsize=(18,15))
    plt.xlim((-0.1,1.1))
    plt.ylabel('Cumulative expression (%)',fontdict=dict(size=20))
    plt.xlabel('1 - R^2',fontdict=dict(size=20))
    plt.title(f'Cumulative Distribution of the Number of \nExpressions on R^2 for {field}', y=1.02,fontdict=dict(size=30,weight='bold'), verticalalignment='baseline')
    for i in range(len(record)):
        ml = record[i]["ml"]
        cof = record[i]["cof"]
        eq = np.poly1d(np.array(cof))
        x = np.linspace(0, 1.02, 102)
        #index = (-1)**(i%2)
        if i%3 == 2:
            linestyle = "solid"
            marker = '1'
        elif i%3 == 1: 
            linestyle = (0,(3,1,1,1,1,1))
            marker = None
        elif i%3 == 0:
            linestyle = (0,(5,10))
            marker = None
        else:
            linestyle = "dotted"
        plt.plot(x, eq(x), label=ml, linestyle=linestyle, marker=marker)
        #text.append(plt.text(0.01, eq(0.01), ml))
        #arrow.append(plt.annotate(ml, xy=(0.01,eq(0.01)), xytext=(0.1+index*0.2, eq(0.01)), arrowprops=dict(arrowstyle='->', lw= 1, color='red')))
        #arrow.append(plt.annotate(ml, xy=(0.9,eq(0.9)), xytext=(0.9+index*0.2, eq(0.9)), arrowprops=dict(arrowstyle='->', lw= 1, color='red')))
    
    #adjust_text(text,arrowprops=dict(arrowstyle='->', lw= 1, color='red'))
    #adjust_text(arrow,lim=500,expand_text=(1.3,1.35))
    #adjust_text(text,lim=1500,expand_text=(1.4,1.4),force_text=(0.1,0.5))
    if field == "Biology":
        plt.legend(loc="lower right")
        plt.vlines([0.01], -0.1, 1, linestyles='dashed', colors='red')
        plt.text(-0.05, -0.13, '1 - R^2 = 0.01',fontdict=dict(size=18))
        plt.vlines([0.1], -0.1, 1, linestyles='dashed', colors='red')
        plt.text(0.11, -0.05, '1 - R^2 = 0.1',fontdict=dict(size=18))
        plt.vlines([0.9], -0.1, 1, linestyles='dashed', colors='red')
        plt.text(0.74, -0.08, '1 - R^2 = 0.9',fontdict=dict(size=18))
    else:
        plt.legend(loc="upper left")
        plt.vlines([0.01], -0.1, 0.5, linestyles='dashed', colors='red')
        plt.text(-0.05, -0.13, '1 - R^2 = 0.01',fontdict=dict(size=18))
        plt.vlines([0.1], -0.1, 0.6, linestyles='dashed', colors='red')
        plt.text(0.11, -0.05, '1 - R^2 = 0.1',fontdict=dict(size=18))
        plt.vlines([0.9], -0.1, 0.9, linestyles='dashed', colors='red')
        plt.text(0.83, -0.13, '1 - R^2 = 0.9',fontdict=dict(size=18))
    plt.savefig(save)
    plt.clf()

if __name__ == "__main__":
    for field in ('phy', 'che', 'bio'):
        with open(f'/lustre/S/liyutai/srmaker/sort_{field}.json', 'r+') as f:
            sort = json.load(f)
            graphy(sort,f'/lustre/S/liyutai/srmaker/sort_{field}.png', field)