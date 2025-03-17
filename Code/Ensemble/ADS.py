from collections import defaultdict
# !pip install z3-solver
from z3 import *
import ast
import copy
import random
import pandas as pd
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
        print(v, type(v))
        if ast.literal_eval(v) in part_A:
          part = 'A'

        else:
          part = 'B'

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
            # print('this is the neighbor: ', neighbor)
            graph[neighbor].remove(vertex.id)
            if neighbor not in removed_vertices:
                degrees[neighbor] -= 1

            graph[vertex.id].remove(neighbor)

        graph.pop(vertex.id)

        for v in graph: #reconstruct the heap
          part = 'A' if ast.literal_eval(v) in part_A else 'B'
          heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))
          vertices.sort()



        if all(not neighbors for neighbors in graph.values()):
            break



    return sorted(removed_vertices), sorted(removed_vertices_withpassfail, key = lambda v: v.id)

def CreateFormula(rule):

  rule = ast.literal_eval(rule)

  encodedweathers = ['CLEV', 'SUNO', 'SUEV', 'FOMO', 'FONI', 'SUNN', 'RAIN']

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
          Failassertions.append(ast.literal_eval(assertions.loc[i, col]))

      i = i + 1

    i = i + 1
    while i < len(assertions.index) and assertions.loc[i, col] != '[]' and type(assertions.loc[i, col]) != float:

      if assertions.loc[i, col+'Prob'] >= theta:  
          Passassertions.append(ast.literal_eval(assertions.loc[i, col]))

      i = i + 1

    asserts.append([Failassertions, Passassertions])


  return asserts


gpinds = [0, 60, 120, 180, 240, 300 ]
dtinds = [0, 20, 40, 80, 60,100 ]
drinds = [160, 180, 200, 240, 220, 260]

for theta in [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]:
    for kk in range(0, 10):
        res = pd.DataFrame(columns = ['Run1', 'Run1Prob', 'Run2', 'Run2Prob', 'Run3', 'Run3Prob', 'Run4', 'Run4Prob', 'Run5', 'Run5Prob', 'Run6', 'Run6Prob', 'Run7', 'Run7Prob', 'Run8', 'Run8Prob', 'Run9', 'Run9Prob', 'Run10', 'Run10Prob', 'Run11', 'Run11Prob', 'Run12', 'Run12Prob', 'Run13', 'Run13Prob', 'Run14', 'Run14Prob', 'Run15', 'Run15Prob', 'Run16', 'Run16Prob', 'Run17', 'Run17Prob', 'Run18', 'Run18Prob', 'Run19', 'Run19Prob', 'Run20', 'Run20Prob'])
    
        for jj in range(len(gpinds)):
    
            indexx = res.shape[0]
    
            gpfail = pd.read_excel('pure fail class asserts - GP2.xlsx', sheet_name='dataset'+str(kk))[gpinds[jj]:gpinds[jj] + 59].reset_index(drop=True)
    
            gppass = pd.read_excel('pure pass class asserts - GP2.xlsx', sheet_name='dataset'+str(kk))[gpinds[jj]:gpinds[jj] + 59].reset_index(drop=True)
    
            dt = pd.read_excel('DT and DR Assertions.xlsx', sheet_name='dataset'+str(kk))[dtinds[jj]:dtinds[jj] + 19].reset_index(drop=True)
    
            dr = pd.read_excel('DT and DR Assertions.xlsx', sheet_name='dataset'+str(kk))[drinds[jj]:drinds[jj] + 19].reset_index(drop=True)
    
            cols = ['Run'+str(i) for i in range(1, 21)]
    
            gpasserts = []
    
            for col in cols:
    
                Failassertions = []
                Passassertions = []
    
                i = 0
                while i < len(gpfail.index) and gpfail.loc[i, col] != '[]' and type(gpfail.loc[i, col]) != float:

                    if gpfail.loc[i, col+'Prob'] >= theta:
                        Failassertions.append(ast.literal_eval(gpfail.loc[i, col]))
    
                    i = i + 1
    
                i = 0
                while  i < len(gppass.index) and gppass.loc[i, col] != '[]' and type(gppass.loc[i, col]) != float:

                    if gppass.loc[i, col+'Prob'] >= theta:
                        Passassertions.append(ast.literal_eval(gppass.loc[i, col]))
    
                    i = i + 1
    
                gpasserts.append([Failassertions, Passassertions])
    
            dtassert = GetFailAndPassAssertions(dt, theta)
            drassert = GetFailAndPassAssertions(dr, theta)
    

            ensemble = dtassert
    
            for i in range(len(ensemble)): #combine everything
    
                for j in range(len(ensemble[i])):
    
                    ensemble[i][j].extend(drassert[i][j])
                    ensemble[i][j].extend(gpasserts[i][j])
    
    
  
    
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
    
                    A = CreateFormula(A_1)
    
                    j = 0
    
                    while j < len(fail_assertions):
    
    
                        s = Solver()
                        B_1 = str(fail_assertions[j])
    
         
                        B = CreateFormula(B_1)
    
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
    
                    weights[str(pass_assertions[i])] = 1/len(rule)
    
                for i in range(len(fail_assertions)):
    
                    rule = ast.literal_eval(str(fail_assertions[i]))
    
                    weights[str(fail_assertions[i])] = 1/len(rule)
    
    
                ######################
    
                removed_vertices, removed_vertices_withpassfail = remove_vertices(inconsistencies, pass_assertions, fail_assertions, weights)
                
                for item in removed_vertices_withpassfail:

                    if item.part == 'A': #from pass
                        pass_assertions.remove(ast.literal_eval(item.id))
                    else:
                        fail_assertions.remove(ast.literal_eval(item.id))
    
    
                for hh in range(len(fail_assertions)):
    
                    res.loc[hh + indexx, col] = fail_assertions[hh]
    
                res.loc[len(fail_assertions) + indexx, col] = '[]'
    
                for hh in range(len(pass_assertions)):
    
                    res.loc[len(fail_assertions) + 1 + hh + indexx, col] = pass_assertions[hh]
    
                for gg in range(30 - (len(fail_assertions) + 1 + len(pass_assertions))):
             
                    res.loc[len(fail_assertions) + len(pass_assertions) + 1 + gg + indexx, col] = '###'
    
    
            file_exists = os.path.isfile('ensembleADAS.xlsx')
    
            if file_exists:
                with pd.ExcelWriter('ensembleADAS'+str(theta)+'.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    res.to_excel(writer, sheet_name='dataset'+str(kk), index=False)
    
            else:
                with pd.ExcelWriter('ensembleADAS'+str(theta)+'.xlsx', engine='openpyxl', mode = 'w')  as writer:
                    res.to_excel(writer, sheet_name='dataset'+str(kk), index=False)  
    
