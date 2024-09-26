#building decision Tree on NTSS and extracting rules

import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import numpy as np
from sklearn import tree
from sklearn.tree import _tree
import re
import pickle

def get_rules(tree, feature_names, class_names): #https://mljar.com/blog/extract-rules-decision-tree/
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    paths = []
    path = []

    def recurse(node, path, paths):

        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            path += [(tree_.value[node], tree_.n_node_samples[node])]
            paths += [path]

    recurse(0, path, paths)

    # sort by samples count
    samples_count = [p[-1][1] for p in paths]
    ii = list(np.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]


    rules = []
    for path in paths:
        rule = "if "

        for p in path[:-1]:
            if rule != "if ":
                rule += " and "
            rule += str(p)
        rule += " then "
        if class_names is None:
            rule += "response: "+str(np.round(path[-1][0][0][0],3))
        else:
            classes = path[-1][0][0]
            l = np.argmax(classes)
            rule += f"class: {class_names[l]} (proba: {np.round(100.0*classes[l]/np.sum(classes),2)}%)"
        rule += f" | based on {path[-1][1]:,} samples"
        rules += [rule]

    return rules






def PreprocessDataWithout(data, rep, column):

  i = 0
  j = 0

  # newdata = pd.DataFrame(columns = ["TIN 0 Req-BW", "TIN 1 Req-BW", "TIN 2 Req-BW", "TIN 3 Req-BW", "TIN 4 Req-BW", "TIN 5 Req-BW", "TIN 6 Req-BW", "TIN 7 Req-BW", 'TIN5+TIN6+TIIN7', 'Fitness', 'Label'])

  newdata = pd.DataFrame(columns = column)

  while i < len(data.index):

    # newdata.loc[j, 'TIN 0 Req-BW'] = data.loc[i, 'TIN 0 Req-BW']
    # newdata.loc[j, 'TIN 1 Req-BW'] = data.loc[i, 'TIN 1 Req-BW']
    # newdata.loc[j, 'TIN 2 Req-BW'] = data.loc[i, 'TIN 2 Req-BW']
    # newdata.loc[j, 'TIN 3 Req-BW'] = data.loc[i, 'TIN 3 Req-BW']
    # newdata.loc[j, 'TIN 4 Req-BW'] = data.loc[i, 'TIN 4 Req-BW']
    # newdata.loc[j, 'TIN 5 Req-BW'] = data.loc[i, 'TIN 5 Req-BW']
    # newdata.loc[j, 'TIN 6 Req-BW'] = data.loc[i, 'TIN 6 Req-BW']
    # newdata.loc[j, 'TIN 7 Req-BW'] = data.loc[i, 'TIN 7 Req-BW']

    # newdata.loc[j, 'TIN5+TIN6+TIN7'] = data.loc[i, 'TIN5+TIN6+TIN7']

    # newdata.loc[j, 'Fitness'] = data.loc[i, 'Fitness']

    newdata.loc[j, 'Label'] = data.loc[i, 'Label']

    newdata.loc[j, :] = data.loc[i, :]

    i = i + 1

    j = j + 1

  return newdata

def SplitDataCL(dataa, column):

  X = dataa[column].values.tolist()

  y = dataa['Label'].values.tolist()

  return X, y


def FeatureEngineering(data):

  from itertools import combinations

  tins = ['TIN' + str(i) for i in range(8)]

 
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

      print(features[i])

      f = features[i].split('+')

      if len(f) == 1:
        continue
        
      s = 0


      for j in range(len(f)):

        s = data.loc[hh, 'TIN ' + str(f[j][-1]) + ' Req-BW'] + s

      data.loc[hh, features[i]] = s


  return data, features




def LabelNTSS(ntssdata):

  for i in range(len(ntssdata.index)):

    if ntssdata.loc[i, 'Fitness'] < 0.8:

      ntssdata.loc[i, 'Label'] = 'FAIL'

    else:

      ntssdata.loc[i, 'Label'] = 'PASS'

  return ntssdata


def ExtractPathsWithHigherCoveredFailTests(classifier):

  rules = get_rules(classifier, column, ['FAIL', 'PASS'])

  # print(rules)

  maxfailsamples = 0
  bestpath = ""

  pathandnumfails = []

  for g in range(len(rules)):

    numberoffailsinthesamples = 0

    pattern = r'then class: (.+?)'

    match = re.search(pattern, rules[g])

    if match:
        # Extract the number from the matched group
        theclass = match.group(1)
        # print(theclass)

    else:
      print("No classes!!!")


    if theclass == 'F':

      pattern = r'\(proba: (\d+\.\d+)%\)'

      # Use re.search to find the match
      match = re.search(pattern, rules[g])

      if match:
          prob = float(match.group(1))  # Convert the matched string to a float
          # print("Extracted numeric value:", numeric_value)
      else:
          print("No probability found.")


      pattern = r'based on (\d+) samples'

      match = re.search(pattern, rules[g])

      if match:
          # Extract the number from the matched group
          samplescovered = int(match.group(1))

      else:
        print("No samples!!!")


      numberoffailsinthesamples = int(samplescovered * prob/100)


    elif theclass == 'P':

      pattern = r'\(proba: (\d+\.\d+)%\)'

      # Use re.search to find the match
      match = re.search(pattern, rules[g])

      if match:
          prob = 100 - float(match.group(1))  # Convert the matched string to a float
          # print("Extracted numeric value:", numeric_value)
      else:
          print("No probability found.")


      pattern = r'based on (\d+) samples'

      match = re.search(pattern, rules[g])

      if match:
          # Extract the number from the matched group
          samplescovered = int(match.group(1))

      else:
        print("No samples!!!")


      numberoffailsinthesamples = int(samplescovered * prob/100)

    pathandnumfails.append((rules[g], numberoffailsinthesamples))

      # print('this is number of samples', numberoffailsinthesamples)

    # if maxfailsamples < numberoffailsinthesamples:
    #   maxfailsamples = numberoffailsinthesamples
    #   bestpath = rules[g]
  pathandnumfails.sort(key=lambda x: x[1], reverse = True)

  
  a = [item for item in pathandnumfails if item[1] == pathandnumfails[0][1]]
  
  
  return a

def ExtractPathsWithHigherCoveredPassTests(classifier):

  rules = get_rules(classifier, column, ['FAIL', 'PASS'])

  # print(rules)

  maxfailsamples = 0
  bestpath = ""

  pathandnumfails = []

  for g in range(len(rules)):

    numberoffailsinthesamples = 0

    pattern = r'then class: (.+?)'

    match = re.search(pattern, rules[g])

    if match:
        # Extract the number from the matched group
        theclass = match.group(1)
        # print(theclass)

    else:
      print("No classes!!!")


    if theclass == 'F':

      pattern = r'\(proba: (\d+\.\d+)%\)'

      # Use re.search to find the match
      match = re.search(pattern, rules[g])

      if match:
          prob = 1 -  float(match.group(1))  # Convert the matched string to a float
          # print("Extracted numeric value:", numeric_value)
      else:
          print("No probability found.")


      pattern = r'based on (\d+) samples'

      match = re.search(pattern, rules[g])

      if match:
          # Extract the number from the matched group
          samplescovered = int(match.group(1))

      else:
        print("No samples!!!")


      numberoffailsinthesamples = int(samplescovered * prob/100)


    elif theclass == 'P':

      pattern = r'\(proba: (\d+\.\d+)%\)'

      # Use re.search to find the match
      match = re.search(pattern, rules[g])

      if match:
          prob = float(match.group(1))  # Convert the matched string to a float
          # print("Extracted numeric value:", numeric_value)
      else:
          print("No probability found.")


      pattern = r'based on (\d+) samples'

      match = re.search(pattern, rules[g])

      if match:
          # Extract the number from the matched group
          samplescovered = int(match.group(1))

      else:
        print("No samples!!!")


      numberoffailsinthesamples = int(samplescovered * prob/100)

    pathandnumfails.append((rules[g], numberoffailsinthesamples))

      # print('this is number of samples', numberoffailsinthesamples)

    # if maxfailsamples < numberoffailsinthesamples:
    #   maxfailsamples = numberoffailsinthesamples
    #   bestpath = rules[g]
  pathandnumfails.sort(key=lambda x: x[1], reverse = True)

  
  a = [item for item in pathandnumfails if item[1] == pathandnumfails[0][1]]
  
  
  return a


for hh in range(1, 10):

  ntssdata = pd.read_excel('..\\Router'+str(hh)+'.xlsx')

  res = pd.DataFrame(columns = ['Run'+str(i) for i in range(1, 21)])

  ntssdata = LabelNTSS(ntssdata)

  ntssdata, column = FeatureEngineering(ntssdata)

  rep = 10


  ntsswithout = PreprocessDataWithout(ntssdata, rep, column)

  
  X, y = SplitDataCL(ntsswithout, column)#change this part for with or without

  y = np.array(y)
  y = y.reshape(-1, 1)

  fpaths = []
  for run in range(20):

    classifier = DecisionTreeClassifier(max_depth = 5, class_weight= 'balanced')

    classifier.fit(X, y)

    pickle_file = "router_sum_decision_tree_dataset"+str(hh)+"_run"+str(run)+".pkl"
    with open(pickle_file, 'wb') as file:
        pickle.dump(classifier, file)


    f_path = ExtractPathsWithHigherCoveredFailTests(classifier)

    
    for i in range(len(f_path)):

      res.loc[i, 'Run'+str(run+1)] = f_path[i][0]
    
    
    res.loc[res.shape[0], 'Run'+str(run+1)] = ''

    
    p_path = ExtractPathsWithHigherCoveredPassTests(classifier)


    for i in range(len(p_path)):

      res.loc[i + 1 + len(f_path), 'Run'+str(run+1)] = p_path[i][0]

  
  res.to_excel('router-decisiontree-sum-dataset'+str(hh)+'.xlsx')
