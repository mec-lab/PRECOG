import numpy as np
import copy
import operator
import pickle
import os
import time
import random


def tournament_selection(pop, popsize):
    while len(pop) > popsize:

        # Choose two different individuals from the population
        ind1 = np.random.randint(len(pop))
        ind2 = np.random.randint(len(pop))
        while ind1 == ind2:
            ind2 = np.random.randint(len(pop))

        if pop[ind1].fitness1 > pop[ind2].fitness1:

            # remove ind2 from population and shift following individuals up in list
            for i in range(ind2, len(pop) - 1):
                pop[i] = pop[i + 1]
            pop.pop()  # remove last element from list (because it was shifted up)

        else:

            # remove ind1 from population and shift following individuals up in list
            for i in range(ind1, len(pop) - 1):
                pop[i] = pop[i + 1]
            pop.pop()  # remove last element from list (because it was shifted up)

    assert len(pop) == popsize
    return pop


def survivor_selection(pop, popsize):
    # Tournament selection based on age and fitness

    # Check to see if the pareto front size is larger than the population size
    # and increase population size if it is.
    # print("checking popsize to increase if necessary")
    removal_dict = {}
    for ind in pop:
        removal_dict[ind.myID] = False
    pop_to_save = []
    for i in range(len(pop)):
        for j in range(len(pop)):
            if i != j and not removal_dict[pop[i].myID]:
                removal_dict[pop[i].myID] = dominates(j, i, pop)
    for ind in pop:
        if not removal_dict[ind.myID]:
            pop_to_save.append(ind.myID)
    
    if len(pop_to_save) > popsize:
        popsize = len(pop_to_save)
        print("Popsize increased to", popsize, flush=True)


    # print("entering selection")
    # Remove dominated individuals until the target population size is reached
    while len(pop) > popsize:

        # Choose two different individuals from the population
        ind1 = np.random.randint(len(pop))
        ind2 = np.random.randint(len(pop))
        while ind1 == ind2:
            ind2 = np.random.randint(len(pop))

        if dominates(ind1, ind2, pop):  # ind1 dominates

            # # remove ind2 from population and shift following individuals up in list
            for i in range(ind2, len(pop) - 1):
                pop[i] = pop[i + 1]
            pop.pop()  # remove last element from list (because it was shifted up)
            # print('ind1', pop[ind1].myID, pop[ind1].fitness1, pop[ind1].fitness2)
            # print('ind2', pop[ind2].myID, pop[ind2].fitness1, pop[ind2].fitness2)
            # print('ind 2 dominated')
            # pop.pop(ind2)

        elif dominates(ind2, ind1, pop):  # ind2 dominates

            # remove ind1 from population and shift following individuals up in list
            for i in range(ind1, len(pop) - 1):
                pop[i] = pop[i + 1]
            pop.pop()  # remove last element from list (because it was shifted up)
            # print('ind1', pop[ind1].myID, pop[ind1].fitness1, pop[ind1].fitness2)
            # print('ind2', pop[ind2].myID, pop[ind2].fitness1, pop[ind2].fitness2)
            # print('ind 1 dominated')
            # pop.pop(ind1)

    assert len(pop) == popsize
    # print('selection done')
    return pop, pop_to_save


def dominates(ind1, ind2, pop):
    # Returns true if ind1 dominates ind2, otherwise false
    if pop[ind1].fitness1 == pop[ind2].fitness2 and pop[ind1].fitness1 == pop[ind2].fitness2:
        return pop[ind1].myID > pop[ind2].myID  # if equal, return the newer individual

    elif pop[ind1].fitness1 >= pop[ind2].fitness1 and pop[ind1].fitness2 >= pop[ind2].fitness2:
        return True
    else:
        return False
