import operator
import random
import math
import numpy as np
import pandas as pd
from deap import algorithms, base, creator, gp, tools

import re


def extract_arguments(input_array):
    result = []
    input_array = input_array.replace('(pass_throughmyfloat2','')
    input_array = input_array.replace('(pass_throughmyfloat', '')
    input_array = input_array.replace('pass_throughfloat', '')
    input_array = input_array.replace('pass_throughstr', '')
    input_array = input_array.replace('pass_throughbool', '')
    input_array = input_array.replace('pass_throughtuple', '')
    input_array = input_array.replace('pass_through', '')
    input_array = input_array.replace('sub_and', '')

    pattern = r'(greater_than_func|greater_than_func2|less_than_func2|less_than_func|equal_to)\(*?(ARG[0-7])\)*?, \(*?(-?\d+\.?\d*|-?\.\d+)\)*?\)'


    matches = re.findall(pattern, input_array)

    for match in matches:
        if match[0] == 'greater_than_func' or match[0] == 'greater_than_func2':
            result.append('greater')
        elif match[0] == 'less_than_func' or match[0] == 'less_than_func2':
            result.append('less')
        elif match[0] == 'equal_to':
            result.append('equal')

        result.append(f'{match[1]}, {match[2]}')

    return result

def less_than_func2(x, y):

    if x < y and isinstance(x, myfloat2):
        return 'true'
    else:
        return 'false'


def greater_than_func2(x, y):

    if x > y and isinstance(x, myfloat2):
        return 'true'
    else:
        return 'false'

def less_than_func(x, y):

    if x < y and isinstance(x, myfloat):
        return 'true'
    else:
        return 'false'


def greater_than_func(x, y):

    if x > y and isinstance(x, myfloat):
        return 'true'
    else:
        return 'false'


def equal_to(x, y):
    # print('x in equal to is ', x)
    # print('type of x in equal to is', type(x))
    if x[0] == y and isinstance(x, tuple):
        return 'true'
    else:
        return 'false'


def CheckForValidRanges(operator, variable, value):
    variables = ['ARG0', 'ARG1', 'ARG2', 'ARG3', 'ARG4', 'ARG5', 'ARG6', 'ARG7']


    ranges = [(0, 1), (0, 1), (0, 45), (0, 45), (-30, 30), (-30, 30), (0, 1), (0, 1)] 


    indexx = variables.index(variable)

    if operator == 'greater':

        if value >= ranges[indexx][1]:
            return False
        else:
            return True

    elif operator == 'less':

        if value <= ranges[indexx][0]:
            return False
        else:
            return True

    elif operator == 'equal':

        if ranges[indexx][0] <= value <= ranges[indexx][1]:
            return True
        else:
            return False


def CheckforValidity(ind):
    arguments = extract_arguments(ind)

    validity = []

    for i in range(0, len(arguments) - 1, 2):
        operator = arguments[i]
        variable = arguments[i + 1][arguments[i + 1].find('ARG'): arguments[i + 1].find('ARG') + 4]
        value = float(arguments[i + 1][arguments[i + 1].find(', ') + 2:])

        validity.append(CheckForValidRanges(operator, variable, value))

    if len(validity) == 0:
        return False

    return all(validity)


# Define the fitness function
def evaluate(individual):

    truepoints = []

    flag = CheckforValidity(str(individual))

    if flag == False:  # the individual is not unique
        return False,
    else:

        func = toolbox.compile(expr=individual)

        results = []

        for i in range(len(testpopulation.index)):

            x = testpopulation.loc[i:i, ['ALT_Mode1', 'ALT_Mode2', 'TurnK1', 'TurnK2', 'Pwheel1', 'Pwheel2', 'Throttle1', 'Throttle2']].values

            # print('this is x[0] ', x[0])

            result = func(*x[0])

            # print(result)

            results.append(result)

        countfails = 0
        countpasses = 0
        res = 0

        for i in range(len(results)):

            # print('this is results[i] ', results[i])
            if results[i] == 'true':
                # print('this is label ', testpopulation.loc[i, 'Label'])
                if testpopulation.loc[i, 'Label'] == 0:
                    countfails = countfails + 1

                elif testpopulation.loc[i, 'Label'] == 1:
                    countpasses = countpasses + 1


                truepoints.append(float(testpopulation.loc[i, 'Label'])) #UN COMMENT FOR SETUPS OTHER THAN TOWN


        allpassesofdataset = 0
        for i in range(len(testpopulation.index)):
            if testpopulation.loc[i, 'Label'] == 1:
                allpassesofdataset = allpassesofdataset + 1

        allfailsofdataset = 0

        for i in range(len(testpopulation.index)):

            if testpopulation.loc[i, 'Label'] == 0:
                allfailsofdataset = allfailsofdataset + 1


        if fitness == 'naish':
  
            res = (countfails / allfailsofdataset) - (countpasses / (1 + allpassesofdataset))


        elif fitness == 'tarantula':

            if len(truepoints) !=0 :

               print(allpassesofdataset, allfailsofdataset)

               res = (countfails /allfailsofdataset )/((countfails /allfailsofdataset ) + (countpasses /allpassesofdataset ) )

            else:

               res = -100000

        elif fitness == 'ochiai':
            if len(truepoints) != 0:

                res = countfails / (math.sqrt(allfailsofdataset * (countfails + countpasses)))

            else:
                res = -1000


        return res,


def pass_through(x):
    return x


def pass_throughbool(x):
    return x


def pass_throughfloat(x):
    return x


def pass_throughstr(x):
    return x


def pass_throughtuple(x):
    return x


def whole_and(ar1, ar2):
    if ar1 == 'true' and ar2 == 'true':
        return True
    else:
        return False


def sub_and(ar1, ar2):
    
    if (ar1 == 'true' and ar2 == '') or (ar1 == 'true' and ar2 == 'true') or (ar1 == '' and ar2 == 'true'):

        return 'true'
    else:
        return 'false'


def Preprocess(data, cols):

    for col in cols:

        data[col] = data[col].apply(lambda x: (x, ''))

    return data

class myfloat:

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return myfloat(self.value + other.value)

    def __sub__(self, other):
        return myfloat(self.value - other.value)

    def __mul__(self, other):
        return myfloat(self.value * other.value)

class myfloat2:

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return myfloat(self.value + other.value)

    def __sub__(self, other):
        return myfloat(self.value - other.value)

    def __mul__(self, other):
        return myfloat(self.value * other.value)


def pass_throughmyfloat(x):
    return x
def pass_throughmyfloat2(x):
    return x


# Define the primitive set for genetic programming
pset = gp.PrimitiveSetTyped("MAIN", [tuple, tuple, myfloat2, myfloat2, myfloat2, myfloat2, myfloat, myfloat], str)  
pset.addPrimitive(sub_and, [str, str], str)
pset.addPrimitive(less_than_func2, [myfloat2, int], str)
pset.addPrimitive(greater_than_func2, [myfloat2, int], str)
pset.addPrimitive(less_than_func, [myfloat, float], str)
pset.addPrimitive(greater_than_func, [myfloat, float], str)
pset.addPrimitive(equal_to, [tuple, int], str)
pset.addEphemeralConstant("rand", lambda: int((random.uniform(-30, 30))), int)
pset.addEphemeralConstant("randbool", lambda: int(random.choice([0, 1])), int)
pset.addEphemeralConstant("randbool2", lambda: round(random.uniform(0, 1), 1), float)
pset.addPrimitive(pass_through, [int], int)
pset.addPrimitive(pass_throughmyfloat, [myfloat], myfloat)
pset.addPrimitive(pass_throughmyfloat2, [myfloat2], myfloat2)
pset.addPrimitive(pass_throughfloat, [float], float)
pset.addPrimitive(pass_throughtuple, [tuple], tuple)
pset.addTerminal('', str)

fitness = input('Select fitness function from Tarantula, Naish and Ochiai...')


bestfitnessovertime = pd.DataFrame(columns=['Run', 'Generation', 'BestFitness', 'BestInd'])

results = pd.DataFrame(columns=['Run', 'TestDataset', 'PopulationSize', 'NumberofGenerations',
                                'MaxTreeDepth', 'BestIndividualFormula', 'BestIndividualFitness'])


wholepopulation = pd.read_excel('...\\Aircraft - 0.xlsx') #aircraft system is not flaky.

wholepopulation = Preprocess(wholepopulation, ['ALT_Mode1', 'ALT_Mode2'])

for h in range(20):

    best_individuals_overgenerations = []
    best_individuals_overgenerations_fitness = []
    best_individual = None
    # Create the fitness and individual classes
    best_fitness = -10000
    creator.create("FitnessMin", base.Fitness, weights=(1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    # Initialize the toolbox
    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=14)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("compile", gp.compile, pset=pset)
    toolbox.register("evaluate", evaluate)
    toolbox.register("select", tools.selTournament, tournsize=7)

    max_depth = 5

    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genGrow, min_=1, max_=5)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_depth))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_depth))

    NGEN = 50

    testpopulation = wholepopulation
    populationsize = 50

    gen = 0
    cxpb = 0.7
    mutpb = 0.1  
    while gen < NGEN:
        try:
            print(h)
            print('Generation ', gen)
            # Create the initial population
            population = toolbox.population(
                n=populationsize * 2)  

            fits = toolbox.map(toolbox.evaluate, population)

            for fit, ind in zip(fits, population):
                ind.fitness.values = fit
                # print(fit)
                # print(countt)
                if fit[0] == False:
                    population = list(filter((ind).__ne__, population))
                    # population.remove(ind)

            print('now len of initial population is ', len(population))

            if len(population) < populationsize:
                population = population + toolbox.population(n=populationsize - len(population))

            elif len(population) > populationsize:

                population = population[:populationsize]

            N = 10

            top_best_individuals = tools.selBest(population, k = N)
            # print('this is top best ind list ', top_best_individuals)
            # print('[0]', tools.selBest(population, k = N)[0])
            # print('from list ', top_best_individuals[0])
            # print('str form ', str(top_best_individuals[0]))

            top_best_individuals_fitness = []

            for ll in range(N):
                top_best_individuals_fitness.append(top_best_individuals[ll].fitness.values[0])
                # print(top_best_individuals[ll].fitness)
                # print(top_best_individuals[ll].fitness.values[0])

            best_individuals_overgenerations.append(top_best_individuals)
            best_individuals_overgenerations_fitness.append(top_best_individuals_fitness)

            current_best_individual = tools.selBest(population, k=1)[0]
            current_best_fitness = current_best_individual.fitness.values[0]

            if fitnessmaxormin == 'min':
                if current_best_fitness <= best_fitness:
                    best_fitness = current_best_fitness
                    best_individual = current_best_individual
            else:
                if current_best_fitness >= best_fitness:
                    best_fitness = current_best_fitness
                    best_individual = current_best_individual

            bestfitnessovertime.loc[bestfitnessovertime.shape[0]] = [h, gen, best_fitness, best_individual]

            gen = gen + 1
        except:
            continue

    topbests = 20

    flattened_list_ind = [item for sublist in best_individuals_overgenerations for item in sublist]
    flattened_list_fit = [item for sublist in best_individuals_overgenerations_fitness for item in sublist]

    paired_list = list(zip(flattened_list_fit, flattened_list_ind))

    # Sort the paired list based on the sorting criteria
    paired_list.sort(reverse=True, key=lambda x: x[0])

    # Extract the top N items based on the sorted order
    top_n_items = [str(item[1]) for item in paired_list[:topbests]]
    top_n_items_fit = [item[0] for item in paired_list[:topbests]]


    results.loc[results.shape[0]] = [h, 'random', populationsize, NGEN, max_depth, top_n_items, top_n_items_fit]


results.to_excel('GPresults_failclass_aircraft_'+fitness+'.xlsx')

bestfitnessovertime.to_excel(
    'BestFitnessesOvertime_failclass_aircraft_'+fitness+'.xlsx')
