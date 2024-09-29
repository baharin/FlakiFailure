from pandas.core import frame
import re
import pandas as pd
import ast

def PreprocessDataWithout(data, rep):

  i = 0
  j = 0

  newdata = pd.DataFrame(columns = ["TIN 0 Req-BW", "TIN 1 Req-BW", "TIN 2 Req-BW", "TIN 3 Req-BW", "TIN 4 Req-BW", "TIN 5 Req-BW", "TIN 6 Req-BW", "TIN 7 Req-BW", 'TIN5+TIN6+TIIN7', 'Fitness'])

  while i < len(data.index):

    newdata.loc[j, 'TIN 0 Req-BW'] = data.loc[i, 'TIN 0 Req-BW']
    newdata.loc[j, 'TIN 1 Req-BW'] = data.loc[i, 'TIN 1 Req-BW']
    newdata.loc[j, 'TIN 2 Req-BW'] = data.loc[i, 'TIN 2 Req-BW']
    newdata.loc[j, 'TIN 3 Req-BW'] = data.loc[i, 'TIN 3 Req-BW']
    newdata.loc[j, 'TIN 4 Req-BW'] = data.loc[i, 'TIN 4 Req-BW']
    newdata.loc[j, 'TIN 5 Req-BW'] = data.loc[i, 'TIN 5 Req-BW']
    newdata.loc[j, 'TIN 6 Req-BW'] = data.loc[i, 'TIN 6 Req-BW']
    newdata.loc[j, 'TIN 7 Req-BW'] = data.loc[i, 'TIN 7 Req-BW']

    newdata.loc[j, 'TIN5+TIN6+TIN7'] = data.loc[i, 'TIN 5 Req-BW'] + data.loc[i, 'TIN 6 Req-BW'] + data.loc[i, 'TIN 7 Req-BW']

    newdata.loc[j, 'Fitness'] = data.loc[i, 'Fitness']

    newdata.loc[j, 'Label'] = data.loc[i, 'Label']

    i = i + 1

    j = j + 1

  return newdata

def PreprocessRule(df):

  cols = ['Run'+str(i) for i in range(1, 21)]

  for hhh in range(len(df.index)):

    for col in cols:

      rulee = df.loc[hhh, col]

      if rulee == '' or rulee == None or rulee == 'NaN' or type(rulee) == float :

        continue

      vars = ExtractBounds(rulee)

      listt = []

      for var in vars:

        if var == 'TIN0Req-BW':
          var1 = 'TIN 0 Req-BW'
        elif var == 'TIN1Req-BW':
          var1 = 'TIN 1 Req-BW'
        elif var == 'TIN2Req-BW':
          var1 = 'TIN 2 Req-BW'
        elif var == 'TIN3Req-BW':
          var1 = 'TIN 3 Req-BW'
        elif var == 'TIN4Req-BW':
          var1 = 'TIN 4 Req-BW'
        elif var == 'TIN5Req-BW':
          var1 = 'TIN 5 Req-BW'
        elif var == 'TIN6Req-BW':
          var1 = 'TIN 6 Req-BW'
        elif var == 'TIN7Req-BW':
          var1 = 'TIN 7 Req-BW'
        else:
          var1 = var

        if vars[var][2] == 'greater':
          t = ('greater_than_func', var1, vars[var][0])
          listt.append(t)
        elif vars[var][2] == 'smaller':
          t = ('less_than_func', var1, vars[var][0])
          listt.append(t)
        elif vars[var][2] == 'between':
          t = ('greater_than_func', var1, vars[var][0])
          listt.append(t)
          t = ('less_than_func', var1, vars[var][1])
          listt.append(t)
        elif vars[var][2] == 'equal':
          t = ('equal_to', var1, vars[var][0])
          listt.append(t)

      df.at[hhh, col] = str(listt)

  return df

def ExtractBounds(rule):

  rule = rule[1:-1].split('^')


  dictt = {}

  for i in range(len(rule)):

    if rule[i].find('>') != -1:

      dictt[rule[i][:rule[i].find('=')]] = [float(rule[i][rule[i].find('=')+2 : len(rule[i])]), "", "greater"]

    elif rule[i].find('<') != -1:

      dictt[rule[i][:rule[i].find('=')]] = [float(rule[i][rule[i].find('<')+1 : len(rule[i])]), "", "smaller"]

    elif rule[i].find('-') != -1:

      for k in range(rule[i].find('=')+2, len(rule[i])):
        if rule[i][k] == '-':
          a = rule[i][rule[i].find('=')+1: k]
          k = k
          break

      dictt[rule[i][:rule[i].find('=')]] = [float(a), float(rule[i][k+1:len(rule[i])]), "between"]

    elif rule[i].find('=') != -1:

      dictt[rule[i][:rule[i].find('=')]] = [float(rule[i][rule[i].find('=')+1 : len(rule[i])]), "", "equal"]

  return dictt



def FindGroups(withorwithout, df):

  groups = []

  group = []
  count = 0
  i = 0
  while i <len(df.index):
    group = []
    while i < len(df.index) and (not pd.isna(df.loc[i, withorwithout])):

      group.append(df.loc[i, withorwithout])
      count = count + 1
      i = i + 1

    if len(group) != 0 :
      groups.append(group)

    i = i + 1

  return groups

def ExtractRanges(rule):

  dictt = {'ARG5+ARG6+ARG7': [0, 1000], 'ARG0': [0, 400], 'ARG1': [0, 350], 'ARG2': [0, 306],'ARG3': [0, 267],'ARG4': [0, 234],'ARG5': [0, 205],'ARG6': [0, 179],'ARG7': [0, 157]}

  for i in range(len(rule)):

    if rule[i][0] == 'greater_than_func':

      dictt[rule[i][1]][0] = float(rule[i][2]) + 0.1  #because the func is >

    elif rule[i][0] == 'less_than_func':

      dictt[rule[i][1]][1] = float(rule[i][2]) - 0.1 #because the func is <

  return dictt



def ExtractVars(rulee):

  pattern = r'ARG\d+'

  return re.findall(pattern, rulee)


def ExtractValue(rulee):

  pattern = r'\d+\.\d+'

  return re.findall(pattern, rulee)

def ExtractVarsandValues(rule):

  varsandvalues = []

  if rule.find('greater') != -1:
    varsandvalues.append('greater')
  else:
    varsandvalues.append('less')

  vars = ExtractVars(rule)

  values = ExtractValue(rule)

  varsandvalues.append(vars)

  varsandvalues.append(values[0])

  return varsandvalues


def CalculatePerformance(df, dataset):

  cols = ['Run'+str(i) for i in range(1, 21)]

  for hhh in range(len(df.index)):

    for col in cols:


      if  type(df.loc[hhh, col]) == float or df.loc[hhh, col][0] == '' or df.loc[hhh, col] == '[]':
        df.loc[hhh, col] = ['']
        continue
    
      dt  = False

      try: #rule comes from DT/DR
        rule = ast.literal_eval(df.loc[hhh, col])

        ranges = ExtractRanges(rule)

        dt = True

      except: #rule comes from gp

        rule = df.loc[hhh, col]
        ranges = ExtractVarsandValues(rule)


      truepoints = 0

      countfails = 0
      countpasses = 0

      for h in range(len(dataset.index)):

        if dt == True:
          
          if ranges['ARG0'][0] <= dataset.loc[h, 'TIN 0 Req-BW'] <= ranges['ARG0'][1] and ranges['ARG1'][0] <= dataset.loc[h, 'TIN 1 Req-BW'] <= ranges['ARG1'][1] and ranges['ARG2'][0] <= dataset.loc[h, 'TIN 2 Req-BW'] <= ranges['ARG2'][1] and ranges['ARG3'][0] <= dataset.loc[h, 'TIN 3 Req-BW'] <= ranges['ARG3'][1] and ranges['ARG4'][0] <= dataset.loc[h, 'TIN 4 Req-BW'] <= ranges['ARG4'][1] and ranges['ARG5'][0] <= dataset.loc[h, 'TIN 5 Req-BW'] <= ranges['ARG5'][1] and ranges['ARG6'][0] <= dataset.loc[h, 'TIN 6 Req-BW'] <= ranges['ARG6'][1] and ranges['ARG7'][0] <= dataset.loc[h, 'TIN 7 Req-BW'] <= ranges['ARG7'][1] and ranges['ARG5+ARG6+ARG7'][0] <= dataset.loc[h, 'ARG5+ARG6+ARG7'] <= ranges['ARG5+ARG6+ARG7'][1]:
            
            truepoints = truepoints + 1
            if dataset.loc[h, 'Label'] == 0:

                countfails = countfails + 1
                print('now countfail is ', countfails)
            else:
                countpasses = countpasses + 1
        
        else:

            if len(ranges[1]) == 1: #the formula is either x > num or x < num. there is only one variable

                if ranges[0] == 'greater':

                    if float(dataset.loc[h, 'TIN '+ ranges[1][0][-1] + ' Req-BW']) > float(ranges[2]):

                        truepoints = truepoints + 1

                        if dataset.loc[h, 'Label'] == 0:

                            countfails = countfails + 1

                        elif dataset.loc[h, 'Label'] == 1:

                            countpasses = countpasses + 1

                else:

                    if float(dataset.loc[h, 'TIN '+ ranges[1][0][-1] + ' Req-BW']) < float(ranges[2]):

                        truepoints = truepoints + 1

                        if dataset.loc[h, 'Label'] == 0:

                            countfails = countfails + 1

                        elif dataset.loc[h, 'Label'] == 1:

                            countpasses = countpasses + 1

            else:

                if ranges[0] == 'greater':

                    sums = 0
                    for kk in range(len(ranges[1])):

                        sums = sums +  float(dataset.loc[h, 'TIN ' + ranges[1][kk][-1] + ' Req-BW'])

                    if sums > float(ranges[2]):

                        truepoints = truepoints + 1

                        if dataset.loc[h, 'Label'] == 0:

                            countfails = countfails + 1

                        elif dataset.loc[h, 'Label'] == 1:

                            countpasses = countpasses + 1

                else:
                    sums = 0
                    for kk in range(len(ranges[1])):

                        sums = sums +  float(dataset.loc[h, 'TIN ' + ranges[1][kk][-1] + ' Req-BW'])

                    if sums < float(ranges[2]):

                        truepoints = truepoints + 1

                        if dataset.loc[h, 'Label'] == 0:

                            countfails = countfails + 1
                        
                        elif dataset.loc[h, 'Label'] == 1:

                            countpasses = countpasses + 1


      if truepoints != 0 :
        # print('yes')
        fp = countfails / truepoints
        pp = countpasses / truepoints

      else:
        fp = 0
        pp = 0

      allfailsofdataset = dataset['Label'].value_counts()[0]
        # print('all fails of dataset', allfailsofdataset)

      fr = countfails/allfailsofdataset
      pr = countpasses/(len(dataset.index) - allfailsofdataset)
      
      ssss = str(fp) + ', ' + str(fr) + ', ' + str(pp) + ', ' + str(pr)

      df.at[hhh, col+str('Prob')] = ssss

  return df


def FeatureEngineering(data):

  from itertools import combinations

  tins = ['TIN' + str(i) for i in range(8)]

  # Generate all 2-combinations of TINs
  features = ["TIN 0 Req-BW", "TIN 1 Req-BW", "TIN 2 Req-BW", "TIN 3 Req-BW", "TIN 4 Req-BW", "TIN 5 Req-BW", "TIN 6 Req-BW", "TIN 7 Req-BW"]


  for i in range(2, 9):
    tin_combinations = list(combinations(tins, i))

    for j in range(len(tin_combinations)):
      summation_combinations = ''
      for k in range(i):
        summation_combinations = tin_combinations[j][k] + '+' + summation_combinations

      summation_combinations = summation_combinations[:-1]
      features.append(summation_combinations)


  for hh in range(len(data.index)):

    for i in range(len(features)):

      f = features[i].split('+')

      if len(f) == 1:
        continue

      s = 0
      # print(f)

      for j in range(len(f)):

        s = data.loc[hh, 'TIN ' + str(f[j][-1]) + ' Req-BW'] + s

      data.loc[hh, features[i]] = s

  return data

def HandleFlakyTests(data, rep):

  i = 0
  k = 0

  newdata = pd.DataFrame(columns = ["TIN 0 Req-BW", "TIN 1 Req-BW", "TIN 2 Req-BW", "TIN 3 Req-BW", "TIN 4 Req-BW", "TIN 5 Req-BW", "TIN 6 Req-BW", "TIN 7 Req-BW", 'Label'])

  while i < len(data.index):

    countfails = 0
    countpass = 0

    newdata.loc[k, ["TIN 0 Req-BW", "TIN 1 Req-BW", "TIN 2 Req-BW", "TIN 3 Req-BW", "TIN 4 Req-BW", "TIN 5 Req-BW", "TIN 6 Req-BW", "TIN 7 Req-BW"]] = data.loc[i, ["TIN 0 Req-BW", "TIN 1 Req-BW", "TIN 2 Req-BW", "TIN 3 Req-BW", "TIN 4 Req-BW", "TIN 5 Req-BW", "TIN 6 Req-BW", "TIN 7 Req-BW"]]

    for j in range(rep):

      if data.loc[i + j, "Label"] == 1:

        countpass = countpass + 1

      elif data.loc[i + j, "Label"] == 0:

        countfails = countfails + 1

    if countpass > countfails:

      newdata.loc[k, 'Label'] = 1

    else:

      newdata.loc[k, 'Label'] = 0

    i = i + rep

    k = k + 1

  return newdata

def Preprocess(data):
  
  for i in range(len(data.index)):

    data.loc[i, 'ARG0'] = data.loc[i, 'TIN 0 Req-BW']
    data.loc[i, 'ARG1'] = data.loc[i, 'TIN 1 Req-BW']
    data.loc[i, 'ARG2'] = data.loc[i, 'TIN 2 Req-BW']
    data.loc[i, 'ARG3'] = data.loc[i, 'TIN 3 Req-BW']
    data.loc[i, 'ARG4'] = data.loc[i, 'TIN 4 Req-BW']
    data.loc[i, 'ARG5'] = data.loc[i, 'TIN 5 Req-BW']
    data.loc[i, 'ARG6'] = data.loc[i, 'TIN 6 Req-BW']
    data.loc[i, 'ARG7'] = data.loc[i, 'TIN 7 Req-BW']
    data.loc[i, 'ARG5+ARG6+ARG7'] = data.loc[i, 'TIN5+TIN6+TIN7']

  return data


for hh in range(0, 10):

  df = pd.read_excel('...\\path_to_file\\Ensemble Assertions.xlsx', sheet_name='dataset'+str(hh))

  ntsstestdata = pd.read_excel('...\\path_to_file\\Router'+str(hh)+'.xlsx')
  ntsstestdata['TIN5+TIN6+TIN7'] = ntsstestdata['TIN 5 Req-BW'] + ntsstestdata[ 'TIN 6 Req-BW'] + ntsstestdata['TIN 7 Req-BW']

  ntsstestdata = Preprocess(ntsstestdata)

  df[180:211] = CalculatePerformance(df[180:211].reset_index(), ntsstestdata).drop('index', axis = 1)

  df.to_excel('EnsembleRouterProbs'+str(hh)+'.xlsx')
