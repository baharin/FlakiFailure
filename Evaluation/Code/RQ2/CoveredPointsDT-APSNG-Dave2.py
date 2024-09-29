def ExtractRanges(rule, model):

  if model == 'APSNG':
    
    dictt = {'CLEV': [0,1], 'SUNO': [0,1], 'SUEV': [0,1], 'FOMO': [0,1], 'FONI': [0,1], 'SUNN': [0,1], 'RAIN': [0,1], 'ARG0':[0, 6], 'ARG1': [5, 100], 'ARG2': [30, 85]}

  elif model == 'dave2':

    dictt = {'CLEV': [0,1], 'SUNO': [0,1], 'SUEV': [0,1], 'FOMO': [0,1], 'FONI': [0,1], 'SUNN': [0,1], 'RAIN': [0,1] , 'ARG0':[0,6], 'ARG1': [5, 10], 'ARG2': [3, 20]}

  elif model == 'beamng-town-R1':

    dictt = {'CLEV': [0,1], 'SUNO': [0,1], 'SUEV': [0,1], 'FOMO': [0,1], 'FONI': [0,1], 'SUNN': [0,1], 'RAIN': [0,1] , 'ARG0': [0,6], 'ARG1': [5, 50], 'ARG2': [0, 10]}

  elif model == 'beamng-town-R2toR4':

    dictt = {'CLEV': [0,1], 'SUNO': [0,1], 'SUEV': [0,1], 'FOMO': [0,1], 'FONI': [0,1], 'SUNN': [0,1], 'RAIN': [0,1] , 'ARG0': [0,6], 'ARG1': [20, 50], 'ARG2': [0, 10]}

  for i in range(len(rule)):

    if rule[i][0] == 'greater_than_func':

      dictt[rule[i][1]][0] = float(rule[i][2]) + 1  #because the func is >

    elif rule[i][0] == 'less_than_func':

      dictt[rule[i][1]][1] = float(rule[i][2]) - 1 #because the func is <

    elif rule[i][0] == 'equal_to':

      # print(rule[i])
      dictt[rule[i][1]][0] = float(rule[i][2])
      dictt[rule[i][1]][1] = float(rule[i][2])

  return dictt



def CalculatePerformance(asserts, probs, dataset, model, res, alg):

  covered_values = [('No', -1, -1, -1)] * len(res.index)

  cols = ['RUN'+str(i) for i in range(1, 21)]

  for col in cols:

    res['Covered'+alg+col] = covered_values

  for ii in range(len(asserts)):

    for jj in range(len(asserts[ii][0])): #iterate over fail rules

      rule = asserts[ii][0][jj]

      print('this is rule', rule)
      ranges = ExtractRanges(rule, model)


      countfails = 0

      truepoints = 0

      for h in range(len(dataset.index)):

        if model == 'beamng' or model == 'dave2':

          allfailsofdataset = dataset['TestOutcome'].value_counts()['FAIL']

          if 'dt' in alg or 'DT' in alg:

            if ranges['CLEV'][0] <= float(dataset.loc[h, 'CLEV']) <= ranges['CLEV'][1] and ranges['SUNO'][0] <= float(dataset.loc[h, 'SUNO']) <= ranges['SUNO'][1] and ranges['SUEV'][0] <= float(dataset.loc[h, 'SUEV']) <= ranges['SUEV'][1] and ranges['FOMO'][0] <= float(dataset.loc[h, 'FOMO']) <= ranges['FOMO'][1] and ranges['FONI'][0] <= float(dataset.loc[h, 'FONI']) <= ranges['FONI'][1] and ranges['SUNN'][0] <= float(dataset.loc[h, 'SUNN']) <= ranges['SUNN'][1] and ranges['RAIN'][0] <= float(dataset.loc[h, 'RAIN']) <= ranges['RAIN'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'Maxspeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'MAX_ANGLE']) <= ranges['ARG2'][1]:

              # truepoints = truepoints + 1

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][0][jj][0]:

                  # print('yes', h)

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][0][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][0][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])

              # if dataset.loc[h, 'TestOutcome'] == 'FAIL':

                # countfails = countfails + 1


          else:

            if ranges['ARG0'][0] <=  float(dataset.loc[h, 'Weather'])  <= ranges['ARG0'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'Maxspeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'MAX_ANGLE']) <= ranges['ARG2'][1]:

              # truepoints = truepoints + 1

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][0][jj][0]:

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][0][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][0][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])


              else:

                # print(res.loc[h, 'Covered'+alg])
                # print(type(res.loc[h, 'Covered'+alg]))
                # print(rule)
                # print(type(rule))
                # print(precision)
                # print(type(precision))
                # # print(recall)
                # # print(type(recall))

                res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ''

                # print(res.loc[h, 'Covered'+alg])

                # print(type(res.loc[h, 'Covered'+alg]))

                # res.loc[h, 'Covered'+alg] = ('Yes', str(rule), precision, recall)

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', str(rule), probs[ii][0][jj][0], probs[ii][0][jj][1])

                # print(res.loc[h, 'Covered'+alg])


        elif model == 'beamng-town-R1' or model == 'beamng-town-R2toR4':

          try:
            allfailsofdataset = dataset['Label'].value_counts()[0]
          except:
            return -1, -1, -1, -1, res

          if 'dt' in alg or 'DT' in alg:

            if ranges['CLEV'][0] <= float(dataset.loc[h, 'CLEV']) <= ranges['CLEV'][1] and ranges['SUNO'][0] <= float(dataset.loc[h, 'SUNO']) <= ranges['SUNO'][1] and ranges['SUEV'][0] <= float(dataset.loc[h, 'SUEV']) <= ranges['SUEV'][1] and ranges['FOMO'][0] <= float(dataset.loc[h, 'FOMO']) <= ranges['FOMO'][1] and ranges['FONI'][0] <= float(dataset.loc[h, 'FONI']) <= ranges['FONI'][1] and ranges['SUNN'][0] <= float(dataset.loc[h, 'SUNN']) <= ranges['SUNN'][1] and ranges['RAIN'][0] <= float(dataset.loc[h, 'RAIN']) <= ranges['RAIN'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'MaxSpeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'Traffic Amount']) <= ranges['ARG2'][1]:

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][0][jj][0]:

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][0][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][0][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])


          else:

            if ranges['ARG0'][0] <=  float(dataset.loc[h, 'Weather'])  <= ranges['ARG0'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'MaxSpeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'Traffic Amount']) <= ranges['ARG2'][1]:

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][0][jj][0]:

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][0][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][0][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])


    for jj in range(len(asserts[ii][1])): #iterate over pass rules

      rule = asserts[ii][1][jj]

      print('this is rule', rule)
      ranges = ExtractRanges(rule, model)


      countfails = 0

      truepoints = 0

      for h in range(len(dataset.index)):

        if model == 'APSNG' or model == 'dave2':

          allfailsofdataset = dataset['TestOutcome'].value_counts()['FAIL']

          if 'dt' in alg or 'DT' in alg:

            if ranges['CLEV'][0] <= float(dataset.loc[h, 'CLEV']) <= ranges['CLEV'][1] and ranges['SUNO'][0] <= float(dataset.loc[h, 'SUNO']) <= ranges['SUNO'][1] and ranges['SUEV'][0] <= float(dataset.loc[h, 'SUEV']) <= ranges['SUEV'][1] and ranges['FOMO'][0] <= float(dataset.loc[h, 'FOMO']) <= ranges['FOMO'][1] and ranges['FONI'][0] <= float(dataset.loc[h, 'FONI']) <= ranges['FONI'][1] and ranges['SUNN'][0] <= float(dataset.loc[h, 'SUNN']) <= ranges['SUNN'][1] and ranges['RAIN'][0] <= float(dataset.loc[h, 'RAIN']) <= ranges['RAIN'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'Maxspeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'MAX_ANGLE']) <= ranges['ARG2'][1]:

              # truepoints = truepoints + 1

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][1][jj][0]:

                  # print('yes', h)

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][1][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][1][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])

              # if dataset.loc[h, 'TestOutcome'] == 'FAIL':

                # countfails = countfails + 1


          else:

            if ranges['ARG0'][0] <=  float(dataset.loc[h, 'Weather'])  <= ranges['ARG0'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'Maxspeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'MAX_ANGLE']) <= ranges['ARG2'][1]:

              # truepoints = truepoints + 1

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][1][jj][0]:

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][1][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][1][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])


              else:

                # print(res.loc[h, 'Covered'+alg])
                # print(type(res.loc[h, 'Covered'+alg]))
                # print(rule)
                # print(type(rule))
                # print(precision)
                # print(type(precision))
                # # print(recall)
                # # print(type(recall))

                res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ''

                # print(res.loc[h, 'Covered'+alg])

                # print(type(res.loc[h, 'Covered'+alg]))

                # res.loc[h, 'Covered'+alg] = ('Yes', str(rule), precision, recall)

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', str(rule), probs[ii][1][jj][0], probs[ii][1][jj][1])

                # print(res.loc[h, 'Covered'+alg])


        elif model == 'beamng-town-R1' or model == 'beamng-town-R2toR4':

          try:
            allfailsofdataset = dataset['Label'].value_counts()[0]
          except:
            return -1, -1, -1, -1, res

          if 'dt' in alg or 'DT' in alg:

            if ranges['CLEV'][0] <= float(dataset.loc[h, 'CLEV']) <= ranges['CLEV'][1] and ranges['SUNO'][0] <= float(dataset.loc[h, 'SUNO']) <= ranges['SUNO'][1] and ranges['SUEV'][0] <= float(dataset.loc[h, 'SUEV']) <= ranges['SUEV'][1] and ranges['FOMO'][0] <= float(dataset.loc[h, 'FOMO']) <= ranges['FOMO'][1] and ranges['FONI'][0] <= float(dataset.loc[h, 'FONI']) <= ranges['FONI'][1] and ranges['SUNN'][0] <= float(dataset.loc[h, 'SUNN']) <= ranges['SUNN'][1] and ranges['RAIN'][0] <= float(dataset.loc[h, 'RAIN']) <= ranges['RAIN'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'MaxSpeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'Traffic Amount']) <= ranges['ARG2'][1]:

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][1][jj][0]:

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][1][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][1][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])


          else:

            if ranges['ARG0'][0] <=  float(dataset.loc[h, 'Weather'])  <= ranges['ARG0'][1] and ranges['ARG1'][0] <=  float(dataset.loc[h, 'MaxSpeed'])  <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'Traffic Amount']) <= ranges['ARG2'][1]:

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][1][jj][0]:

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][1][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][1][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])


      # print(truepoints)
      # if truepoints != 0 :
      #   fp = countfails / truepoints

      # else:
      #   fp = 0


      # print('all fails of dataset', allfailsofdataset)

      # fr = countfails/allfailsofdataset

  return res

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


def RemoveFlakyTests(data, rep, features, label):

  i = 0
  while i < len(data.index):

    flag = False

    data.reset_index(drop=True, inplace=True)

    for j in range(rep):

      # if data.loc[i + j, ["Weather", "Maxspeed", "MAX_ANGLE"]].to_list() == data.loc[i, ["Weather", "Maxspeed", "MAX_ANGLE"]].to_list() and data.loc[i, 'TestOutcome'] != data.loc[i+j, 'TestOutcome']:
        if data.loc[i + j, features].to_list() == data.loc[i, features].to_list() and data.loc[i, label] != data.loc[i+j, label]:

          flag = True
          break

    if flag == True: #the test is flaky

      # print('yes')

      data = data.drop([i + j for j in range(rep)])

      i = 0

    else:
      i = i + rep

  return data

def FindGroups(df):

  groups = []

  group = []
  count = 0
  i = 0
  while i <len(df.index):
    group = []
    while i < len(df.index) and (not pd.isna(df.loc[i, 'Without Repetition'])):

      group.append(df.loc[i, 'Without Repetition'])
      count = count + 1
      i = i + 1

    if len(group) != 0 :
      groups.append(group)
      # print(groups)

    i = i + 1

  return groups


def FindPrecision(df):

  groups = []

  group = []
  count = 0
  i = 0
  while i <len(df.index):
    group = []
    while i < len(df.index) and (not pd.isna(df.loc[i, 'Precision1'])):

      group.append(df.loc[i, 'Precision1'])
      count = count + 1
      i = i + 1

    if len(group) != 0 :
      groups.append(group)
      # print(groups)

    i = i + 1

  return groups


def FindRecall(df):

  groups = []

  group = []
  count = 0
  i = 0
  while i <len(df.index):
    group = []
    while i < len(df.index) and (not pd.isna(df.loc[i, 'Recall1'])):

      group.append(df.loc[i, 'Recall1'])
      count = count + 1
      i = i + 1

    if len(group) != 0 :
      groups.append(group)
      # print(groups)

    i = i + 1

  return groups


def FindAcc(group, testset, model, res, alg, assertionsprecisions, asssertionsrecalls):

  # for i in range(len(testset.index)):

  #   testset.loc[i, 'Covered'+alg] = ('No', -1, -1, -1)

  covered_values = [('No', -1, -1, -1)] * len(testset.index)

  testset['Covered'+alg] = covered_values


  # group = group[0]

  # assertionsprecisions = assertionsprecisions[0]

  # asssertionsrecalls = asssertionsrecalls[0]

  print(group)

  for i in range(len(group)):

    print('here1 ', group[i])

    if 'DR' in alg:

      r = str(PreprocessRule(group[i]))

    else:

      r = group[i]

    rule = ast.literal_eval(r)

    print('here' , rule)

    rule = SimplifyRule(rule)

    res = CalculatePerformance(rule, testset, model, res, alg, assertionsprecisions[i], asssertionsrecalls[i])

    # accuracydf.loc[accuracydf.shape[0]] = ['all', model, len(testset.index)  ,  'Without' , rule, truepoints, countfails, acc, fr]

  return res

def ExtractBounds(rule):
  #print(type(rule))
  #print("rule", rule)
  rule = rule[1:-1].split('^')
  print("rule", rule)

  dictt = {}

  for i in range(len(rule)):
    #print(rule[i])
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
      #print(a, "****", k+1, rule[i][k+1:len(rule[i])])
      dictt[rule[i][:rule[i].find('=')]] = [float(a), float(rule[i][k+1:len(rule[i])]), "between"]

    elif rule[i].find('=') != -1:

      #print(rule[i][rule[i].find('=')+1 : len(rule[i])])
      #print(len(rule[i][rule[i].find('=')+1 : len(rule[i])]))
      dictt[rule[i][:rule[i].find('=')]] = [float(rule[i][rule[i].find('=')+1 : len(rule[i])]), "", "equal"]

  #print("dictt is", dictt)

  return dictt

def PreprocessRule(rulee):

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

  return listt

def HandleFlakyTests(data, rep, features, label, model):

  i = 0
  k = 0

  featurescopy = features
  featurescopy.append(label)

  newdata = pd.DataFrame(columns = featurescopy)

  while i < len(data.index):

    countfails = 0
    countpass = 0

    newdata.loc[k, features] = data.loc[i, features]

    for j in range(rep):

      if data.loc[i + j, label] == 1 or data.loc[i + j , label]  == 'PASS':

        countpass = countpass + 1

      elif data.loc[i + j, label] == 0 or data.loc[i + j, label] == 'FAIL':

        countfails = countfails + 1

    if countpass > countfails:

      if 'town' in model:

        newdata.loc[k, label] = 1
      else:

        newdata.loc[k, label] = 'PASS'

    else:
      if 'town' in model:

        newdata.loc[k, label] = 0

      else:

        newdata.loc[k, label] = 'FAIL'

    i = i + rep

    k = k + 1

  return newdata




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

        # newdata.loc[j, 'Weather'] = float(data.loc[j, 'Weather'])

        if 'town' not in model:

            newdata.loc[k, 'Maxspeed'] = data.loc[j, 'Maxspeed'] * 1.0

            newdata.loc[k, 'MAX_ANGLE'] = data.loc[j, 'MAX_ANGLE'] * 1.0

            newdata.loc[k, 'TestOutcome'] = data.loc[j, 'TestOutcome']


        else:
            newdata.loc[k, 'MaxSpeed'] = data.loc[j, 'MaxSpeed'] * 1.0

            newdata.loc[k, 'Traffic Amount'] = data.loc[j, 'Traffic Amount'] * 1.0

            newdata.loc[k, 'Label'] = data.loc[j, 'Label'] #change to Label(Ultra) for ultra

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
        j = j + rep

    return newdata

def SimplifyRule(rule):

  i = 0

  while i < len(rule) - 1:

    j = i + 1
    while j < len(rule):

      if rule[i][1] == rule[j][1] and rule[i][0] == rule[j][0]: #if variables and operator are the same

          if rule[i][0] == 'greater_than_func':

            if float(rule[i][2]) >= float(rule[j][2]): #rule j should be removed

              rule.remove(rule[j])
              i = -1
              break
            else:

              rule.remove(rule[i])
              i = -1
              break

          elif rule[i][0] == 'less_than_func':

            if float(rule[i][2]) <= float(rule[j][2]): #rule j should be removed

              rule.remove(rule[j])
              i = -1
              break
            else:

              rule.remove(rule[i])
              i = -1
              break

      j = j + 1

    i = i + 1

  return rule


def GetFailAndPassAssertions(assertions, theta):

  cols = ['RUN'+str(i) for i in range(1, 21)]

  asserts = []

  probs = []

  for col in cols:

    Failassertions = []
    Passassertions = []

    Failassertionsprobs = []
    Passassertionsprobs = []

    i = 0
    while i < len(assertions.index) and assertions.loc[i, col] != '[]' and type(assertions.loc[i, col]) != float:

      if ast.literal_eval(assertions.loc[i, col+'Prob'])[0] >= theta:
        Failassertions.append(ast.literal_eval(assertions.loc[i, col]))
        Failassertionsprobs.append((ast.literal_eval(assertions.loc[i, col+'Prob'])[0], ast.literal_eval(assertions.loc[i, col+'Prob'])[1]))
      i = i + 1

    i = i + 1
    # print(assertions.loc[i, col], type(assertions.loc[i, col] != '[]'))
    while i < len(assertions.index) and assertions.loc[i, col] != '[]' and type(assertions.loc[i, col]) != float:
      # print(i, col)
      if ast.literal_eval(assertions.loc[i, col+'Prob'])[0] >= theta:
        Passassertions.append(ast.literal_eval(assertions.loc[i, col]))
        Passassertionsprobs.append((ast.literal_eval(assertions.loc[i, col+'Prob'])[0],ast.literal_eval(assertions.loc[i, col+'Prob'])[1] ))
      i = i + 1

    asserts.append([Failassertions, Passassertions])
    probs.append([Failassertionsprobs, Passassertionsprobs])

  return asserts, probs


import pandas as pd
import ast

model = 'Dave2' #change to APSNG for APSNG

thetas = [0 , 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

for hh in range(1, 10):

  for theta in thetas:
    assertions = pd.read_excel('...\\path_to_file\\DT and DR Assertions.xlsx', sheet_name = 'dataset'+str(hh))

    testset = pd.read_excel('...\\path_to_file\\Dave2_testset.xlsx')

    cols = ['Weather', 'Maxspeed' , 'MAX_ANGLE']
    collabel = 'TestOutcome'

    testset = HandleFlakyTests(testset, 10, cols, collabel, model)
    testset = Preprocess(testset)
    res = testset

    asserts, probs = GetFailAndPassAssertions(assertions[180:199].reset_index(), theta) #change 

    res = CalculatePerformance(asserts, probs, testset, model, res, 'dr')

    import os 

    file_exists = os.path.isfile('dr-coveredpoints-dave2-theta'+str(theta)+'-testset.xlsx')

    with pd.ExcelWriter('dt-coveredpoints-dave2-theta'+str(theta)+'-testset.xlsx', engine = 'openpyxl', mode = 'a' if file_exists else 'w') as writer:
      res.to_excel(writer, sheet_name = 'dataset'+str(hh), index = False)
