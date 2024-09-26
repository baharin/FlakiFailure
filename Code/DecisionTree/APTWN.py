import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier, export_text, plot_tree
import numpy as np
from sklearn import tree
from sklearn.tree import _tree
import re
import matplotlib.pyplot as plt
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



def PreprocessDataWithout(data, rep, labelcol):

  i = 0
  j = 0

  newdata = pd.DataFrame(columns = ["Weather_0", "Weather_1", 'Weather_2', 'Weather_3', 'Weather_4', 'Weather_5', 'Weather_6', 'MaxSpeed', 'Traffic Amount', 'Label'])

  while i < len(data.index):

    for kk in range(7):

      newdata.loc[j, 'Weather_'+str(kk)] = data.loc[i, 'Weather_'+str(kk)]

    newdata.loc[j, 'MaxSpeed'] = data.loc[i, 'MaxSpeed']

    newdata.loc[j, 'Traffic Amount'] = data.loc[i, 'Traffic Amount']

    # newdata.loc[j, 'MinimumOOBDistance'] = data.loc[i, 'MinimumOOBDistance']

    newdata.loc[j, labelcol] = data.loc[i, labelcol]


    i = i + 1

    j = j + 1

  return newdata

def SplitData(dataa, labelcol):

  X = dataa[["Weather_0", "Weather_1", 'Weather_2', 'Weather_3', 'Weather_4', 'Weather_5', 'Weather_6', "MaxSpeed", "Traffic Amount"]]

  y = dataa[labelcol]

  return X, y

def PreprocessDataForWeather(dataa):

  dataa['Weather'] = dataa['Weather'].astype(int)

  df_encoded = pd.get_dummies(dataa, columns=['Weather'], prefix=['Weather'])

  return df_encoded



def ExtractPathsWithHigherCoveredFailTests(classifier, X):

  rules = get_rules(classifier, ["Weather_0", "Weather_1", 'Weather_2', 'Weather_3', 'Weather_4', 'Weather_5', 'Weather_6', 'MaxSpeed', 'Traffic Amount'], ['0', '1'])

  # print(rules)

  maxfailsamples = 0
  bestpath = ""

  pathandnumfails = []

  for g in range(len(rules)):

    # print('this is rules ', rules[g])

    numberoffailsinthesamples = 0

    pattern = r'then class: (.+?)'

    match = re.search(pattern, rules[g])

    if match:
        # Extract the number from the matched group
        theclass = match.group(1)
        # print(theclass)

    else:
      print("No classes!!!")


    if theclass == '0':

      # print('this is rule ', rules[g])

      pattern = r'\(proba: (\d+\.\d+)%\)'

      # Use re.search to find the match
      match = re.search(pattern, rules[g])

      if match:
          prob = float(match.group(1))  # Convert the matched string to a float
          # print("Extracted numeric value:", numeric_value)
      else:
          print("No probability found.")


      # pattern = r'based on (\d+) samples'
      pattern = r'based on (\d{1,3}(?:,\d{3})*) samples'

      match = re.search(pattern, rules[g])

      if match:
          # Extract the number from the matched group
          samplescovered = int(match.group(1).replace(',', ''))
          # print('this is samples coveered ', samplescovered)

      else:
        print("No samples!!!")


      numberoffailsinthesamples = int(samplescovered * prob/100)

      # print('this is number of samples', numberoffailsinthesamples)

    elif theclass == '1':

      # print('this is rule ', rules[g])

      pattern = r'\(proba: (\d+\.\d+)%\)'

      # Use re.search to find the match
      match = re.search(pattern, rules[g])

      if match:
          prob = 100 - float(match.group(1))  # Convert the matched string to a float      #find the probability of fail class
          # print("Extracted numeric value:", numeric_value)
      else:
          print("No probability found.")


      # pattern = r'based on (\d+) samples'
      pattern = r'based on (\d{1,3}(?:,\d{3})*) samples'

      match = re.search(pattern, rules[g])

      if match:
          # Extract the number from the matched group
          samplescovered = int(match.group(1).replace(',', ''))
          # print('this is samples coveered ', samplescovered)

      else:
        print("No samples!!!")


      numberoffailsinthesamples = int(samplescovered * prob/100)

      # print('this is number of samples', numberoffailsinthesamples)

    pathandnumfails.append((rules[g], numberoffailsinthesamples))


  pathandnumfails.sort(key=lambda x: x[1], reverse = True)

  
  a = [item for item in pathandnumfails if item[1] == pathandnumfails[0][1]]

  return a

def ExtractPathsWithHigherCoveredPassTests(classifier, X):

  rules = get_rules(classifier, ["Weather_0", "Weather_1", 'Weather_2', 'Weather_3', 'Weather_4', 'Weather_5', 'Weather_6', 'MaxSpeed', 'Traffic Amount'], ['0', '1'])

  # print(rules)

  maxfailsamples = 0
  bestpath = ""

  pathandnumfails = []

  for g in range(len(rules)):

    # print('this is rules ', rules[g])

    numberoffailsinthesamples = 0

    pattern = r'then class: (.+?)'

    match = re.search(pattern, rules[g])

    if match:
        # Extract the number from the matched group
        theclass = match.group(1)
        # print(theclass)

    else:
      print("No classes!!!")


    if theclass == '0':

      # print('this is rule ', rules[g])

      pattern = r'\(proba: (\d+\.\d+)%\)'

      # Use re.search to find the match
      match = re.search(pattern, rules[g])

      if match:
          prob = 100 -float(match.group(1))  # Convert the matched string to a float
          # print("Extracted numeric value:", numeric_value)
      else:
          print("No probability found.")


      # pattern = r'based on (\d+) samples'
      pattern = r'based on (\d{1,3}(?:,\d{3})*) samples'

      match = re.search(pattern, rules[g])

      if match:
          # Extract the number from the matched group
          samplescovered = int(match.group(1).replace(',', ''))
          # print('this is samples coveered ', samplescovered)

      else:
        print("No samples!!!")


      numberoffailsinthesamples = int(samplescovered * prob/100)

      # print('this is number of samples', numberoffailsinthesamples)

    elif theclass == '1':

      # print('this is rule ', rules[g])

      pattern = r'\(proba: (\d+\.\d+)%\)'

      # Use re.search to find the match
      match = re.search(pattern, rules[g])

      if match:
          prob = float(match.group(1))  # Convert the matched string to a float      #find the probability of fail class
          # print("Extracted numeric value:", numeric_value)
      else:
          print("No probability found.")


      # pattern = r'based on (\d+) samples'
      pattern = r'based on (\d{1,3}(?:,\d{3})*) samples'

      match = re.search(pattern, rules[g])

      if match:
          # Extract the number from the matched group
          samplescovered = int(match.group(1).replace(',', ''))
          # print('this is samples coveered ', samplescovered)

      else:
        print("No samples!!!")


      numberoffailsinthesamples = int(samplescovered * prob/100)

      # print('this is number of samples', numberoffailsinthesamples)

    pathandnumfails.append((rules[g], numberoffailsinthesamples))


  pathandnumfails.sort(key=lambda x: x[1], reverse = True)

  
  a = [item for item in pathandnumfails if item[1] == pathandnumfails[0][1]]

  return a




a = input('select requirement: R1, R2, R3, R3')

if a  == 'R1':

  label = 'Label'

elif a == 'R2':

  label = 'Label(Damage)'

elif a == 'R3':

  label = 'Label(Ultra)'

elif a == 'R4':

  label = 'Label(Distance)'
  
for hh in range(1, 10):

  if a == 'R1':

    towndata = pd.read_csv('...\\AP-TWN - R1 - '+str(hh)+'.csv')

  else:

    towndata = pd.read_csv('...\\AP-TWN - R2 to R4 - '+str(hh)+'.csv')

  res = pd.DataFrame(columns = ['Run'+str(i) for i in range(1, 21)])

  towndata = PreprocessDataForWeather(towndata)

  townwithout = PreprocessDataWithout(towndata, rep = 10, labelcol = label)


  X, y = SplitData(townwithout, label)

  y = y.astype(int)

  fpaths = []
  for run in range(20):

    classifier = DecisionTreeClassifier(max_depth = 5, class_weight = 'balanced')


    classifier.fit(X, y)


    pickle_file = a+"_decision_tree_dataset"+str(hh)+"_run"+str(run)+".pkl"
    with open(pickle_file, 'wb') as file:
        pickle.dump(classifier, file)


    f_path = ExtractPathsWithHigherCoveredFailTests(classifier, X)

    
    for i in range(len(f_path)):

      res.loc[i, 'Run'+str(run+1)] = f_path[i][0]
    
    
    res.loc[res.shape[0], 'Run'+str(run+1)] = ''

    
    p_path = ExtractPathsWithHigherCoveredPassTests(classifier, X)


    for i in range(len(p_path)):

      res.loc[i + 1 + len(f_path), 'Run'+str(run+1)] = p_path[i][0]

  res.to_excel(a+'-decisiontree-dataset'+str(hh)+'.xlsx')
