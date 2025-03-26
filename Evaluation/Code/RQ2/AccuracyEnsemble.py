import pandas as pd

def CalculateInconclusiveness(coveredpoints, technique):

  cols = ['RUN'+str(i) for i in range(1, 21)]

  inconclus = []

  for col in cols:

    inconclu = 0

    for i in range(len(coveredpoints.index)):

      if ast.literal_eval(coveredpoints.loc[i, 'Covered'+technique+col])[0] == 'No':

        inconclu = inconclu + 1

    inconclus.append(inconclu/len(coveredpoints.index))

  return inconclus

def CalculatePerformance(coveredpoints, technique, inconclus, model):


  cols = ['RUN'+str(i) for i in range(1, 21)]

  accs = []

  falsefailss = []
  falsepassess = []

  for ind, col in enumerate(cols):

    inconclu = inconclus[ind]

    if inconclu == 1:

      accs.append(-1)
      falsefailss.append(-1)
      falsepassess.append(-1)
      continue


    inconclu = 0

    for i in range(len(coveredpoints.index)):

      if ast.literal_eval(coveredpoints.loc[i, 'Covered'+technique+col])[0] == 'No':

        inconclu = inconclu + 1

    numberofcoveredpoints = len(coveredpoints.index) - inconclu

    truefails = 0
    falsefails = 0
    truepasses = 0
    falsepasses = 0

    for i in range(len(coveredpoints.index)):

      if ast.literal_eval(coveredpoints.loc[i, 'Covered'+technique+col])[0] == 'FAIL':

        if model == 'APSNG' or model == 'Dave2':

          if coveredpoints.loc[i, 'TestOutcome'] == 'FAIL':

            truefails = truefails + 1

          elif coveredpoints.loc[i, 'TestOutcome'] == 'PASS':

            falsefails = falsefails +  1

        else:

          if coveredpoints.loc[i, 'Label'] == 0:

            truefails = truefails + 1

          elif coveredpoints.loc[i, 'Label'] == 1:

            falsefails = falsefails +  1

      elif ast.literal_eval(coveredpoints.loc[i, 'Covered'+technique+col])[0] == 'PASS':

        if model == 'APSNG' or model == 'Dave2':

          if coveredpoints.loc[i, 'TestOutcome'] == 'PASS':

            truepasses = truepasses + 1

          elif coveredpoints.loc[i, 'TestOutcome'] == 'FAIL':

            falsepasses = falsepasses +  1

        else:

          if coveredpoints.loc[i, 'Label'] == 1:

            truepasses = truepasses + 1

          elif coveredpoints.loc[i, 'Label'] == 0:

            falsepasses = falsepasses +  1


    accuracy = (truefails + truepasses)/(truefails + truepasses + falsefails + falsepasses)

    accs.append(accuracy)
    falsefailss.append(falsefails/numberofcoveredpoints)
    falsepassess.append(falsepasses/numberofcoveredpoints)


  return accs, falsepassess, falsefailss

import ast

models = ['APSNG', 'Dave2', 'R1', 'R4', 'R2', 'R3', 'Router', 'Aircraft']

withorwithout = ['dataset'+str(hh) for hh in range(0, 10)]

theta_values = ['0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']



for w in withorwithout:
  results = pd.DataFrame(columns = ['RUN'+str(i) for i in range(1, 21)])
  
  for model in models:
    
    for theta in theta_values:

      coveredpoints = pd.read_excel('...\\path_to_file\\ensemble'+'-coveredpoints-'+model+ '-theta' + theta + '-testset.xlsx', sheet_name = w)

      indexx = results.shape[0]

      dtinconclu = CalculateInconclusiveness(coveredpoints, 'Ensemble')

      dtaccuracy, dtfalsepasses, dtfalsefails = CalculatePerformance(coveredpoints, 'Ensemble', dtinconclu, model)


      for i in range(len(dtinconclu)):
        results.loc[indexx, 'RUN'+str(i+1)] = str((dtinconclu[i], dtaccuracy[i], dtfalsepasses[i], dtfalsefails[i]))


      results.loc[indexx + 1] = [None] * results.shape[1]


    results.loc[indexx + 2] = ['*****'] * results.shape[1]

  if w == 'dataset0':

    with pd.ExcelWriter('EnsembleAccuracyInconclu.xlsx', engine='openpyxl', mode='w') as writer:
      results.to_excel(writer, sheet_name=w, index=False)
  
  else:

    with pd.ExcelWriter('EnsembleAccuracyInconclu.xlsx', engine='openpyxl', mode='a') as writer:
      results.to_excel(writer, sheet_name=w, index=False)
