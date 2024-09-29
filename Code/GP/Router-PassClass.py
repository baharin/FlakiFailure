import operator
import random
import math
import copy
import numpy as np
import pandas as pd
from deap import algorithms, base, creator, gp, tools


def less_than_func(x, y):

    if x < y:
        return 'true'
    else:
        return 'false'


def greater_than_func(x, y):

    if x > y:
        return 'true'
    else:
        return 'false'


def evaluate(individual):
    
  func = toolbox.compile(expr=individual)

  results = []

  for i in range(len(testpopulation.index)):

      x = testpopulation.loc[i:i, ['TIN 0 Req-BW', 'TIN 1 Req-BW', 'TIN 2 Req-BW', 'TIN 3 Req-BW', 'TIN 4 Req-BW', 'TIN 5 Req-BW', 'TIN 6 Req-BW', 'TIN 7 Req-BW']].values

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

      res = (countpasses / allpassesofdataset) - (countfails / (1 + allfailsofdataset))
  
  elif fitnessfunc == 'Tarantula':
    
      res = (countpasses /allpassesofdataset )/((countfails /allfailsofdataset ) + (countpasses /allpassesofdataset ) )
    
  elif fitnessfunc == 'Ochiai':
    
      res = countpasses / (math.sqrt(allpassesofdataset * (countfails + countpasses)))

  return res,



def pass_through(x):
    return x


def PreprocessNTSS(data, threshold):
    for i in range(len(data.index)):

        if data.loc[i, 'Fitness'] < threshold:
            data.loc[i, 'Label'] = 0
        else:
            data.loc[i, 'Label'] = 1

    return data

def PreprocessWithoutRep2(data, rep):
    newdata = pd.DataFrame(columns=['Label', 'Fitness', 'TIN 0 Req-BW', 'TIN 1 Req-BW', 'TIN 2 Req-BW', 'TIN 3 Req-BW'
        , 'TIN 4 Req-BW', 'TIN 5 Req-BW', 'TIN 6 Req-BW', 'TIN 7 Req-BW'])

    j = 0
    k = 0
    counterr = 0

    while j < len(data.index):
        newdata.loc[k, 'TIN 0 Req-BW'] = data.loc[j, 'TIN 0 Req-BW']

        newdata.loc[k, 'TIN 1 Req-BW'] = data.loc[j, 'TIN 1 Req-BW']

        newdata.loc[k, 'TIN 2 Req-BW'] = data.loc[j, 'TIN 2 Req-BW']
        newdata.loc[k, 'TIN 3 Req-BW'] = data.loc[j, 'TIN 3 Req-BW']
        newdata.loc[k, 'TIN 4 Req-BW'] = data.loc[j, 'TIN 4 Req-BW']
        newdata.loc[k, 'TIN 5 Req-BW'] = data.loc[j, 'TIN 5 Req-BW']
        newdata.loc[k, 'TIN 6 Req-BW'] = data.loc[j, 'TIN 6 Req-BW']
        newdata.loc[k, 'TIN 7 Req-BW'] = data.loc[j, 'TIN 7 Req-BW']

        newdata.loc[k, 'Fitness'] = data.loc[j, 'Fitness']

        newdata.loc[k, 'Label'] = data.loc[j, 'Label']

        k = k + 1
        j = j + 1

    return newdata

def HandleDuplicateIndividuals(pops):
    for ind in pops:

        if pops.count(ind) >= 2:  # duplications

            j = 1  # keeping the first occurance
            counts = pops.count(ind)

            indexxx = pops.index(ind)
            copyind = copy.deepcopy(ind)
            while j < counts:

                newind_fit = (False,)
                while newind_fit[0] == False:

                    ind = copyind

                    newind = toolbox.mutate(ind)[0]

                    newind_fit = toolbox.evaluate(newind)

                    newind.fitness.values = newind_fit

                pops[indexxx] = newind

                j = j + 1

    return pops


fitnessfunc = input('Select Fitness Function from Tarantula, Naish, Ochiai,...')



results = pd.DataFrame(columns=['Run', 'TestDataset', 'PopulationSize', 'NumberofGenerations',
                                'MaxTreeDepth', 'BestIndividualFormula', 'BestIndividualFitness', 'MaxofRandomNumber'])


pset = gp.PrimitiveSetTyped("MAIN", [int, int, int, int, int, int, int, int], str)
pset.addPrimitive(operator.add, [int, int], int)
pset.addPrimitive(less_than_func, [int, float], str)
pset.addPrimitive(greater_than_func, [int, float], str)
pset.addEphemeralConstant("rand", lambda: float(int((random.uniform(0, 400)))), float)
pset.addPrimitive(pass_through, [float], float)

bestfitnessovertime = pd.DataFrame(columns=['Run', 'Generation', 'BestFitness', 'BestInd'])

rep = 10
for k in range(1, 10):

    wholepopulation = pd.read_excel('Router'+str(k)+'.xlsx')
  
    wholepopulation = PreprocessNTSS(wholepopulation, 0.8)  

    wholepopulation = PreprocessWithoutRep2(wholepopulation, rep)

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



results.to_excel('GPresults_Router_passclass'+str(k)+'.xlsx')

bestfitnessovertime.to_excel('BestFitnessesOvertime_Router_passclass'+str(k)+'.xlsx')
