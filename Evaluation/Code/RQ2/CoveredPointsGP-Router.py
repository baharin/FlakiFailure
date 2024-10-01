simport re

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



def CalculatePerformance(asserts, probs, dataset, res, alg):

  cols = ['RUN'+str(i) for i in range(1, 21)]
  
  covered_values = [('No', -1, -1, -1)] * len(res.index)

  for col in cols:

    res['Covered'+alg+col] = covered_values

  for ii in range(len(asserts)):

    for jj in range(len(asserts[ii][0])): #iterate over fail rules

      rule = asserts[ii][0][jj]

      ranges = ExtractVarsandValues(rule)

    
      for h in range(len(dataset.index)):

        if len(ranges[1]) == 1: #the formula is either x > num or x < num. there is only one variable

          if ranges[0] == 'greater':

            if float(dataset.loc[h, 'TIN '+ ranges[1][0][-1] + ' Req-BW']) > float(ranges[2]):

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

              # if dataset.loc[h, 'Label'] == 0:

              #   countfails = countfails + 1

          else:

            if float(dataset.loc[h, 'TIN '+ ranges[1][0][-1] + ' Req-BW']) < float(ranges[2]):

              # truepoints = truepoints + 1

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][0][jj][0]:

                  # print('yes', h)

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][0][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][0][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', str(rule), probs[ii][0][jj][0], probs[ii][0][jj][1])

              # if dataset.loc[h, 'Label'] == 0:

              #   countfails = countfails + 1

        else:

          # dataset = FeatureEngineering(dataset, ranges)

          if ranges[0] == 'greater':

            sums = 0
            for kk in range(len(ranges[1])):

              sums = sums +  float(dataset.loc[h, 'TIN ' + ranges[1][kk][-1] + ' Req-BW'])

            if sums > float(ranges[2]):

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][0][jj][0]:

                  # print('yes', h)

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', rule, probs[ii][0][jj][0], probs[ii][0][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][0][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][0][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', str(rule), probs[ii][0][jj][0], probs[ii][0][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', str(rule), probs[ii][0][jj][0], probs[ii][0][jj][1])

              # truepoints = truepoints + 1

              # if dataset.loc[h, 'Label'] == 0:

              #   countfails = countfails + 1

          else:
            sums = 0
            for kk in range(len(ranges[1])):

              sums = sums +  float(dataset.loc[h, 'TIN ' + ranges[1][kk][-1] + ' Req-BW'])

            if sums < float(ranges[2]):

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][0][jj][0]:

                  # print('yes', h)

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', str(rule), probs[ii][0][jj][0], probs[ii][0][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][0][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][0][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', str(rule), probs[ii][0][jj][0], probs[ii][0][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('FAIL', str(rule), probs[ii][0][jj][0], probs[ii][0][jj][1])

     
     
     
     
    for jj in range(len(asserts[ii][1])): #iterate over pass rules

      rule = asserts[ii][1][jj]

      ranges = ExtractVarsandValues(rule)

    
      for h in range(len(dataset.index)):

        if len(ranges[1]) == 1: #the formula is either x > num or x < num. there is only one variable

          if ranges[0] == 'greater':

            if float(dataset.loc[h, 'TIN '+ ranges[1][0][-1] + ' Req-BW']) > float(ranges[2]):

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

              # if dataset.loc[h, 'Label'] == 0:

              #   countfails = countfails + 1

          else:

            if float(dataset.loc[h, 'TIN '+ ranges[1][0][-1] + ' Req-BW']) < float(ranges[2]):

              # truepoints = truepoints + 1

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][1][jj][0]:

                  # print('yes', h)

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][1][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][1][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', str(rule), probs[ii][1][jj][0], probs[ii][1][jj][1])

              # if dataset.loc[h, 'Label'] == 0:

              #   countfails = countfails + 1

        else:

          # dataset = FeatureEngineering(dataset, ranges)

          if ranges[0] == 'greater':

            sums = 0
            for kk in range(len(ranges[1])):

              sums = sums +  float(dataset.loc[h, 'TIN ' + ranges[1][kk][-1] + ' Req-BW'])

            if sums > float(ranges[2]):

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][1][jj][0]:

                  # print('yes', h)

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', rule, probs[ii][1][jj][0], probs[ii][1][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][1][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][1][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', str(rule), probs[ii][1][jj][0], probs[ii][1][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', str(rule), probs[ii][1][jj][0], probs[ii][1][jj][1])

              # truepoints = truepoints + 1

              # if dataset.loc[h, 'Label'] == 0:

              #   countfails = countfails + 1

          else:
            sums = 0
            for kk in range(len(ranges[1])):

              sums = sums +  float(dataset.loc[h, 'TIN ' + ranges[1][kk][-1] + ' Req-BW'])

            if sums < float(ranges[2]):

              if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][0] != 'No': # if this test input is already covered by another rule

                if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] < probs[ii][1][jj][0]:

                  # print('yes', h)

                  res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', str(rule), probs[ii][1][jj][0], probs[ii][1][jj][1])

                elif res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][2] == probs[ii][1][jj][0]:

                  if res.loc[h, 'Covered'+alg+'RUN'+str(ii + 1)][3] < probs[ii][1][jj][1]:

                    res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', str(rule), probs[ii][1][jj][0], probs[ii][1][jj][1])


              else:

                res.at[h, 'Covered'+alg+'RUN'+str(ii + 1)] = ('PASS', str(rule), probs[ii][1][jj][0], probs[ii][1][jj][1])       

  return res

def CalculatePerformanceDT(rule, dataset, column, res, alg, precision, recall):

  print('this is rule now, ', rule)

  ranges = ExtractRanges(rule)

  print(ranges)

  countfails = 0

  truepoints = 0

  for h in range(len(dataset.index)):

    # print(float(dataset.loc[h, 'Weather']))
    # print(dataset.loc[h, 'Weather'])

    if column == 'TIN5+TIN6+TIN7':

      if ranges['TIN5+TIN6+TIN7'][0] <= dataset.loc[h, 'TIN5+TIN6+TIN7'] <= ranges['TIN5+TIN6+TIN7'][1]:

        # truepoints = truepoints + 1

        if res.loc[h, 'Covered'+alg][0] != 'No': # if this test input is already covered by another rule

            if res.loc[h, 'Covered'+alg][2] < precision:

              # print('yes', h)

              res.at[h, 'Covered'+alg] = ('Yes', rule, precision, recall)

            elif res.loc[h, 'Covered'+alg][2] == precision:

              if res.loc[h, 'Covered'+alg][3] < recall:

                res.at[h, 'Covered'+alg] = ('Yes', rule, precision, recall)


        else:

            res.at[h, 'Covered'+alg] = ('Yes', rule, precision, recall)

        # if dataset.loc[h, 'Label'] == 0:

        #   countfails = countfails + 1

    else:
      # print('this is h ', h)

      if ranges['TIN 0 Req-BW'][0] <= dataset.loc[h, 'TIN 0 Req-BW'] <= ranges['TIN 0 Req-BW'][1] and ranges['TIN 1 Req-BW'][0] <= dataset.loc[h, 'TIN 1 Req-BW'] <= ranges['TIN 1 Req-BW'][1] and ranges['TIN 2 Req-BW'][0] <= dataset.loc[h, 'TIN 2 Req-BW'] <= ranges['TIN 2 Req-BW'][1] and ranges['TIN 3 Req-BW'][0] <= dataset.loc[h, 'TIN 3 Req-BW'] <= ranges['TIN 3 Req-BW'][1] and ranges['TIN 4 Req-BW'][0] <= dataset.loc[h, 'TIN 4 Req-BW'] <= ranges['TIN 4 Req-BW'][1] and ranges['TIN 5 Req-BW'][0] <= dataset.loc[h, 'TIN 5 Req-BW'] <= ranges['TIN 5 Req-BW'][1] and ranges['TIN 6 Req-BW'][0] <= dataset.loc[h, 'TIN 6 Req-BW'] <= ranges['TIN 6 Req-BW'][1] and ranges['TIN 7 Req-BW'][0] <= dataset.loc[h, 'TIN 7 Req-BW'] <= ranges['TIN 7 Req-BW'][1]:

        # print('yes')
        # truepoints = truepoints + 1

        if res.loc[h, 'Covered'+alg][0] != 'No': # if this test input is already covered by another rule

          if res.loc[h, 'Covered'+alg][2] < precision:

              # print('yes', h)

              res.at[h, 'Covered'+alg] = ('Yes', rule, precision, recall)

          elif res.loc[h, 'Covered'+alg][2] == precision:

              if res.loc[h, 'Covered'+alg][3] < recall:

                res.at[h, 'Covered'+alg] = ('Yes', rule, precision, recall)


        else:

            res.at[h, 'Covered'+alg] = ('Yes', rule, precision, recall)

        # if dataset.loc[h, 'Label'] == 0:

        #   # print('fail')
        #   countfails = countfails + 1


  # print(countfails, truepoints)
  # if truepoints != 0 :
  #   fp = countfails / truepoints

  # else:
  #   fp = 0

  # allfailsofdataset = dataset['Label'].value_counts()[0]
  # # print('all fails of dataset', allfailsofdataset)

  # fr = countfails/allfailsofdataset

  return res


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

def FindAcc(group, testset, model, res, alg, assertionsprecisions, assertionsrecalls):

  covered_values = [('No', -1, -1, -1)] * len(testset.index)

  testset['Covered'+alg] = covered_values

  print(group)

  # group = group[0]

  # assertionsprecisions = assertionsprecisions[0]

  # assertionsrecalls = assertionsrecalls[0]

  print(group)

  for i in range(len(group)):

    print('here1 ', group[i])

    if 'DR' in alg:

      r = str(PreprocessRule(group[i]))
      rule = ast.literal_eval(r)

    else:

      if 'gp' in alg or 'rs' in alg:

        rule = group[i]

      else:
        r = group[i]
        rule = ast.literal_eval(r)

    # print('this is ruleeee', r)
    # rule = ast.literal_eval(r)

    # print('here' , rule)

    # rule = SimplifyRule(rule)

    if 'GP' in alg or 'gp' in alg or 'rs' in alg or 'RS' in alg:

      res = CalculatePerformanceGP(rule, testset, model, res, alg, assertionsprecisions[i], assertionsrecalls[i])

    elif 'DT' in alg:

      if '5any' in alg:

        col = 'TIN5+TIN6+TIN7'

    else:

      if 'sum' in alg:

        col = 'TIN5+TIN6+TIN7'

      else:

        col = ["TIN 0 Req-BW", "TIN 1 Req-BW", "TIN 2 Req-BW", "TIN 3 Req-BW", "TIN 4 Req-BW", "TIN 5 Req-BW", "TIN 6 Req-BW", "TIN 7 Req-BW"]

      res = CalculatePerformanceDT(rule, testset, col, res, alg, assertionsprecisions[i], assertionsrecalls[i])

    # accuracydf.loc[accuracydf.shape[0]] = ['all', model, len(testset.index)  ,  'Without' , rule, truepoints, countfails, acc, fr]

  return res

def ExtractRanges(rule):

  dictt = {'TIN5+TIN6+TIN7': [0, 541], 'TIN 0 Req-BW': [0, 400], 'TIN 1 Req-BW': [0, 350], 'TIN 2 Req-BW': [0, 306],'TIN 3 Req-BW': [0, 267],'TIN 4 Req-BW': [0, 234],'TIN 5 Req-BW': [0, 205],'TIN 6 Req-BW': [0, 179],'TIN 7 Req-BW': [0, 157]}


  # print('this is rule ', rule)

  for i in range(len(rule)):

    # print(rule[i][0])

    if rule[i][0] == 'greater_than_func':

      # print('ok')
      dictt[rule[i][1]][0] = float(rule[i][2]) + 1  #because the func is >

    elif rule[i][0] == 'less_than_func':

      dictt[rule[i][1]][1] = float(rule[i][2]) - 1 #because the func is <

  return dictt

def PreprocessRule(rulee):

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

  return listt

def FeatureEngineering(data, ranges):

  for i in range(len(data.index)):

    # data.loc[i, 'TIN5+TIN6+TIN7'] = float(data.loc[i, 'TIN 5 Req-BW']) + float(data.loc[i, 'TIN 6 Req-BW']) + float(data.loc[i, 'TIN 7 Req-BW'])

    s = ''
    summ = 0

    for j in range(len(ranges[1])):

      s = s + 'TIN' + ranges[1][j][-1] + '+'
      summ = summ + float(data.loc[i, 'TIN ' + ranges[1][j][-1] + ' Req-BW'])

    s = s[:-1]

    data.loc[i, s] = summ

  return data


def ReduceListBasedonTheta(listofassertions, theta, precisions, recalls):

  i = 0

  while i < len(listofassertions):

    if precisions[i] < theta:

      del listofassertions[i]
      del precisions[i]
      del recalls[i]

      i = 0

    else:

      i = i + 1

  return listofassertions, precisions, recalls

def GetFailAndPassAssertions(failassertions, passassertions, theta):

  cols = ['Run'+str(i) for i in range(1, 21)]

  asserts = []

  probs = []

  for col in cols:

    Failassertions = []
    Passassertions = []

    Failassertionsprobs = []
    Passassertionsprobs = []

    i = 0
    while i < len(failassertions.index) and failassertions.loc[i, col] != '[]' and type(failassertions.loc[i, col]) != float:

      if ast.literal_eval(failassertions.loc[i, col+'Prob'])[0] >= theta:
        Failassertions.append(failassertions.loc[i, col])
        Failassertionsprobs.append((ast.literal_eval(failassertions.loc[i, col+'Prob'])[0], ast.literal_eval(failassertions.loc[i, col+'Prob'])[1]))
      i = i + 1

    i = 0
    while i < len(passassertions.index) and passassertions.loc[i, col] != '[]' and type(passassertions.loc[i, col]) != float:
      if ast.literal_eval(passassertions.loc[i, col+'Prob'])[0] >= theta:
        Passassertions.append(passassertions.loc[i, col])
        Passassertionsprobs.append((ast.literal_eval(passassertions.loc[i, col+'Prob'])[0],ast.literal_eval(passassertions.loc[i, col+'Prob'])[1] ))
      i = i + 1

    asserts.append([Failassertions, Passassertions])
    probs.append([Failassertionsprobs, Passassertionsprobs])

  return asserts, probs

def ConsistencyCheck(asserts, probs):

  for ii in range(len(asserts)):

    fail_assertions = asserts[ii][0]
    pass_assertions = asserts[ii][1]

    new_fail_assertions, new_pass_assertions = ConsistencyCheckingRouter.process_assertions(fail_assertions, pass_assertions)

    asserts[ii][0] = new_fail_assertions
    asserts[ii][1] = new_pass_assertions

    map_probs_fail = {fail_assertions[i]: probs[ii][0][i] for i in range(len(fail_assertions))}
    map_probs_pass = {pass_assertions[i]: probs[ii][1][i] for i in range(len(pass_assertions))}

    new_probs_fail = [map_probs_fail[value] for value in new_fail_assertions]
    new_probs_pass = [map_probs_pass[value] for value in new_pass_assertions]

    probs[ii][0] = new_probs_fail
    probs[ii][1] = new_probs_pass
    
  return asserts, probs

import pandas as pd
import ast
import ConsistencyCheckingRouter

thetas = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]


ts = ['Tarantula', 'Ochiai', 'Naish']



for theta in thetas:

  for ind, t in enumerate(ts):

    for hh in range(0, 10):

      failassertions = pd.read_excel('...\\path_to_file\\GP - FailClass Assertions.xlsx', sheet_name='dataset'+str(hh))
      passassertions = pd.read_excel('...\\path_to_file\\GP - PassClass Assertions.xlsx', sheet_name='dataset'+str(hh))

      testset = pd.read_excel('...\\path_to_file\\Router_testset.xlsx')
      
      res = testset

      asserts, probs = GetFailAndPassAssertions(failassertions[ind*30 + 540:ind*30 + 29 + 540].reset_index(), passassertions[ind*30 + 540:ind*30 + 29 + 540].reset_index(), theta)

      asserts, probs = ConsistencyCheck(asserts, probs)
      
      res = CalculatePerformance(asserts, probs, testset, res, 'gp'+t)

      import os 

      file_exists = os.path.isfile('GP-'+t+'-coveredpoints-Router-theta'+str(theta)+'-testset.xlsx')

      with pd.ExcelWriter('GP-'+t+'-coveredpoints-Router-theta'+str(theta)+'-testset.xlsx', engine = 'openpyxl', mode = 'a' if file_exists else 'w') as writer:
          res.to_excel(writer, sheet_name = 'dataset'+str(hh), index = False)

