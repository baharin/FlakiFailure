from collections import defaultdict
# !pip install z3-solver
from z3 import *
import ast
import copy
import random
import pandas as pd
import re
import heapq

import pandas as pd
import ast
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

        try:
          if ast.literal_eval(v) in part_A:
            part = 'A'

          else:
            part = 'B'

        except:

          if v in part_A:
            part = 'A'
            print('i am part A GPPPPPPPP')
          else:
            part = 'B'
            print('i am part B GPPPPPPPPP')
        heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))
        vertices.sort()
        # print([v.id for v in vertices])

    removed_vertices = set()

    removed_vertices_withpassfail = set()


    while vertices:
        vertex = heapq.heappop(vertices)


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

          try:
            if ast.literal_eval(v) in part_A:
              part = 'A'
              print('i am part A')
            else:
              part = 'B'
              print('i am part B')

          except:

            if v in part_A:
              part = 'A'

            else:
              part = 'B'


          heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))
          vertices.sort()



                # print('print new heap ',[v.id for v in vertices])





        if all(not neighbors for neighbors in graph.values()):
            break



    return sorted(removed_vertices), sorted(removed_vertices_withpassfail, key = lambda v: v.id)

def CreateFormula(rule):

  # print('this is rule', rule)
  # print(type(rule))

  print(rule, type(rule))

  rule = ast.literal_eval(rule)


  numberofpredicates = len(rule)

  f = [ 0 for i in range(len(rule))]

  for i, predicate in enumerate(rule):

    var1 = Int(predicate[1])

    if predicate[1] in encodedweathers:

      var1 = Int('ARG0')

      if predicate[0] == 'equal_to':

        if int(predicate[2]) == 0:

          f[i] = And( var1 != encodedweathers.index(predicate[1]))

        else:

          f[i] = And( var1 == encodedweathers.index(predicate[1]))

    elif predicate[0] == 'greater_than_func':

        f[i] = And(var1 > int(predicate[2]))

    elif predicate[0] == 'less_than_func':

        f[i] = And(var1 < int(predicate[2]))

    elif predicate[0] == 'equal_to':

        f[i] = And(var1 == int(predicate[2]))


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

def PreprocessDTDR(r):

  
  for i in range(len(r)):

    r_list = list(r[i])

    r_list[1] = r_list[1].replace('TIN ','ARG')
    r_list[1] = r_list[1].replace(' Req-BW','')
    r_list[1] = r_list[1].replace('TIN5+TIN6+TIN7', 'ARG5+ARG6+ARG7')

    r[i] = tuple(r_list)

  return r

def GetFailAndPassAssertions(assertions, theta):

  cols = ['Run'+str(i) for i in range(1, 21)]

  asserts = []

  probs = []

  for col in cols:

    Failassertions = []
    Passassertions = []

    Failassertionsprobs = []
    Passassertionsprobs = []

    i = 0
    while i < len(assertions.index) and assertions.loc[i, col] != '[]' and type(assertions.loc[i, col]) != float:

      if assertions.loc[i, col+'Prob'] >= theta:
            r = PreprocessDTDR(ast.literal_eval(assertions.loc[i, col]))
      

            Failassertions.append(r)

      i = i + 1

    i = i + 1
    while i < len(assertions.index) and assertions.loc[i, col] != '[]' and type(assertions.loc[i, col]) != float:

      if assertions.loc[i, col+'Prob'] >= theta:

          r = PreprocessDTDR(ast.literal_eval(assertions.loc[i, col]))


          Passassertions.append(r)

      i = i + 1

    asserts.append([Failassertions, Passassertions])


  return asserts

def CreateFormulaNTSS(vars, floatt, rulee):

  if len(vars) == 1: #there is only one var
    if rulee.find('greater') != -1:  #the formula is like var > value

      var1 = Int(vars[0])

      formula = And(var1 > int(float(floatt[0])))

    elif rulee.find('less') != -1:
      var1 = Int(vars[0])

      formula = And(var1 < int(float(floatt[0])))


  else: # we have sum of multiple vars

    variables = [Int(x) for x in vars]

    # print('variables ', variables)

    sum_all = sum(variables)

    # print('sum_all ', sum_all)

    if rulee.find('greater') != -1:

      formula = And(sum_all > int(float(floatt[0])))

    else:

      formula = And(sum_all < int(float(floatt[0])))


  return formula

def ExtractVars(rulee):

  pattern = r'ARG\d+'

  return re.findall(pattern, rulee)


def ExtractValue(rulee):

  pattern = r'\d+\.\d+'

  return re.findall(pattern, rulee)

def ExtractVarsDTDR(rulee):

  vs = []

  for i in range(len(rulee)):

    if rulee[i][1].find('+') != -1:

      vs.append('ARG5')
      vs.append('ARG6')
      vs.append('ARG7')

    else:
      vs.append(rulee[i][1])

  return vs


def ExtractValueDTDR(rulee):

  # pattern = r'\d+'

  floatss = []

  for i in range(len(rulee)):

    floatss.append(rulee[i][2])

  return floatss

for theta in [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]:
    for kk in range(0, 10):
    
      gpfail = pd.read_excel('..\\pure fail class rules - GP2.xlsx', sheet_name='dataset'+str(kk))[360:420].reset_index(drop=True)
    
      gppass = pd.read_excel('..\\pure pass class rules - GP2.xlsx', sheet_name='dataset'+str(kk))[360:420].reset_index(drop=True)
    
      dtind = pd.read_excel('..\\DT and DR Assertions.xlsx', sheet_name='dataset'+str(kk))[120:139].reset_index(drop=True)
    
      dtsum = pd.read_excel('..\\DT and DR Assertions.xlsx', sheet_name='dataset'+str(kk))[140:159].reset_index(drop=True)
    
      drind = pd.read_excel('..\\DT and DR Assertions.xlsx', sheet_name='dataset'+str(kk))[280:299].reset_index(drop=True)
    
      drsum = pd.read_excel('..\\DT and DR Assertions.xlsx', sheet_name='dataset'+str(kk))[300:319].reset_index(drop=True)
    
      cols = ['Run'+str(i) for i in range(1, 21)]
    
      gpasserts = []
    
      for col in cols:
    
        Failassertions = []
        Passassertions = []
    
        i = 0
        while i < len(gpfail.index) and gpfail.loc[i, col] != '[]' and type(gpfail.loc[i, col]) != float:

          if  gpfail.loc[i, col+'Prob'] >= theta:
              Failassertions.append(gpfail.loc[i, col])
    
          i = i + 1
    
        i = 0
        while  i < len(gppass.index) and gppass.loc[i, col] != '[]' and type(gppass.loc[i, col]) != float:

          if gppass.loc[i, col+'Prob'] >= theta:  
              Passassertions.append(gppass.loc[i, col])
    
          i = i + 1
    
        gpasserts.append([Failassertions, Passassertions])
    
      dtassertind = GetFailAndPassAssertions(dtind, theta)
      dtassertsum = GetFailAndPassAssertions(dtsum, theta)
      drassertind = GetFailAndPassAssertions(drind, theta)
      drassertsum = GetFailAndPassAssertions(drsum, theta)
    
    
      ensemble = dtassertind
    
      for i in range(len(ensemble)): #combine everything
    
        for j in range(len(ensemble[i])):
    
          ensemble[i][j].extend(dtassertsum[i][j])
          ensemble[i][j].extend(drassertind[i][j])
          ensemble[i][j].extend(drassertsum[i][j])
          ensemble[i][j].extend(gpasserts[i][j])
    
    
    
    
      res = pd.DataFrame(columns = ['Run1', 'Run1Prob', 'Run2', 'Run2Prob', 'Run3', 'Run3Prob', 'Run4', 'Run4Prob', 'Run5', 'Run5Prob', 'Run6', 'Run6Prob', 'Run7', 'Run7Prob', 'Run8', 'Run8Prob', 'Run9', 'Run9Prob', 'Run10', 'Run10Prob', 'Run11', 'Run11Prob', 'Run12', 'Run12Prob', 'Run13', 'Run13Prob', 'Run14', 'Run14Prob', 'Run15', 'Run15Prob', 'Run16', 'Run16Prob', 'Run17', 'Run17Prob', 'Run18', 'Run18Prob', 'Run19', 'Run19Prob', 'Run20', 'Run20Prob'])
    
    
      cols = ['Run'+str(i) for i in range(1, 21)]
    
      for ind, col in enumerate(cols):
    
    
        fail_assertions = ensemble[ind][0]
    
        pass_assertions = ensemble[ind][1]
    
        
        i = 0
        j = 0
    
        s = Solver()
    
        inconsistencies = defaultdict(list)  # dictionary of inconsistencies (the graph)
    
    
        while i < len(pass_assertions):
    
            A_1 = str(pass_assertions[i])
    
            if type(pass_assertions[i]) == str: #NTSS
    
              
              vars = ExtractVars(A_1)
              floatt = ExtractValue(A_1)
              A = CreateFormulaNTSS(vars, floatt, A_1)
    
    
            else: #DT / DR
    
              vars = ExtractVarsDTDR(pass_assertions[i])
              floatt = ExtractValueDTDR(pass_assertions[i])
              A = CreateFormulaNTSS(vars, floatt, A_1)
    
            # A = CreateFormula(A_1)
    
            j = 0
    
            while j < len(fail_assertions):
    
                s = Solver()
                B_1 = str(fail_assertions[j])
    
                if type(fail_assertions[j]) == str: #GP
    
                  
                  vars = ExtractVars(B_1)
                  floatt = ExtractValue(B_1)
                  B = CreateFormulaNTSS(vars, floatt, B_1)
    
                else: #DT / DR
    
                  vars = ExtractVarsDTDR(fail_assertions[j])
                  floatt = ExtractValueDTDR(fail_assertions[j])
                  B = CreateFormulaNTSS(vars, floatt, B_1)
    
                s.add(A, B)
    
                if s.check() == sat:
                    
                    inconsistencies[A_1].append(B_1)
            
                    inconsistencies[B_1].append(A_1)
    
                else:
                    print(f"Consistent pair found: {A} and {B}")
    
                j += 1
    
            i += 1
    
    
        weights = {}
    
        for i in range(len(pass_assertions)):
    
          rule = pass_assertions[i]
    
          if type(pass_assertions[i]) == str: #NTSS
    
            weights[pass_assertions[i]] = 1/len(ExtractVars(rule))
    
          else: #DT / DR
    
            weights[str(pass_assertions[i])] = 1/len(ExtractVarsDTDR(rule))
    
        for i in range(len(fail_assertions)):
    
          rule = fail_assertions[i]
    
          if type(fail_assertions[i]) == str: #NTSS
    
            weights[fail_assertions[i]] = 1/len(ExtractVars(rule))
    
            # print(fail_assertions[i], type(fail_assertions[i]))
    
          else: #DT / DR
    
            weights[str(fail_assertions[i])] = 1/len(ExtractVarsDTDR(rule))
    
    
        ######################
        
        removed_vertices, removed_vertices_withpassfail = remove_vertices(inconsistencies, pass_assertions, fail_assertions, weights)
        
        for item in removed_vertices_withpassfail:
          
          if item.part == 'A': #from pass
            try:
              pass_assertions.remove(ast.literal_eval(item.id))
              
            except:
              pass_assertions.remove(item.id)
    
          else:
            try:
              fail_assertions.remove(ast.literal_eval(item.id))
              
            except:
    
              fail_assertions.remove(item.id)
    
        for hh in range(len(fail_assertions)):
    
          res.loc[hh, col] = fail_assertions[hh]
    
        res.loc[len(fail_assertions), col] = '[]'
    
        for hh in range(len(pass_assertions)):
    
          res.loc[len(fail_assertions) + 1 + hh, col] = pass_assertions[hh]
    
      file_exists = os.path.isfile('ensembleNTSS.xlsx')
    
      if file_exists:
          with pd.ExcelWriter('ensembleRouter'+theta+'.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
              res.to_excel(writer, sheet_name='dataset'+str(kk), index=False)
    
      else:
          with pd.ExcelWriter('ensembleRouter'+theta+'.xlsx', engine='openpyxl', mode = 'w')  as writer:
              res.to_excel(writer, sheet_name='dataset'+str(kk), index=False)  

