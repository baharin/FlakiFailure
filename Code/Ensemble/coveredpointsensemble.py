#ensemble consistency checking AP based on theta. and finding covered points.

from collections import defaultdict
# !pip install z3-solver
from z3 import *
import ast
import copy
import random
import pandas as pd

import heapq

def ExtractRanges(rule, model):
    if model == 'R141':
        dictt = {'ARG0': [0, 1], 'ARG1': [0, 1], 'ARG2' : [0, 45], 'ARG3': [-30, 30]}

    elif model == 'R16':
      
        dictt = {'ARG0': [0, 1], 'ARG1': [0, 1], 'ARG2': [0, 1], 'ARG3': [0, 1], 'ARG4': [0, 1], 'ARG5': [0, 1], 'ARG6' : [0, 45], 'ARG7': [0, 45], 'ARG8': [0, 45], 'ARG9': [-30, 30], 'ARG10': [-30, 30], 'ARG11': [-30, 30]}

    elif model == 'R121':
        
        dictt = {'ARG0': [0, 1], 'ARG1': [0, 1], 'ARG2' : [0, 45], 'ARG3': [0, 45], 'ARG4': [-30, 30], 'ARG5': [-30, 30], 'ARG6': [0, 1], 'ARG7': [0, 1]}

    print('this is rule ', rule, model, len(rule), type(rule)) #[('greater_than_func', 'ARG2', '29')]

    for i in range(len(rule)):

        if rule[i][0] == 'greater_than_func':

            print('here')

            dictt[rule[i][1]][0] = float(rule[i][2]) + 0.1  #because the func is >

        elif rule[i][0] == 'less_than_func':

            dictt[rule[i][1]][1] = float(rule[i][2]) - 0.1 #because the func is <

        elif rule[i][0] == 'equal_to':

            dictt[rule[i][1]][0] = float(rule[i][2])
            dictt[rule[i][1]][1] = float(rule[i][2])

    print(dictt)

    return dictt

def CalculatePerformance(fail_assertions, pass_assertions, dataset, model, res, run):

    covered_values = [('No', -1, -1, -1)] * len(res.index)

    res['Covered'+run] = covered_values

  
    for jj in range(len(fail_assertions)): #iterate over fail rules

      rule = ast.literal_eval(fail_assertions[jj])

      print('this is rule', rule)
      ranges = ExtractRanges(rule, model)

      print('this is ranges', ranges)

      for h in range(len(dataset.index)):

        if model == 'R141':

            if ranges['ARG0'][0] <= float(dataset.loc[h, 'AP_Eng1']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <= float(dataset.loc[h, 'ALT_Mode1']) <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'TurnK1']) <= ranges['ARG2'][1] and ranges['ARG3'][0] <= float(dataset.loc[h, 'Pwheel1']) <= ranges['ARG3'][1]:

                if res.loc[h, 'Covered'+run][0] != 'No': # if this test input is already covered by another rule

                    continue

                elif res.loc[h, 'Covered'+run][0] == 'No':

                    res.at[h, 'Covered'+run] = ('0', rule)

        elif model == 'R16':
           
           if ranges['ARG0'][0] <= float(dataset.loc[h, 'AP_Eng1']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <= float(dataset.loc[h, 'AP_Eng2']) <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'AP_Eng3']) <= ranges['ARG2'][1] and ranges['ARG3'][0] <= float(dataset.loc[h, 'ALT_Mode1']) <= ranges['ARG3'][1] and ranges['ARG4'][0] <= float(dataset.loc[h, 'ALT_Mode2']) <= ranges['ARG4'][1] and ranges['ARG5'][0] <= float(dataset.loc[h, 'ALT_Mode3']) <= ranges['ARG5'][1] and ranges['ARG6'][0] <= float(dataset.loc[h, 'TurnK1']) <= ranges['ARG6'][1] and ranges['ARG7'][0] <= float(dataset.loc[h, 'TurnK2']) <= ranges['ARG7'][1] and ranges['ARG8'][0] <= float(dataset.loc[h, 'TurnK3']) <= ranges['ARG8'][1] and ranges['ARG9'][0] <= float(dataset.loc[h, 'Pwheel1']) <= ranges['ARG9'][1] and ranges['ARG10'][0] <= float(dataset.loc[h, 'Pwheel2']) <= ranges['ARG10'][1] and ranges['ARG11'][0] <= float(dataset.loc[h, 'Pwheel3']) <= ranges['ARG11'][1]:

                if res.loc[h, 'Covered'+run][0] != 'No': # if this test input is already covered by another rule

                    continue

                else:

                    res.at[h, 'Covered'+run] = ('0', rule)

        elif model == 'R121':
           
           if ranges['ARG0'][0] <= float(dataset.loc[h, 'ALT_Mode1']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <= float(dataset.loc[h, 'ALT_Mode2']) <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'TurnK1']) <= ranges['ARG2'][1] and ranges['ARG3'][0] <= float(dataset.loc[h, 'TurnK2']) <= ranges['ARG3'][1] and ranges['ARG4'][0] <= float(dataset.loc[h, 'Pwheel1']) <= ranges['ARG4'][1] and ranges['ARG5'][0] <= float(dataset.loc[h, 'Pwheel2']) <= ranges['ARG5'][1] and ranges['ARG6'][0] <= float(dataset.loc[h, 'Throttle1']) <= ranges['ARG6'][1] and ranges['ARG7'][0] <= float(dataset.loc[h, 'Throttle2']) <= ranges['ARG7'][1]:

                if res.loc[h, 'Covered'+run][0] != 'No': # if this test input is already covered by another rule

                    continue

                else:

                    res.at[h, 'Covered'+run] = ('0', rule)
           

    for jj in range(len(pass_assertions)): #iterate over pass rules

      rule = ast.literal_eval(pass_assertions[jj])

      print('this is rule', rule)
      ranges = ExtractRanges(rule, model)


      for h in range(len(dataset.index)):

        if model == 'R141':

            if ranges['ARG0'][0] <= float(dataset.loc[h, 'AP_Eng1']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <= float(dataset.loc[h, 'ALT_Mode1']) <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'TurnK1']) <= ranges['ARG2'][1] and ranges['ARG3'][0] <= float(dataset.loc[h, 'Pwheel1']) <= ranges['ARG3'][1]:

                if res.loc[h, 'Covered'+run][0] != 'No': # if this test input is already covered by another rule

                    continue

                elif res.loc[h, 'Covered'+run][0] == 'No':

                    res.at[h, 'Covered'+run] = ('1', rule)

        elif model == 'R16':
           if ranges['ARG0'][0] <= float(dataset.loc[h, 'AP_Eng1']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <= float(dataset.loc[h, 'AP_Eng2']) <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'AP_Eng3']) <= ranges['ARG2'][1] and ranges['ARG3'][0] <= float(dataset.loc[h, 'ALT_Mode1']) <= ranges['ARG3'][1] and ranges['ARG4'][0] <= float(dataset.loc[h, 'ALT_Mode2']) <= ranges['ARG4'][1] and ranges['ARG5'][0] <= float(dataset.loc[h, 'ALT_Mode3']) <= ranges['ARG5'][1] and ranges['ARG6'][0] <= float(dataset.loc[h, 'TurnK1']) <= ranges['ARG6'][1] and ranges['ARG7'][0] <= float(dataset.loc[h, 'TurnK2']) <= ranges['ARG7'][1] and ranges['ARG8'][0] <= float(dataset.loc[h, 'TurnK3']) <= ranges['ARG8'][1] and ranges['ARG9'][0] <= float(dataset.loc[h, 'Pwheel1']) <= ranges['ARG9'][1] and ranges['ARG10'][0] <= float(dataset.loc[h, 'Pwheel2']) <= ranges['ARG10'][1] and ranges['ARG11'][0] <= float(dataset.loc[h, 'Pwheel3']) <= ranges['ARG11'][1]:
                if res.loc[h, 'Covered'+run][0] != 'No': # if this test input is already covered by another rule

                    continue

                else:

                    res.at[h, 'Covered'+run] = ('1', rule)

        elif model == 'R121':
           if ranges['ARG0'][0] <= float(dataset.loc[h, 'ALT_Mode1']) <= ranges['ARG0'][1] and ranges['ARG1'][0] <= float(dataset.loc[h, 'ALT_Mode2']) <= ranges['ARG1'][1] and ranges['ARG2'][0] <= float(dataset.loc[h, 'TurnK1']) <= ranges['ARG2'][1] and ranges['ARG3'][0] <= float(dataset.loc[h, 'TurnK2']) <= ranges['ARG3'][1] and ranges['ARG4'][0] <= float(dataset.loc[h, 'Pwheel1']) <= ranges['ARG4'][1] and ranges['ARG5'][0] <= float(dataset.loc[h, 'Pwheel2']) <= ranges['ARG5'][1] and ranges['ARG6'][0] <= float(dataset.loc[h, 'Throttle1']) <= ranges['ARG6'][1] and ranges['ARG7'][0] <= float(dataset.loc[h, 'Throttle2']) <= ranges['ARG7'][1]:

                if res.loc[h, 'Covered'+run][0] != 'No': # if this test input is already covered by another rule

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
        # if self.degree != other.degree:
        #     return self.degree > other.degree
        # if self.weight != other.weight:
        #     return self.weight > other.weight
        # return self.part == 'A' and other.part == 'B' #part A is pass, part B is fail

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

    # print('vertices ', [v.id for v in vertices])

    # print('****************************')

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

            # vertices = []

            # print('the current vertices before pop is ', [vv.id for vv in vertices])
            # heapq.heappop(vertices)
            # print('the vertices after pop is ', [vv.id for vv in vertices])

            graph[vertex.id].remove(neighbor)

        graph.pop(vertex.id)

        for v in graph: #reconstruct the heap
          part = 'A' if v in part_A else 'B'
          heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))
          vertices.sort()



                # print('print new heap ',[v.id for v in vertices])





        if all(not neighbors for neighbors in graph.values()):
            break



    return sorted(removed_vertices), sorted(removed_vertices_withpassfail, key = lambda v: v.id)

def CreateFormula(rule):

  # print('this is rule', rule)
  # print(type(rule))

  rule = ast.literal_eval(rule)

  # print(rule)
  # print(type(rule))

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


  # print(f)

  finalformula = f[0]

  for ff in f[1:]:

    finalformula = And(finalformula, ff)


  return finalformula

def remove_common_elements(list1, list2):
    # Convert the lists to sets to find common elements
    set1 = set(list1)
    set2 = set(list2)
    common_elements = set1 & set2

    # Remove common elements from both lists
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


  ####I have to do this because i removed alt mode for GP but it is there for DT/DR
  for i in range(len(fail_assertions)):
     
     fail_assertions[i] = fail_assertions[i].replace("ARG5", "ARG7")
     fail_assertions[i] = fail_assertions[i].replace("ARG4", "ARG6")
     fail_assertions[i] = fail_assertions[i].replace("ARG3", "ARG5")
     fail_assertions[i] = fail_assertions[i].replace("ARG2", "ARG4")
     fail_assertions[i] = fail_assertions[i].replace("ARG1", "ARG3")
     fail_assertions[i] = fail_assertions[i].replace("ARG0", "ARG2")


  for i in range(len(pass_assertions)):
     
     pass_assertions[i] = pass_assertions[i].replace("ARG5", "ARG7")
     pass_assertions[i] = pass_assertions[i].replace("ARG4", "ARG6")
     pass_assertions[i] = pass_assertions[i].replace("ARG3", "ARG5")
     pass_assertions[i] = pass_assertions[i].replace("ARG2", "ARG4")
     pass_assertions[i] = pass_assertions[i].replace("ARG1", "ARG3")
     pass_assertions[i] = pass_assertions[i].replace("ARG0", "ARG2")

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
# thetas = [0.5]
runs = ['Run'+str(j) for j in range(1, 21)]
# runs = ['Run'+str(j) for j in range(1, 2)]

for theta in thetas:

  for m, model in enumerate(['R121']):

    GPdata = pd.read_excel('C:\\Users\\Mehrdad\\Documents\\rabbitrun\\meetings\\Paper 3 - GenTC\\autopilot\\AP121 after adding the condition in code\\GP\\GPruleswithProb.xlsx')
    GPdata = GPdata[m: m+126]
    GPdata = GPdata.reset_index(drop=True)
        
    if model == 'R121':
        dtdata = pd.read_excel('C:/Users/Mehrdad/Documents/rabbitRun/meetings/Paper 3 - GenTC/autopilot/baseline/DT-R12_1-simplified.xlsx')
        drdata = pd.read_excel('C:/Users/Mehrdad/Documents/rabbitRun/meetings/Paper 3 - GenTC/autopilot/baseline/DR-R12_1-simplified.xlsx')

        testset = pd.read_excel('C:/Users/Mehrdad/Documents/rabbitRun/meetings/Paper 3 - GenTC/autopilot/testset/AP_R12_1-testset.xlsx')

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


      inconsistencies = defaultdict(list)  # dictionary of inconsistencies (the graph)

      # print('fail_assertions', fail_assertions)

      while i < len(pass_assertions):

          A_1 = pass_assertions[i]

          A = CreateFormula(A_1)

          j = 0

          while j < len(fail_assertions):

              # print('i, j', i, j)
              s = Solver()
              B_1 = fail_assertions[j]

              # s.push()  # Save the current state of the solver
              B = CreateFormula(B_1)

              s.add(A, B)
              # print(s)
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

      # print(weights)




      ######################
      removed_vertices, removed_vertices_withpassfail = remove_vertices(inconsistencies, pass_assertions, fail_assertions, weights)


      # print('len of pass assertion before removing ', len(pass_assertions))
      # print('len of fail assertion before removing ', len(fail_assertions))


      for item in removed_vertices_withpassfail:
        if item.part == 'A': #from pass
          pass_assertions.remove(item.id)
        else:
          fail_assertions.remove(item.id)

      # print(pass_assertions)
      # print(fail_assertions)

      # print('len of pass assertion after removing ', len(pass_assertions))
      # print('len of fail assertion after removing ', len(fail_assertions))


      ########################### covered points ##############################

      res = CalculatePerformance(fail_assertions, pass_assertions, testset, model, res, run)

      # print('done')

    import os 

    file_exists = os.path.isfile('Ensemble'+'-coveredpoints-'+model+'-theta'+str(theta)+'-testset.xlsx')

    with pd.ExcelWriter('Ensemble'+'-coveredpoints-'+model+'-theta'+str(theta)+'-testset.xlsx', engine = 'openpyxl', mode = 'a' if file_exists else 'w') as writer:
        res.to_excel(writer, sheet_name = 'dataset', index = False)


      



