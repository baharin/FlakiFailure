import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
import ast 

# Initialize dictionary to store data for boxplots
datasets = ['APSNG', 'Dave2', 'R1', 'R4', 'R2', 'R3', 'Router', 'Aircraft']
methods = ['Tarantula', 'Ochiai', 'Naish', 'DT', 'DR', 'Ensemble']
stats = {}
data_for_plot = {dataset: {method: [] for method in methodsforplots} for dataset in datasetsforplots}

#GP
for k, method in enumerate(methods):
    if method == 'Tarantula' or method =='Ochiai' or method == 'Naish':
        for i, dataset in enumerate(datasets):
            for d in range(2, 23, 2):
                pop = []
                for hh in range(10):
                    data = pd.read_excel('...\\path_to_file\\GPAccuracyInconclu.xlsx', 
                                    sheet_name='dataset'+str(hh))
                    for run in range(1, 21):
                        aar = ast.literal_eval(data.loc[i*72 + k*24 + d, 'RUN'+str(run)])[0]
                        if aar == 1:
                            continue
                        else:
                            aa = (1 - ast.literal_eval(data.loc[i*72 + k*24 + d, 'RUN'+str(run)])[0]) * ast.literal_eval(data.loc[i*72 + k*24 + d, 'RUN'+str(run)])[1]
                            pop.append(aa)

                pop = [x for x in pop if not math.isnan(x)]

                if len(pop) != 0:

                    stats[method + ',' + dataset + ',' + str(d) ] = np.mean(np.abs(pop - np.mean(pop)))

                else:
                    stats[method + ',' + dataset + ',' + str(d) ] = 'NA'
            
print('GP done')

method = 'Ensemble'
for i, dataset in enumerate(datasets):
    for d in range(2, 23, 2):
        pop = []
        for hh in range(10):
            data = pd.read_excel('...\\path_to_file\\'+method+'AccuracyInconclu.xlsx', sheet_name='dataset'+str(hh))
            for run in range(1, 21):
                aar = ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[0]
                if aar == 1:
                    continue
                else:
                    aa = (1 - ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[0]) * ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[1]
                    pop.append(aa) 
        
        pop = [x for x in pop if not math.isnan(x)]

        if len(pop) != 0 :

            stats[method + ',' + dataset + ',' + str(d) ] = np.mean(np.abs(pop - np.mean(pop)))

        else:

            stats[method + ',' + dataset + ',' + str(d) ] = 'NA'

print('ENS done')     

method = 'DT'
for i, dataset in enumerate(datasets):
    for d in range(2, 23, 2):
        pop = []
        for hh in range(10):
            data = pd.read_excel('...\\path_to_file\\'+method+'AccuracyInconclu.xlsx', sheet_name='dataset'+str(hh))
            for run in range(1, 21):
                aar = ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[0]
                if aar == 1:
                    continue
                else:
                    aa = (1 - ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[0]) * ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[1]
                    pop.append(aa) 
        
        pop = [x for x in pop if not math.isnan(x)]

        if len(pop) != 0 :

            stats[method + ',' + dataset + ',' + str(d) ] = np.mean(np.abs(pop - np.mean(pop)))

        else:

            stats[method + ',' + dataset + ',' + str(d) ] = 'NA'

print('DT done')  

method = 'DR'
for i, dataset in enumerate(datasets):
    for d in range(2, 23, 2):
        pop = []
        for hh in range(10):
            data = pd.read_excel('...\\path_to_file\\'+method+'AccuracyInconclu.xlsx', sheet_name='dataset'+str(hh))
            for run in range(1, 21):
                aar = ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[0]
                if aar == 1:
                    continue
                else:
                    aa = (1 - ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[0]) * ast.literal_eval(data.loc[i*24 + d, 'RUN'+str(run)])[1]
                    pop.append(aa) 
        
        pop = [x for x in pop if not math.isnan(x)]

        if len(pop) != 0 :

            stats[method + ',' + dataset + ',' + str(d) ] = np.mean(np.abs(pop - np.mean(pop)))

        else:

            stats[method + ',' + dataset + ',' + str(d) ] = 'NA'

print('DR done')  

df = pd.DataFrame(list(stats.items()), columns=['(Method, Dataset, Theta)', 'MAD'])

df.to_excel('AAD.xlsx', index=False)
