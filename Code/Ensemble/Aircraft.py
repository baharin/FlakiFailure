from collections import defaultdict
# !pip install z3-solver
from z3 import *
import ast
import copy
import random
import pandas as pd

import heapq

def ExtractRanges(rule, model):

    dictt = {'ARG0': [0, 1], 'ARG1': [0, 1], 'ARG2' : [0, 45], 'ARG3': [0, 45], 'ARG4': [-30, 30], 'ARG5': [-30, 30], 'ARG6': [0, 1], 'ARG7': [0, 1]}

    for i in range(len(rule)):

        if rule[i][0] == 'greater_than_func':

            dictt[rule[i][1]][0] = float(rule[i][2]) + 0.1  #because the func is >

        elif rule[i][0] == 'less_than_func':

            dictt[rule[i][1]][1] = float(rule[i][2]) - 0.1 #because the func is <

        elif rule[i][0] == 'equal_to':

            dictt[rule[i][1]][0] = float(rule[i][2])
            dictt[rule[i][1]][1] = float(rule[i][2])

    return dictt

def CalculatePerformance(fail_assertions, pass_assertions, dataset, model, res, run):

    covered_values = [('No', -1, -1, -1)] * len(res.index)

    res['Covered'+run] = covered_values

  
    for jj in range(len(fail_assertions)): #iterate over fail rules

      rule = ast.literal_eval(fail_assertions[jj])

      ranges = ExtractRanges(rule, model)

      for h in range(len(dataset.index)):
           
       if ranges['ARG0'][0] <= float(dataset.loc[h, 'ALT_Mode1']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <= float(dataset.loc[h, 'ALT_Mode2']) <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'TurnK1']) <= ranges['ARG2'][1] and ranges['ARG3'][0] <= float(dataset.loc[h, 'TurnK2']) <= ranges['ARG3'][1] and ranges['ARG4'][0] <= float(dataset.loc[h, 'Pwheel1']) <= ranges['ARG4'][1] and ranges['ARG5'][0] <= float(dataset.loc[h, 'Pwheel2']) <= ranges['ARG5'][1] and ranges['ARG6'][0] <= float(dataset.loc[h, 'Throttle1']) <= ranges['ARG6'][1] and ranges['ARG7'][0] <= float(dataset.loc[h, 'Throttle2']) <= ranges['ARG7'][1]:

            if res.loc[h, 'Covered'+run][0] != 'No': 

                continue

            else:

                res.at[h, 'Covered'+run] = ('0', rule)
           

    for jj in range(len(pass_assertions)): #iterate over pass rules

      rule = ast.literal_eval(pass_assertions[jj])

      
      ranges = ExtractRanges(rule, model)


      for h in range(len(dataset.index)):
          
       if ranges['ARG0'][0] <= float(dataset.loc[h, 'ALT_Mode1']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <= float(dataset.loc[h, 'ALT_Mode2']) <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'TurnK1']) <= ranges['ARG2'][1] and ranges['ARG3'][0] <= float(dataset.loc[h, 'TurnK2']) <= ranges['ARG3'][1] and ranges['ARG4'][0] <= float(dataset.loc[h, 'Pwheel1']) <= ranges['ARG4'][1] and ranges['ARG5'][0] <= float(dataset.loc[h, 'Pwheel2']) <= ranges['ARG5'][1] and ranges['ARG6'][0] <= float(dataset.loc[h, 'Throttle1']) <= ranges['ARG6'][1] and ranges['ARG7'][0] <= float(dataset.loc[h, 'Throttle2']) <= ranges['ARG7'][1]:

            if res.loc[h, 'Covered'+run][0] != 'No': 
                continue

            else:

                res.at[h, 'Covered'+run] = ('1', rule)

    return res


class Vertex:
    def __init__(self, id, degree, weight, part):
        self.id = id
        self.degree = degree
        self.weight = weight
        self.part = part

    def __lt__(self, other):

        if self.weight != other.weight:
            return self.weight > other.weight
        if self.degree != other.degree:
            return self.degree > other.degree
        return self.part == 'A' and other.part == 'B' #part A is pass, part B is fail

def remove_vertices(graph, part_A, part_B, weights):
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}

    vertices = []

    for v in graph:
        part = 'A' if v in part_A else 'B'
        heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))
        vertices.sort()
        print([v.id for v in vertices])

    removed_vertices = set()

    removed_vertices_withpassfail = set()

    while vertices:
        vertex = heapq.heappop(vertices)
        # print('this is the poped item: ', vertex.id)

        if vertex.id in removed_vertices:
            continue
        removed_vertices.add(vertex.id)
        removed_vertices_withpassfail.add(vertex)

        while len(list(graph[vertex.id])) > 0:  #iterate over neighbors of vertex
            neighbor = list(graph[vertex.id])[0]
            # print('this is the neighbor: ', neighbor)
            graph[neighbor].remove(vertex.id)
            if neighbor not in removed_vertices:
                degrees[neighbor] -= 1

            graph[vertex.id].remove(neighbor)

        graph.pop(vertex.id)

        for v in graph: #reconstruct the heap
          part = 'A' if v in part_A else 'B'
          heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))
          vertices.sort()

        if all(not neighbors for neighbors in graph.values()):
            break



    return sorted(removed_vertices), sorted(removed_vertices_withpassfail, key = lambda v: v.id)

def CreateFormula(rule):

  rule = ast.literal_eval(rule)

  numberofpredicates = len(rule)

  f = [ 0 for i in range(len(rule))]

  for i, predicate in enumerate(rule):

    var1 = Real(predicate[1])

    if predicate[0] == 'greater_than_func':

        f[i] = And(var1 > float(predicate[2]))

    elif predicate[0] == 'less_than_func':

        f[i] = And(var1 < float(predicate[2]))

    elif predicate[0] == 'equal_to':

        f[i] = And(var1 == float(predicate[2]))


  finalformula = f[0]

  for ff in f[1:]:

    finalformula = And(finalformula, ff)


  return finalformula

def remove_common_elements(list1, list2):

    set1 = set(list1)
    set2 = set(list2)
    common_elements = set1 & set2

    list1 = [item for item in list1 if item not in common_elements]
    list2 = [item for item in list2 if item not in common_elements]

    return list1, list2


def GPFindPassandFail(data, theta, run):

  i = 0

  fail_assertions = []

  pass_assertions =  []

  for kk in range(3):

    while data.loc[i, run] != [] and data.loc[i, run] != '[]':

      if data.loc[i, run+'Prob'] >= theta:

        fail_assertions.append(data.loc[i, run])

      i = i + 1

    i = i + 1

    while data.loc[i, run] != [] and data.loc[i, run] != '[]':

      if data.loc[i, run+'Prob'] >= theta:

        pass_assertions.append(data.loc[i, run])

      i = i + 1

    i = i + 1

  return fail_assertions, pass_assertions


def FindPassandFail(data, theta, run):

  i = 0

  fail_assertions = []

  pass_assertions =  []

  while i < len(data.index) and data.loc[i, run] != [] and data.loc[i, run] != '[]':

    if data.loc[i, run+'Prob'] >= theta:

      fail_assertions.append(data.loc[i, run])

    i = i + 1

  i = i + 1

  while i < len(data.index) and data.loc[i, run] != [] and data.loc[i, run] != '[]':

    if data.loc[i, run+'Prob'] >= theta:

      pass_assertions.append(data.loc[i, run])

    i = i + 1

  return fail_assertions, pass_assertions




results = []


thetas = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
runs = ['Run'+str(j) for j in range(1, 21)]

for theta in thetas:

  for m, model in enumerate(['R121']):

    GPdata = pd.read_excel('...\\GPruleswithProb.xlsx')
    GPdata = GPdata[m: m+126]
    GPdata = GPdata.reset_index(drop=True)
        
    
    dtdata = pd.read_excel('.../DT-AP.xlsx')
    drdata = pd.read_excel('.../DR-AP.xlsx')

    testset = pd.read_excel('.../AP_testset.xlsx')

    res = testset

    for run in runs:

      gpfail_assertions, gppass_assertions = GPFindPassandFail(GPdata, theta, run)

      dtfail_assertions, dtpass_assertions = FindPassandFail(dtdata, theta, run)

      drfail_assertions, drpass_assertions = FindPassandFail(drdata, theta, run)

      
      fail_assertions = gpfail_assertions
      pass_assertions = gppass_assertions

      fail_assertions.extend(dtfail_assertions)
      pass_assertions.extend(dtpass_assertions)

      fail_assertions.extend(drfail_assertions)
      pass_assertions.extend(drpass_assertions)


      i = 0
      j = 0


      s = Solver()


      inconsistencies = defaultdict(list)  

      while i < len(pass_assertions):

          A_1 = pass_assertions[i]

          A = CreateFormula(A_1)

          j = 0

          while j < len(fail_assertions):

              s = Solver()
              B_1 = fail_assertions[j]

              B = CreateFormula(B_1)

              s.add(A, B)
              if s.check() == sat:
                  # A and B are inconsistent
                  print(f"Inconsistent pair found: {A} and {B}")

                  inconsistencies[A_1].append(B_1)

                  inconsistencies[B_1].append(A_1)

              else:
                  print(f"Consistent pair found: {A} and {B}")

              j += 1

          i += 1


      weights = {}

      for i in range(len(pass_assertions)):

        rule = ast.literal_eval(pass_assertions[i])

        weights[pass_assertions[i]] = 1/len(rule)

      for i in range(len(fail_assertions)):

        rule = ast.literal_eval(fail_assertions[i])

        weights[fail_assertions[i]] = 1/len(rule)

      ######################
      removed_vertices, removed_vertices_withpassfail = remove_vertices(inconsistencies, pass_assertions, fail_assertions, weights)

      for item in removed_vertices_withpassfail:
        if item.part == 'A': #from pass
          pass_assertions.remove(item.id)
        else:
          fail_assertions.remove(item.id)

      ########################### covered points ##############################

      res = CalculatePerformance(fail_assertions, pass_assertions, testset, model, res, run)

    import os 

    file_exists = os.path.isfile('Ensemble'+'-coveredpoints-'+model+'-theta'+str(theta)+'-testset.xlsx')

    with pd.ExcelWriter('Ensemble'+'-coveredpoints-'+model+'-theta'+str(theta)+'-testset.xlsx', engine = 'openpyxl', mode = 'a' if file_exists else 'w') as writer:
        res.to_excel(writer, sheet_name = 'dataset', index = False)
