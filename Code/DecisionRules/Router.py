#Decision Rules - RIPPER - NTSS
import ast
import pickle
import wittgenstein as lw
import pandas as pd
from skopt import BayesSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix,balanced_accuracy_score
from sklearn.model_selection import train_test_split

def PreprocessWithoutRep(data, rep):

  i = 0
  j = 0

  newdata = pd.DataFrame(columns = ["TIN 0 Req-BW", "TIN 1 Req-BW", "TIN 2 Req-BW", "TIN 3 Req-BW", "TIN 4 Req-BW", "TIN 5 Req-BW", "TIN 6 Req-BW", "TIN 7 Req-BW", 'TIN5+TIN6+TIIN7', 'Fitness', 'Label'])

  while i < len(data.index):

    newdata.loc[j, 'TIN 0 Req-BW'] = data.loc[i, 'TIN 0 Req-BW']
    newdata.loc[j, 'TIN 1 Req-BW'] = data.loc[i, 'TIN 1 Req-BW']
    newdata.loc[j, 'TIN 2 Req-BW'] = data.loc[i, 'TIN 2 Req-BW']
    newdata.loc[j, 'TIN 3 Req-BW'] = data.loc[i, 'TIN 3 Req-BW']
    newdata.loc[j, 'TIN 4 Req-BW'] = data.loc[i, 'TIN 4 Req-BW']
    newdata.loc[j, 'TIN 5 Req-BW'] = data.loc[i, 'TIN 5 Req-BW']
    newdata.loc[j, 'TIN 6 Req-BW'] = data.loc[i, 'TIN 6 Req-BW']
    newdata.loc[j, 'TIN 7 Req-BW'] = data.loc[i, 'TIN 7 Req-BW']

    newdata.loc[j, 'TIN5+TIN6+TIN7'] = data.loc[i, 'TIN5+TIN6+TIN7']

    newdata.loc[j, 'Fitness'] = data.loc[i, 'Fitness']

    newdata.loc[j, 'Label'] = data.loc[i, 'Label']

    i = i + 1

    j = j + 1

  return newdata



def LabelDataAndPreprocess(data, threshold):

  for i in range(len(data.index)):

    data.loc[i, 'TIN5+TIN6+TIN7'] = data.loc[i, 'TIN 5 Req-BW'] + data.loc[i, 'TIN 6 Req-BW'] + data.loc[i, 'TIN 7 Req-BW']

    if data.loc[i, 'Fitness'] >= threshold:

      data.loc[i, 'Label'] = 'PASS'

    else:

      data.loc[i, 'Label'] = 'FAIL'

  return data

def GetConfSamp(dictt, passorfail, data):

  trues = 0
  inrange = 0

  for i in range(len(data.index)):

    count = 0

    # print('this is dictt')
    # print(dictt)
    for var in dictt:

      if var != 'TIN5+TIN6+TIN7':
        var1 = var[:3] + ' ' + var[3] + ' ' + 'Req-BW'   #uncomment for individual
      else:
        var1 = var
      if dictt[var][2] == "between":

        if  dictt[var][0]<= data.loc[i, var1]<= dictt[var][1]:
          count = count + 1

      elif dictt[var][2] == "greater":

        if  data.loc[i, var1]>= dictt[var][0]:
          count = count + 1

      elif dictt[var][2] == "smaller":

        if  data.loc[i, var1]<= dictt[var][0]:
          count = count + 1

      elif dictt[var][2] == "equal":

        if  data.loc[i, var1]== dictt[var][0]:
          count = count + 1

    if count == len(dictt): #all the variables are in the ranges
      inrange = inrange + 1
      if data.loc[i, 'Label'] == 'FAIL' and passorfail == 'fail': #class 0
          trues = trues + 1
      elif data.loc[i, 'Label'] == 'PASS' and passorfail == 'pass':
          trues = trues + 1
    else:
      continue

  try:
    return (trues/inrange)*100, inrange
  except:
    return trues, inrange
  
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

def FindHighestNumberOfFails(confsandsamp):


  confs  = []
  confsandsamp = [x for x in confsandsamp if x != -1]

  for j in range(len(confsandsamp) - 1):

    c = ast.literal_eval(confsandsamp[j])

    numoffail = (c[0]/100) * c[1]

    # print(confsandsamp)
    # print(type(confsandsamp[-1]))
    rule = ast.literal_eval(confsandsamp[-1])[j]

    confs.append((rule, numoffail))

  confs.sort(key = lambda x: x[1], reverse = True)

  a = [item for item in confs if item[1] == confs[0][1]]

  return a




for hh in range(1, 10):


  res = pd.DataFrame(columns=['Run'+str(i) for i in range(1, 21)])

  data = pd.read_excel('..\\Router'+str(hh)+'.xlsx')  
  
  threshold = 0.8
  data = LabelDataAndPreprocess(data, threshold)
  rep = 10

  data = PreprocessWithoutRep(data, rep)


  X, y = data.loc[:, ['TIN5+TIN6+TIN7']], data.loc[:, 'Label']

  rules = []
  rulesresults = pd.DataFrame(columns = ['Run'])
  for i in range(20):

    try:
      drmodel.fit(X_train, y_train, pos_class = 'PASS')
      params = drmodel.best_params_
      clf = lw.RIPPER(**params)
    except:
      clf = lw.RIPPER(max_rule_conds=16) #if bayesian cannot find a good model, i just use default
    
    clf.fit(X, y, pos_class = 'FAIL')

    with open('router_sum_fail_decisionrule_dataset'+str(hh)+'_run'+str(i)+'.pkl', 'wb') as file:
      pickle.dump(clf, file)

    clf.ruleset_.out_pretty()

    #print(clf.ruleset_.count_conds())
    rules.append(clf.ruleset_)


    
  lastindex = rulesresults.shape[0]

  for k in range(len(rules)):
    listt = []
    for j in range(len(rules[k])):

      listt.append(str(rules[k][j]))

      c = str(rules[k][j])
      dictt = ExtractBounds(c)

      #print(a,b)

      conf, samples = GetConfSamp(dictt, 'fail', data)

      print(conf, samples)
      rulesresults.loc[j + lastindex, 'RUN'+str(k+1)] = str((conf, samples))


    print("*************")

    rulesresults.loc[j+lastindex+1, 'RUN'+str(k+1)] = str(listt)


  indeces = []

  for i in range(1, 21):
    rulesresults['RUN'+str(i)] = rulesresults['RUN'+str(i)].fillna(-1)

    # rule, fitness = FindBasedonTarantula(data.loc[:, 'RUN'+str(i)].values.tolist())
    f_path = FindHighestNumberOfFails(rulesresults.loc[:, 'RUN'+str(i)].values.tolist())


    for j in range(len(f_path)):

      res.loc[j, 'Run'+str(i)] = f_path[j][0]

    print('this is j ', j)
    
    res.loc[j + 1, 'Run'+str(i)] = '####'
    indeces.append(j + 2)


  ##########################PASS CLASS#############################

  rules = []
  rulesresults = pd.DataFrame(columns = ['Run'])
  for i in range(20):

    drmodel = BayesSearchCV(lw.RIPPER(max_rule_conds=16), {'prune_size': [0.1, 0.8], 'k': [1, 3]}, optimizer_kwargs = {'acq_func': 'EI'})

    try:
      drmodel.fit(X_train, y_train, pos_class = 'PASS')
      params = drmodel.best_params_
      clf = lw.RIPPER(**params)
    except:
      clf = lw.RIPPER(max_rule_conds=16) #if bayesian cannot find a good model, i just use default

    clf.fit(X, y, pos_class = 'PASS')

    with open('router_sum_pass_decisionrule_dataset'+str(hh)+'_run'+str(i)+'.pkl', 'wb') as file:
      pickle.dump(clf, file)

    # y_pred = clf.predict(X_test)

    clf.ruleset_.out_pretty()

    #print(clf.ruleset_.count_conds())
    rules.append(clf.ruleset_)


    
  lastindex = rulesresults.shape[0]

  for k in range(len(rules)):
    listt = []
    for j in range(len(rules[k])):

      listt.append(str(rules[k][j]))

      c = str(rules[k][j])
      dictt = ExtractBounds(c)

      #print(a,b)

      conf, samples = GetConfSamp(dictt, 'pass', data)

      print(conf, samples)
      rulesresults.loc[j + lastindex, 'RUN'+str(k+1)] = str((conf, samples))


    print("*************")

    rulesresults.loc[j+lastindex+1, 'RUN'+str(k+1)] = str(listt)


  for i in range(1, 21):
    rulesresults['RUN'+str(i)] = rulesresults['RUN'+str(i)].fillna(-1)

    # rule, fitness = FindBasedonTarantula(data.loc[:, 'RUN'+str(i)].values.tolist())
    p_path = FindHighestNumberOfFails(rulesresults.loc[:, 'RUN'+str(i)].values.tolist())


    for j in range(len(p_path)):

      res.loc[indeces[i-1], 'Run'+str(i)] = p_path[j][0]  

  res.to_excel("DR-router-sum-dataset"+str(hh)+".xlsx")
