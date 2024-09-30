import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np
import ast 

# Initialize dictionary to store data for boxplots
datasets = ['APSNG', 'Dave2', 'Keeplane', 'Distance', 'Damage', 'Ultra', 'Router']
methods = ['Tarantula', 'Ochiai', 'Naish', 'DT', 'DR', 'Ensemble']
methodsforplots = [r"$GP_T$", r"$GP_O$", r"$GP_N$", "DT", "DR", "Ensemble"]
datasetsforplots = ['AP-SNG', 'DAVE2', 'AP-TWN (R1)', 'AP-TWN (R4)', 'AP-TWN (R2)', 'AP-TWN (R3)', 'Router']
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
popntss = [[] for i in range(11)]
datasets2 = ['APSNG', 'Dave2', 'Keeplane', 'Distance', 'Damage', 'Ultra', 'Router-ind', 'Router-sum']
for i, dataset in enumerate(datasets2):
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
        
        if 'NTSS' in dataset:

            popntss[d//2 - 1].extend(pop)

        else:
            if len(pop) != 0:

                stats[method + ',' + dataset + ',' + str(d) ] = np.mean(np.abs(pop - np.mean(pop)))

            else:

                stats[method + ',' + dataset + ',' + str(d) ] = 'NA'


for h in range(len(popntss)):

    if len(popntss[h]) != 0:

        stats['DT,NTSS,' + str(h)] = np.mean(np.abs(popntss[h] - np.mean(popntss[h])))

    else:

        stats['DT,NTSS,' + str(h)] = 'NA'

print('DT done')

method = 'DR'
popntss = [[] for i in range(11)]
datasets2 = ['APSNG', 'Dave2', 'Keeplane', 'Distance', 'Damage', 'Ultra', 'Router-ind', 'Router-sum']
for i, dataset in enumerate(datasets2):
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
        
        if 'NTSS' in dataset:

            popntss[d//2 - 1].extend(pop)

        else:
            if len(pop) != 0:

                stats[method + ',' + dataset + ',' + str(d) ] = np.mean(np.abs(pop - np.mean(pop)))

            else:

                stats[method + ',' + dataset + ',' + str(d) ] = 'NA'



for h in range(len(popntss)):

    if len(popntss[h]) != 0:

        stats['DR,NTSS,' + str(h)] = np.mean(np.abs(popntss[h] - np.mean(popntss[h])))

    else:

        stats['DR,NTSS,' + str(h)] = 'NA'

print('DR done')

df = pd.DataFrame(list(stats.items()), columns=['(Method, Dataset, Theta)', 'MAD'])

df.to_excel('MAD.xlsx', index=False)
