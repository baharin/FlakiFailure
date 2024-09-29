import copy
import operator
import random
import math
import numpy as np
import pandas as pd
from deap import algorithms, base, creator, gp, tools
from copy import deepcopy

import re


def extract_arguments(input_array):
    result = []

    input_array = input_array.replace('pass_throughfloat', '')
    input_array = input_array.replace('pass_throughstr', '')
    input_array = input_array.replace('pass_throughbool', '')
    input_array = input_array.replace('pass_throughtuple', '')
    input_array = input_array.replace('pass_through', '')
    input_array = input_array.replace('sub_and', '')

    

    pattern = r'(greater_than_func|less_than_func|equal_to)\(*?(ARG[0-7])\)*?, \(*?(-?\d+)\)*?\)'
    
    matches = re.findall(pattern, input_array)


    for match in matches:
        if match[0] == 'greater_than_func':
            result.append('greater')
        elif match[0] == 'less_than_func':
            result.append('less')
        elif match[0] == 'equal_to':
            result.append('equal')

        result.append(f'{match[1]}, {match[2]}')

    return result


def PreprocessWithoutRepetition(data, label): 

    if model == 'townbeamng':

        newdata = pd.DataFrame(
            columns=['Label', 'Weather', 'MaxSpeed', 'Traffic Amount'])
    else:

        newdata = pd.DataFrame(columns=['Label', 'Weather', 'Maxspeed', 'MAX_ANGLE'])

    j = 0
    k = 0
    counterr = 0

    while j < len(data.index):

        if model != 'townbeamng':

            newdata.loc[k, 'Maxspeed'] = data.loc[j, 'Maxspeed'] * 1.0

            newdata.loc[k, 'MAX_ANGLE'] = data.loc[j, 'MAX_ANGLE'] * 1.0

        

            if data.loc[j, 'TestOutcome'] == 'PASS':
                newdata.loc[k, 'Label'] = 1

            else:
                newdata.loc[k, 'Label'] = 0

        else:
            newdata.loc[k, 'MaxSpeed'] = data.loc[j, 'MaxSpeed'] * 1.0

            newdata.loc[k, 'Traffic Amount'] = data.loc[j, 'Traffic Amount'] * 1.0

            newdata.loc[k, 'Label'] = data.loc[j, label]

        if type(data.loc[j, 'Weather']) == str:

            if data.loc[j, 'Weather'] == 'cloudy_evening':

                newdata.loc[k, 'Weather'] = (0.0, '')

            elif data.loc[j, 'Weather'] == 'sunny_noon':

                newdata.loc[k, 'Weather'] = (1.0, '')

            elif data.loc[j, 'Weather'] == 'sunny_evening':

                newdata.loc[k, 'Weather'] = (2.0, '')

            elif data.loc[j, 'Weather'] == 'foggy_morning':

                newdata.loc[k, 'Weather'] = (3.0, '')

            elif data.loc[j, 'Weather'] == 'foggy_night':

                newdata.loc[k, 'Weather'] = (4.0, '')

            elif data.loc[j, 'Weather'] == 'sunny':

                newdata.loc[k, 'Weather'] = (5.0, '')

            elif data.loc[j, 'Weather'] == 'rainy':

                newdata.loc[k, 'Weather'] = (6.0, '')

        else:

            newdata.loc[k, 'Weather'] = (data.loc[j, 'Weather'] * 1.0, '')

        k = k + 1

        j = j + 1

    return newdata

def less_than_func(x, y):


    if x < y and isinstance(x, float):
        return 'true'
    else:
        return 'false'


def greater_than_func(x, y):

    if x > y and isinstance(x, float):
        return 'true'
    else:
        return 'false'

def equal_to(x, y):


    if x[0] == y and isinstance(x, tuple):
        return 'true'
    else:
        return 'false'



def CheckForValidRanges(operator, variable, value, model):
    variables = ['ARG0', 'ARG1', 'ARG2']

    if model == 'dave2':
        ranges = [(0, 6), (5, 10), (3, 20)]
    elif model == 'beamng':
        ranges = [(0, 6), (5, 100), (30, 90)] 

    elif model == 'townbeamng':

        ranges = [(0, 6), (20, 50), (0, 10)]    

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

def CheckforValidity(ind, model):

    arguments = extract_arguments(ind)

    validity = []

    for i in range(0, len(arguments) - 1, 2):
        operator = arguments[i]
        variable = arguments[i + 1][arguments[i + 1].find('ARG'): arguments[i + 1].find('ARG') + 4]
        value = float(arguments[i + 1][arguments[i + 1].find(', ') + 2:])

        validity.append(CheckForValidRanges(operator, variable, value, model))

    if len(validity) == 0:
        return False

    return all(validity)


def evaluate(individual):
    
    truepoints = []

    flag = CheckforValidity(str(individual), model)

    
    if flag == False: 
       
        return False,
    else:

        func = toolbox.compile(expr=individual)

        results = []

        for i in range(len(testpopulation.index)):

            if model == 'townbeamng':
                x =  testpopulation.loc[i:i, ['Weather', "MaxSpeed", 'Traffic Amount']].values

            else:

                x = testpopulation.loc[i:i, ["Weather", 'Maxspeed', 'MAX_ANGLE']].values

            

            result = func(*x[0])

           
            results.append(result)

        countfails = 0
        countpasses = 0
        res = 0

        for i in range(len(results)):

            
            if results[i] == 'true':
               
                if testpopulation.loc[i, 'Label'] == 0:
                    countfails = countfails + 1

                elif testpopulation.loc[i, 'Label'] == 1:
                    countpasses = countpasses + 1

                

        allpassesofdataset = 0
        for i in range(len(testpopulation.index)):
            
            if testpopulation.loc[i, 'Label'] == 1:
                allpassesofdataset = allpassesofdataset + 1

        allfailsofdataset = 0
        for i in range(len(testpopulation.index)):
            if testpopulation.loc[i, 'Label'] == 0:
                allfailsofdataset = allfailsofdataset + 1

        if fitnessfunc == 'Naish':

          res = (countfails / allfailsofdataset) - (countpasses/ (1 + allpassesofdataset))

        elif fitnessfunc == 'Tarantula':

          if len(truepoints) != 0 :
          
              res = (countfails /allfailsofdataset )/((countfails /allfailsofdataset ) + (countpasses /allpassesofdataset ) )
          else:
          
             res = -100000

        elif fitnessfunc == 'Ochiai':
          
          if len(truepoints) != 0:
          
              res = countfails / (math.sqrt(allfailsofdataset*(countfails + countpasses)))
          
          else:
              res = -100000

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

    if (ar1 == 'true' and ar2 == '' ) or (ar1 == 'true' and ar2 == 'true') or (ar1 == '' and ar2 == 'true'):

        return 'true'
    else:
        return 'false'

def HandleDuplicateIndividuals(pops):

    for ind in pops:

        if pops.count(ind) >= 2: #duplications

            j = 1 #keeping the first occurance
            counts = pops.count(ind)
            print('ind is ', ind)
            print('counts is ', counts)
            indexxx = pops.index(ind)
            copyind = copy.deepcopy(ind)
            while j < counts:

                newind_fit = (False,)
                while newind_fit[0] == False:
                    ind = copyind
                    listtt = [ind, ind, ind, ind]
                    newind = algorithms.varAnd(listtt, toolbox, cxpb=0.9, mutpb=0.8)[0]
                    newind_fit = toolbox.evaluate(newind)
                    newind.fitness.values = newind_fit
                pops[indexxx] = newind
              
                j = j + 1

    return pops


# Define the primitive set for genetic programming
pset = gp.PrimitiveSetTyped("MAIN", [tuple, float, float], str) #the first two floats are actually bools
pset.addPrimitive(sub_and, [str, str], str)
pset.addPrimitive(less_than_func, [float, int], str)
pset.addPrimitive(greater_than_func, [float, int], str)
pset.addPrimitive(equal_to, [tuple, int], str)
pset.addEphemeralConstant("rand", lambda: int((random.uniform(0, 100))), int)
pset.addEphemeralConstant("randbool", lambda : int(random.choice([0,1,2,3,4,5,6])), int)
pset.addPrimitive(pass_through, [int], int)
pset.addPrimitive(pass_throughfloat, [float], float)
pset.addPrimitive(pass_throughtuple, [tuple], tuple)
pset.addTerminal('', str)

a = input('Select case study from AP-SNG, Dave2, R1, R2, R3, R4...')

if a == 'AP-SNG':
  model = 'beamng'
  label = 'TestOutcome'
elif a == 'Dave2':
  model = 'dave2'
  label = 'TestOutcome'
elif a == 'R1' or a == 'R2' or a == 'R3' or a == 'R4':
  model = 'townbeamng'
  if a == 'R1':
    label = 'Label'
  elif a == 'R2':
    label = 'Label(Damage)'
  elif a == 'R3':
    label = 'Label(Ultra)'
  elif a == 'R4':
    label = 'Label(Distance)'

fitnessfunc = input('Select fitness function from Tarantula, Naish and Ochiai...')

for k in range(1, 10):

    bestfitnessovertime = pd.DataFrame(columns=['Run', 'Generation', 'BestFitness', 'BestInd'])

    results = pd.DataFrame(columns=['Run', 'TestDataset', 'PopulationSize', 'NumberofGenerations',
                                    'MaxTreeDepth', 'BestIndividualFormula', 'BestIndividualFitness',
                                    'BaselinePrecision'])

    if model == 'beamng':

      wholepopulation = pd.read_excel('...\\AP-SNG'+str(k)+'.xlsx')

    elif model == 'dave2':

      wholepopulation = pd.read_excel('...\\Dave2'+str(k)+'.xlsx')

    elif a == 'R1':

      wholepopulation = pd.read_excel('...\\AP-TWN - R1 - '+str(k)+'.xlsx')

    else:

      wholepopulation = pd.read_csv('...\\AP-TWN - R2 to R4 - '+str(k)+'.csv')


    wholepopulation = PreprocessWithoutRepetition(wholepopulation, label)

    
    max_depth = 5
    for h in range(20):

        best_individuals_overgenerations = []
        best_individuals_overgenerations_fitness = []

        best_individual = None
        
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=max_depth)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("compile", gp.compile, pset=pset)
        toolbox.register("evaluate", evaluate)
        toolbox.register("select", tools.selTournament, tournsize = 7 )

        toolbox.register("mate", gp.cxOnePoint)
        toolbox.register("expr_mut", gp.genGrow, min_=1, max_=max_depth)
        toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
        toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_depth))
        toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=max_depth))

        
        testpopulation = wholepopulation
        populationsize = 50
        # Create the initial population
        population = toolbox.population(n=populationsize*2) 
        
        fits = toolbox.map(toolbox.evaluate, population)

        for fit, ind in zip(fits, population):
            ind.fitness.values = fit
            
            if fit[0] == False:
                population = list(filter((ind).__ne__, population))
                

        if len(population) < populationsize:
            population = population + toolbox.population(n = populationsize - len(population))

        elif len(population) > populationsize:

            population = population[:populationsize]
           
        NGEN = 50 



        gen = 0
        cxpb = 0.7
        mutpb = 0.1 
        while gen < NGEN:
          
            offspring = algorithms.varAnd(population, toolbox, cxpb=cxpb, mutpb=mutpb) #generates a new population (called offspring) from the initial one (population) with the same size as population

            copyoffspring = offspring

            fits = toolbox.map(toolbox.evaluate, offspring)

            countt = 0
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
                
                if fit[0] == False:
                    
                    offspring = list(filter((ind).__ne__, offspring))

                countt = countt + 1


            random.shuffle(offspring)

            if len(offspring) >= 25: 
                offspring = offspring[:25]
                

            popandoffspring = population + offspring


            popandoffspring = HandleDuplicateIndividuals(popandoffspring)

            
            population = toolbox.select(popandoffspring, k=len(population), )

            N = 10

            top_best_individuals = tools.selBest(population, k = N)
            

            top_best_individuals_fitness = []

            for ll in range(N):
                top_best_individuals_fitness.append(top_best_individuals[ll].fitness.values[0])
                
            best_individuals_overgenerations.append(top_best_individuals)
            best_individuals_overgenerations_fitness.append(top_best_individuals_fitness)

            current_best_individual = tools.selBest(population, k=1)[0]
            
            current_best_fitness = current_best_individual.fitness.values[0]

            
            if current_best_fitness >= best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual

            bestfitnessovertime.loc[bestfitnessovertime.shape[0]] = [h, gen, best_fitness, best_individual]

            gen = gen + 1
    


        topbests = 20

        flattened_list_ind = [item for sublist in best_individuals_overgenerations for item in sublist]
        flattened_list_fit = [item for sublist in best_individuals_overgenerations_fitness for item in sublist]

        paired_list = list(zip(flattened_list_fit, flattened_list_ind))

        
        paired_list.sort(reverse=True, key=lambda x: x[0])

        
        top_n_items = [str(item[1]) for item in paired_list[:topbests]]
        top_n_items_fit = [item[0] for item in paired_list[:topbests]]

        


        results.loc[results.shape[0]] = [h, 'GP', populationsize, NGEN, max_depth, top_n_items, top_n_items_fit,
                                         baselineprecision]



results.to_excel('GPresults_'+a+'_'+str(k)+'.xlsx')

bestfitnessovertime.to_excel('BestFitnessesOvertime_'+a+'_'+str(k)+'.xlsx')
