from collections import defaultdict
from z3 import *
import ast
import copy
import random
import pandas as pd
import re
import heapq

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

            graph[neighbor].remove(vertex.id)
            if neighbor not in removed_vertices:
                degrees[neighbor] -= 1
                vertices = []
                for v in graph: #reconstruct the heap
                  part = 'A' if v in part_A else 'B'
                  heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))
                  vertices.sort()


                heapq.heappop(vertices)

            graph[vertex.id].remove(neighbor)

        graph.pop(vertex.id)

        if all(not neighbors for neighbors in graph.values()):
            break



    return sorted(removed_vertices), sorted(removed_vertices_withpassfail, key = lambda v: v.id)

def ExtractVars(rulee):

  pattern = r'ARG\d+'

  return re.findall(pattern, rulee)


def ExtractValue(rulee):

  pattern = r'\d+\.\d+'

  return re.findall(pattern, rulee)


def CreateFormulaNTSS(vars, floatt, rulee):

  if len(vars) == 1:
    if rulee.find('greater') != -1:  

      var1 = Int(vars[0])

      formula = And(var1 > int(float(floatt[0])))

    elif rulee.find('less') != -1:
      var1 = Int(vars[0])

      formula = And(var1 < int(float(floatt[0])))


  else:

    variables = [Int(x) for x in vars]

    sum_all = sum(variables)

    if rulee.find('greater') != -1:

      formula = And(sum_all > int(float(floatt[0])))

    else:

      formula = And(sum_all < int(float(floatt[0])))


  return formula

def remove_common_elements(list1, list2):

    set1 = set(list1)
    set2 = set(list2)
    common_elements = set1 & set2

    list1 = [item for item in list1 if item not in common_elements]
    list2 = [item for item in list2 if item not in common_elements]

    return list1, list2


results = []

for lll in range(1, 10):

  res = pd.DataFrame(columns = ['Run1', 'Run1Prob', 'Run2', 'Run2Prob', 'Run3', 'Run3Prob', 'Run4', 'Run4Prob', 'Run5', 'Run5Prob', 'Run6', 'Run6Prob', 'Run7', 'Run7Prob', 'Run8', 'Run8Prob', 'Run9', 'Run9Prob', 'Run10', 'Run10Prob', 'Run11', 'Run11Prob', 'Run12', 'Run12Prob', 'Run13', 'Run13Prob', 'Run14', 'Run14Prob', 'Run15', 'Run15Prob', 'Run16', 'Run16Prob', 'Run17', 'Run17Prob', 'Run18', 'Run18Prob', 'Run19', 'Run19Prob', 'Run20', 'Run20Prob'])

  fail_assertions1 = pd.read_excel('...\\path_to_file\\pure fail class rules - GP2.xlsx', sheet_name='dataset'+str(lll))
  pass_assertions1 = pd.read_excel('...\\path_to_file\\pure pass class rules - GP2.xlsx', sheet_name='dataset' + str(lll))

  cols = ['Run'+str(i) for i in range(1, 21)]

  for kk in range(3):

    indexx = res.shape[0]

    for col in cols:

      fail_assertions = list(set(fail_assertions1.loc[360 + kk*20:379 + kk*20, col].dropna().values.tolist()))

      pass_assertions = list(set(pass_assertions1.loc[360 + kk*20:379 + kk*20, col].dropna().values.tolist()))

      i = 0
      j = 0

      s = Solver()


      inconsistencies = defaultdict(list) 

      while i < len(pass_assertions):

          A_1 = pass_assertions[i]

          vars = ExtractVars(A_1)
          floatt = ExtractValue(A_1)
          A = CreateFormulaNTSS(vars, floatt, A_1)

          j = 0

          while j < len(fail_assertions):

              s = Solver()
              B_1 = fail_assertions[j]

              vars = ExtractVars(B_1)
              floatt = ExtractValue(B_1)
              B = CreateFormulaNTSS(vars, floatt, B_1)

              s.add(A, B)
  
              if s.check() == sat:

                  print(f"Inconsistent pair found: {A} and {B}")

                  inconsistencies[A_1].append(B_1)

                  inconsistencies[B_1].append(A_1)

              else:
                  print(f"Consistent pair found: {A} and {B}")

              j += 1

          i += 1


      weights = {}

      for i in range(len(pass_assertions)):


        rule = pass_assertions[i]

        vars = ExtractVars(rule)


        weights[rule] = 1/len(vars)

      for i in range(len(fail_assertions)):

        rule = fail_assertions[i]

        vars = ExtractVars(rule)

        weights[rule] = 1/len(vars)

      ######################
      removed_vertices, removed_vertices_withpassfail = remove_vertices(inconsistencies, pass_assertions, fail_assertions, weights)


      for item in removed_vertices_withpassfail:
        if item.part == 'A': #from pass
          pass_assertions.remove(item.id)
        else:
          fail_assertions.remove(item.id)

      for hh in range(len(fail_assertions)):

        res.loc[hh + indexx, col] = fail_assertions[hh]

      res.loc[len(fail_assertions) + indexx, col] = '[]'

      for hh in range(len(pass_assertions)):

        res.loc[len(fail_assertions) + 1 + hh + indexx, col] = pass_assertions[hh]

      for gg in range(30 - (len(fail_assertions) + 1 + len(pass_assertions))):
         
         res.loc[len(fail_assertions) + len(pass_assertions) + 1 + gg + indexx, col] = '###'
      


  results.append(res)

  import os

  file_exists = os.path.isfile('finalresultsntss.xlsx')

  if file_exists:
    with pd.ExcelWriter('finalresultsntss.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
      for i, df in enumerate(results):
        df.to_excel(writer, sheet_name=f'dataset{i+1}', index=False)

  else:
    with pd.ExcelWriter('finalresultsntss.xlsx', engine='openpyxl', mode = 'w')  as writer:
      for i, df in enumerate(results):
        df.to_excel(writer, sheet_name=f'dataset{i+1}', index=False)
