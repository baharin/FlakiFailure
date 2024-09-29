import math
import ast

def Preprocess(dataa):

  weathers = ['CLEV', 'SUNO', 'SUEV', 'FOMO', 'FONI', 'SUNN', 'RAIN']

  for i in range(len(dataa.index)):

    for j in range(len(weathers)):

      dataa.loc[i, weathers[j]] = 0

    if dataa.loc[i, 'Weather'] == 0:
      dataa.loc[i, weathers[0]] = 1

    elif dataa.loc[i, 'Weather'] == 1:
      dataa.loc[i, weathers[1]] = 1

    elif dataa.loc[i, 'Weather'] == 2:
      dataa.loc[i, weathers[2]] = 1

    elif dataa.loc[i, 'Weather'] == 3:
      dataa.loc[i, weathers[3]] = 1

    elif dataa.loc[i, 'Weather'] == 4:
      dataa.loc[i, weathers[4]] = 1

    elif dataa.loc[i, 'Weather'] == 5:
      dataa.loc[i, weathers[5]] = 1

    elif dataa.loc[i, 'Weather'] == 6:
      dataa.loc[i, weathers[6]] = 1

  return dataa

def ExtractRanges(rule, model):

  if model == 'AP-SNG':

    dictt = {'CLEV': [0,1], 'SUNO': [0,1], 'SUEV': [0,1], 'FOMO': [0,1], 'FONI': [0,1], 'SUNN': [0,1], 'RAIN': [0,1], 'ARG0':[0, 6], 'ARG1': [5, 100], 'ARG2': [30, 85]}

  elif model == 'dave2':

    dictt = {'CLEV': [0,1], 'SUNO': [0,1], 'SUEV': [0,1], 'FOMO': [0,1], 'FONI': [0,1], 'SUNN': [0,1], 'RAIN': [0,1] , 'ARG0':[0,6], 'ARG1': [5, 10], 'ARG2': [3, 20]}

  elif model == 'beamng-town-R1':

    dictt = {'CLEV': [0,1], 'SUNO': [0,1], 'SUEV': [0,1], 'FOMO': [0,1], 'FONI': [0,1], 'SUNN': [0,1], 'RAIN': [0,1] , 'ARG0': [0,6], 'ARG1': [5, 50], 'ARG2': [0, 10]}

  elif model == 'beamng-town-R2toR4':

    dictt = {'CLEV': [0,1], 'SUNO': [0,1], 'SUEV': [0,1], 'FOMO': [0,1], 'FONI': [0,1], 'SUNN': [0,1], 'RAIN': [0,1] , 'ARG0': [0,6], 'ARG1': [20, 50], 'ARG2': [0, 10]}

  for i in range(len(rule)):

    if rule[i][0] == 'greater_than_func':

      dictt[rule[i][1]][0] = float(rule[i][2]) + 0.1  #because the func is >

    elif rule[i][0] == 'less_than_func':

      dictt[rule[i][1]][1] = float(rule[i][2]) - 0.1 #because the func is <

    elif rule[i][0] == 'equal_to':

      # print(rule[i])
      dictt[rule[i][1]][0] = float(rule[i][2])
      dictt[rule[i][1]][1] = float(rule[i][2])

  return dictt

def CalculatePerformance(df, dataset, model, label):

  cols = ['Run'+str(i) for i in range(1, 21)]

  for hhh in range(len(df.index)):

    for col in cols:

      try:
        rule = ast.literal_eval(df.loc[hhh, col])
      except:
        continue
      
      if len(rule) == 0 or rule[0] == '':
        continue

      ranges = ExtractRanges(rule, model)

      countfails = 0

      countpasses = 0

      truepoints = 0

      for h in range(len(dataset.index)):

        if model == 'AP-SNG' or model == 'Dave2':

          allfailsofdataset = dataset[label].value_counts()['FAIL']
          allpassesofdataset = dataset[label].value_counts()['PASS']

          if ranges['CLEV'][0] <= float(dataset.loc[h, 'CLEV']) <= ranges['CLEV'][1] and ranges['SUNO'][0] <= float(dataset.loc[h, 'SUNO']) <= ranges['SUNO'][1] and ranges['SUEV'][0] <= float(dataset.loc[h, 'SUEV']) <= ranges['SUEV'][1] and ranges['FOMO'][0] <= float(dataset.loc[h, 'FOMO']) <= ranges['FOMO'][1] and ranges['FONI'][0] <= float(dataset.loc[h, 'FONI']) <= ranges['FONI'][1] and ranges['SUNN'][0] <= float(dataset.loc[h, 'SUNN']) <= ranges['SUNN'][1] and ranges['RAIN'][0] <= float(dataset.loc[h, 'RAIN']) <= ranges['RAIN'][1] and ranges['ARG0'][0] <=  float(dataset.loc[h, 'Weather'])  <= ranges['ARG0'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'Maxspeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'MAX_ANGLE']) <= ranges['ARG2'][1]:

            truepoints = truepoints + 1

            if dataset.loc[h, label] == 'FAIL':

              countfails = countfails + 1

            elif dataset.loc[h, label] == 'PASS':

              countpasses = countpasses + 1

        elif 'town' in model:

          allfailsofdataset = dataset[label].value_counts()[0]
          allpassesofdataset = dataset[label].value_counts()[1]

          if ranges['CLEV'][0] <= float(dataset.loc[h, 'CLEV']) <= ranges['CLEV'][1] and ranges['SUNO'][0] <= float(dataset.loc[h, 'SUNO']) <= ranges['SUNO'][1] and ranges['SUEV'][0] <= float(dataset.loc[h, 'SUEV']) <= ranges['SUEV'][1] and ranges['FOMO'][0] <= float(dataset.loc[h, 'FOMO']) <= ranges['FOMO'][1] and ranges['FONI'][0] <= float(dataset.loc[h, 'FONI']) <= ranges['FONI'][1] and ranges['SUNN'][0] <= float(dataset.loc[h, 'SUNN']) <= ranges['SUNN'][1] and ranges['RAIN'][0] <= float(dataset.loc[h, 'RAIN']) <= ranges['RAIN'][1] and ranges['ARG0'][0] <= float(dataset.loc[h, 'Weather']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'MaxSpeed'])  <= ranges['ARG1'][1] and  ranges['ARG2'][0] <= float(dataset.loc[h, 'Traffic Amount']) <= ranges['ARG2'][1] :

            truepoints = truepoints + 1

            if dataset.loc[h, label] == 0:

              countfails = countfails + 1

            if dataset.loc[h, label] == 1:

              countpasses = countpasses + 1

      if truepoints != 0 :
        fp = countfails / truepoints
        pp = countpasses / truepoints

      else:
        fp = 0
        pp = 0

      fr = countfails/allfailsofdataset
      pr = countpasses/allpassesofdataset

      ssss = str(fp) + ', ' + str(fr) + ', ' + str(pp) + ', ' + str(pr)
      
      df.loc[hhh, col+str('Prob')] = ssss

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

        if var == 'Weather':
            var1 = 'ARG0'
        elif var == 'Maxspeed':
            var1 = 'ARG1'
        elif var == 'MAX_ANGLE':
            var1 = 'ARG2'
        elif var == 'MaxSpeed':
          var1 = 'ARG1'
        elif var == 'TrafficAmount':
          var1 = 'ARG2'

        elif var == 'TIN0Req-BW':
          var1 = 'ARG0'
        elif var == 'TIN1Req-BW':
          var1 = 'ARG1'
        elif var == 'TIN2Req-BW':
          var1 = 'ARG2'
        elif var == 'TIN3Req-BW':
          var1 = 'ARG3'
        elif var == 'TIN4Req-BW':
          var1 = 'ARG4'
        elif var == 'TIN5Req-BW':
          var1 = 'ARG5'
        elif var == 'TIN6Req-BW':
          var1 = 'ARG6'
        elif var == 'TIN7Req-BW':
          var1 = 'ARG7'

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
        else:
          t = ('equal_to', var1, vars[var][0])
          listt.append(t)

      df.at[hhh, col] = str(listt)

  return df

def PreprocessWithoutRepetition(data, rep, model):

    if 'town' in model:

        newdata = pd.DataFrame(
            columns=['Label', 'Weather', 'MaxSpeed', 'Traffic Amount'])
    else:

        newdata = pd.DataFrame(columns=['TestOutcome', 'Weather', 'Maxspeed', 'MAX_ANGLE'])

    j = 0
    k = 0
    counterr = 0

    while j < len(data.index):

        if 'town' not in model:

            newdata.loc[k, 'Maxspeed'] = data.loc[j, 'Maxspeed'] * 1.0

            newdata.loc[k, 'MAX_ANGLE'] = data.loc[j, 'MAX_ANGLE'] * 1.0

            newdata.loc[k, 'TestOutcome'] = data.loc[j, 'TestOutcome']


        else:
            newdata.loc[k, 'MaxSpeed'] = data.loc[j, 'MaxSpeed'] * 1.0

            newdata.loc[k, 'Traffic Amount'] = data.loc[j, 'Traffic Amount'] * 1.0

            if 'R2toR4' in model:
              newdata.loc[k, 'Label(Ultra)'] = data.loc[j, 'Label(Ultra)'] #change to Label(Ultra) for ultra
              newdata.loc[k, 'Label(Distance)'] = data.loc[j, 'Label(Distance)']
              newdata.loc[k, 'Label(Damage)'] = data.loc[j, 'Label(Damage)']

            elif 'R1' in model:
              newdata.loc[k, 'Label'] = data.loc[j, 'Label']


        if type(data.loc[j, 'Weather']) == str:

            if data.loc[j, 'Weather'] == 'cloudy_evening':

                newdata.loc[k, 'Weather'] = (0.0, '')

            elif data.loc[j, 'Weather'] == 'sunny_noon':

                newdata.loc[k, 'Weather'] = (1.0, '')

            elif data.loc[j, 'Weather'] == 'sunny_evening':

                newdata.loc[k, 'Weather'] = (2.0, '')

            elif data.loc[j, 'Weather'] == 'foggy_morning':

                newdata.loc[k, 'Weather'] = (3.0, '')

            elif data.loc[j, 'Weather'] == 'foggy_night':

                newdata.loc[k, 'Weather'] = (4.0, '')

            elif data.loc[j, 'Weather'] == 'sunny':

                newdata.loc[k, 'Weather'] = (5.0, '')

            elif data.loc[j, 'Weather'] == 'rainy':

                newdata.loc[k, 'Weather'] = (6.0, '')

        else:

            newdata.loc[k, 'Weather'] = data.loc[j, 'Weather'] * 1.0

        k = k + 1
        j = j + 1

    return newdata


import pandas as pd

for hh in range(0, 10):

  trainingsetbeamngcmp = PreprocessWithoutRepetition(pd.read_excel('...\\path_to_file\\AP-SNG'+str(hh)+'.xlsx'), 10, 'beamng')
  trainingsetdave2 = PreprocessWithoutRepetition(pd.read_excel('...\\path_to_file\\Dave2'+str(hh)+'.xlsx'), 10, 'dave2')
  trainingsetbeamngtownR2toR4 = PreprocessWithoutRepetition(pd.read_csv('...\\path_to_file\\AP-TWN - R2 to R4 - '+str(hh)+'.csv'), 10, 'beamng-town-R2toR4')
  trainingsetbeamngtownR1 = PreprocessWithoutRepetition(pd.read_excel('...\\path_to_file\\AP-TWN - R1 - '+str(hh)+'.xlsx'), 10, 'beamng-town-R1')
  
  trainingsetbeamngcmp = Preprocess(trainingsetbeamngcmp)
  trainingsetdave2 = Preprocess(trainingsetdave2)
  trainingsetbeamngtownR1 = Preprocess(trainingsetbeamngtownR1)
  trainingsetbeamngtownR2toR4 = Preprocess(trainingsetbeamngtownR2toR4)


  data = pd.read_excel('Ensemble Assertions.xlsx', sheet_name='dataset'+str(hh))

  data[:29] = CalculatePerformance(data[:29].reset_index(), trainingsetbeamngcmp, 'beamng', 'TestOutcome').drop('index', axis = 1)
  data[30:59] = CalculatePerformance(data[30:59].reset_index(), trainingsetdave2, 'dave2', 'TestOutcome').drop('index', axis = 1)
  data[60:89] = CalculatePerformance(data[60:89].reset_index(), trainingsetbeamngtownR1, 'beamng-town-R1', 'Label').drop('index', axis = 1)
  data[90:119] = CalculatePerformance(data[90:119].reset_index(), trainingsetbeamngtownR2toR4, 'beamng-town-R2toR4', 'Label(Damage)').drop('index', axis = 1)
  data[120:149] = CalculatePerformance(data[120:149].reset_index(), trainingsetbeamngtownR2toR4, 'beamng-town-R2toR4', 'Label(Distance)').drop('index', axis = 1)
  data[150:179] = CalculatePerformance(data[150:179].reset_index(), trainingsetbeamngtownR2toR4, 'beamng-town-R2toR4', 'Label(Ultra)').drop('index', axis = 1)

  data.to_excel('EnsembleProbs'+str(hh)+'.xlsx')
  
