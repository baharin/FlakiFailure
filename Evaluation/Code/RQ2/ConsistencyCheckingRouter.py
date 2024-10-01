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
        return self.part == 'A' and other.part == 'B'  # part A is pass, part B is fail

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

        while len(list(graph[vertex.id])) > 0:  # iterate over neighbors of vertex
            neighbor = list(graph[vertex.id])[0]
            graph[neighbor].remove(vertex.id)
            if neighbor not in removed_vertices:
                degrees[neighbor] -= 1
                vertices = []
                for v in graph:  # reconstruct the heap
                    part = 'A' if v in part_A else 'B'
                    heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))
                    vertices.sort()

                heapq.heappop(vertices)

            graph[vertex.id].remove(neighbor)

        graph.pop(vertex.id)

        if all(not neighbors for neighbors in graph.values()):
            break

    return sorted(removed_vertices), sorted(removed_vertices_withpassfail, key=lambda v: v.id)

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

def process_assertions(fail_assertions, pass_assertions):
    inconsistencies = defaultdict(list)

    # Solver for Z3
    s = Solver()

    for A_1 in pass_assertions:
        vars = ExtractVars(A_1)
        floatt = ExtractValue(A_1)
        A = CreateFormulaNTSS(vars, floatt, A_1)

        for B_1 in fail_assertions:
            s = Solver()  # Reset solver for each pair
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

    weights = {}
    for rule in pass_assertions + fail_assertions:
        vars = ExtractVars(rule)
        weights[rule] = 1 / len(vars)

    removed_vertices, removed_vertices_withpassfail = remove_vertices(inconsistencies, pass_assertions, fail_assertions, weights)

    for item in removed_vertices_withpassfail:
        if item.part == 'A':  # from pass
            pass_assertions.remove(item.id)
        else:
            fail_assertions.remove(item.id)

    return fail_assertions, pass_assertions
