from collections import defaultdict
from z3 import *
import ast
import copy
import random
import pandas as pd
import heapq
import os

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
            graph[vertex.id].remove(neighbor)

        graph.pop(vertex.id)

        for v in graph:  # reconstruct the heap
            part = 'A' if v in part_A else 'B'
            heapq.heappush(vertices, Vertex(v, degrees[v], weights[v], part))

        if all(not neighbors for neighbors in graph.values()):
            break

    return sorted(removed_vertices), sorted(removed_vertices_withpassfail, key=lambda v: v.id)

def CreateFormula(rule):
    rule = ast.literal_eval(rule)
    f = [0 for _ in range(len(rule))]

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

def process_assertions(fail_assertions, pass_assertions):
    
    i = 0
    inconsistencies = defaultdict(list)  # dictionary of inconsistencies (the graph)

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
        weights[pass_assertions[i]] = 1 / len(rule)

    for i in range(len(fail_assertions)):
        rule = ast.literal_eval(fail_assertions[i])
        weights[fail_assertions[i]] = 1 / len(rule)

    removed_vertices, removed_vertices_withpassfail = remove_vertices(inconsistencies, pass_assertions, fail_assertions, weights)

    for item in removed_vertices_withpassfail:
        if item.part == 'A':  # from pass
            pass_assertions.remove(item.id)
        else:
            fail_assertions.remove(item.id)

    return fail_assertions, pass_assertions
