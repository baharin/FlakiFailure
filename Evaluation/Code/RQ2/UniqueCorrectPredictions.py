import pandas as pd
import ast
from statistics import mean
import numpy as np


def CheckCovered(gpochiai, dr, model):

    if model == 'Aircraft':
        gpcols = ['CoveredRun'+str(i) for i in range(1, 21)]
        drcols = ['CoveredDRRun'+str(i) for i in range(1, 21)]
    else:
        gpcols = ['CoveredgpOchiaiRUN'+str(i) for i in range(1, 21)]
        drcols = ['CovereddrRUN'+str(i) for i in range(1, 21)]
    
    covered = []

    

    for gpcol, drcol in zip(gpcols, drcols):

        failcoveredbyboth = 0
        failcoveredbynone = 0
        failcoveredbygpbutnotdr = 0
        failcoveredbydrbutnotgp = 0
        failcoveredbygpbutwrongdr = 0
        failcoveredbydrbutwronggp = 0

        passcoveredbynone = 0
        passcoveredbyboth = 0
        passcoveredbygpbutnotdr = 0
        passcoveredbydrbutnotgp = 0
        passcoveredbygpbutwrongdr = 0
        passcoveredbydrbutwronggp = 0

        for i in range(len(gpochiai.index)):
            
            try:
                reallabel = gpochiai.loc[i, 'TestOutcome']
            except:
                reallabel = gpochiai.loc[i, 'Label']

            if reallabel == 'FAIL' or reallabel == '0' or reallabel == 0:
                if ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'FAIL' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == '0' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 0:
                    if ast.literal_eval(dr.loc[i, drcol ])[0] == 'No':
                        failcoveredbygpbutnotdr = failcoveredbygpbutnotdr + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'FAIL' or ast.literal_eval(dr.loc[i, drcol])[0] == '0' or ast.literal_eval(dr.loc[i, drcol])[0] == 0:
                        failcoveredbyboth = failcoveredbyboth + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'PASS' or ast.literal_eval(dr.loc[i, drcol])[0] == '1' or ast.literal_eval(dr.loc[i, drcol])[0] == 1:
                        failcoveredbygpbutwrongdr = failcoveredbygpbutwrongdr + 1

                elif ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'No':
                    if ast.literal_eval(dr.loc[i, drcol])[0] == 'No':
                        failcoveredbynone = failcoveredbynone + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'FAIL' or ast.literal_eval(dr.loc[i, drcol])[0] == '0' or ast.literal_eval(dr.loc[i, drcol])[0] == 0:
                        failcoveredbydrbutnotgp = failcoveredbydrbutnotgp + 1

                elif ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'PASS' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == '1' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 1:
                    if ast.literal_eval(dr.loc[i, drcol])[0] == 'FAIL' or ast.literal_eval(dr.loc[i, drcol])[0] == '0' or ast.literal_eval(dr.loc[i, drcol])[0] == 0:
                        failcoveredbydrbutwronggp = failcoveredbydrbutwronggp + 1
                    

            elif reallabel == 'PASS' or reallabel == '1' or reallabel == 1:
                if ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'PASS' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == '1' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 1:
                    if ast.literal_eval(dr.loc[i, drcol])[0] == 'No':
                        passcoveredbygpbutnotdr = passcoveredbygpbutnotdr + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'PASS' or ast.literal_eval(dr.loc[i, drcol])[0] == '1' or ast.literal_eval(dr.loc[i, drcol])[0] == 1:
                        passcoveredbyboth = passcoveredbyboth + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'FAIL' or ast.literal_eval(dr.loc[i, drcol])[0] == '0' or ast.literal_eval(dr.loc[i, drcol])[0] == 0:
                        passcoveredbygpbutwrongdr = passcoveredbygpbutwrongdr + 1

                elif ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'No':
                    if ast.literal_eval(dr.loc[i, drcol])[0] == 'No':
                        passcoveredbynone = passcoveredbynone + 1
                    elif ast.literal_eval(dr.loc[i, drcol])[0] == 'PASS' or ast.literal_eval(dr.loc[i, drcol])[0] == '1' or ast.literal_eval(dr.loc[i, drcol])[0] == 1:
                        passcoveredbydrbutnotgp = passcoveredbydrbutnotgp + 1

                elif ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 'FAIL' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == '0' or ast.literal_eval(gpochiai.loc[i, gpcol])[0] == 0:
                   if ast.literal_eval(dr.loc[i, drcol])[0] == 'PASS' or ast.literal_eval(dr.loc[i, drcol])[0] == '1' or ast.literal_eval(dr.loc[i, drcol])[0] == 1:
                       passcoveredbydrbutwronggp = passcoveredbydrbutwronggp + 1
                      


        covered.append((failcoveredbyboth/len(gpochiai.index), failcoveredbynone/len(gpochiai.index), failcoveredbygpbutnotdr/len(gpochiai.index), failcoveredbydrbutnotgp/len(gpochiai.index), failcoveredbygpbutwrongdr/len(gpochiai.index), failcoveredbydrbutwronggp/len(gpochiai.index), passcoveredbyboth/len(gpochiai.index), passcoveredbynone/len(gpochiai.index), passcoveredbygpbutnotdr/len(gpochiai.index), passcoveredbydrbutnotgp/len(gpochiai.index), passcoveredbygpbutwrongdr/len(gpochiai.index), passcoveredbydrbutwronggp/len(gpochiai.index)))

    coveredavg = tuple(mean(values) for values in zip(*covered))


    return coveredavg, covered



results = pd.DataFrame(columns=['Theta', 'Model', 'FailCoveredbyBoth', 'FailCoveredbyNone', 'FailCoveredbyGPbutnotDR', 'FailCoveredbyDRbutnotGP', 'FailCoveredbyGPbutWrongDR', 'FailCoveredbyDRbutWrongGP', 'PassCoveredbyBoth', 'PassCoveredbyNone', 'PassCoveredbyGPbutnotDR', 'PassCoveredbyDRbutnotGP', 'PassCoveredbyGPbutWrongDR', 'PassCoveredbyDRbutWrongGP'])


models = ['AP=SNG', 'Dave2', 'R1', 'R2', 'R3', 'R4', 'Aircraft', 'Router']

allcovered = [[] for i in range(11)]

allcoveredmodel = [[] for i in range(8)]

for t, theta in enumerate(['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']):
    for m, model in enumerate(models):
    
        gpochiai = pd.read_excel('path_to_file\\GP-Ochiai-coveredpoints-'+model+'-theta'+theta+'-testset.xlsx')
        dr = pd.read_excel('path_to_file\\dr-coveredpoints-'+model+'-theta'+theta+'-testset.xlsx')

        coveredavg, covered = CheckCovered(gpochiai, dr, model)
        allcovered[t].append(covered)
        
        results.loc[results.shape[0]] = [theta, model, coveredavg[0], coveredavg[1], coveredavg[2], coveredavg[3], coveredavg[4], coveredavg[5], coveredavg[6], coveredavg[7], coveredavg[8], coveredavg[9], coveredavg[10], coveredavg[11]]           

results.to_excel('uniquecorrectpredictions.xlsx')
