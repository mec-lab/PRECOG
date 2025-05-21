import sympy as sp
import numpy as np
import torch
import time
import pandas as pd
import matplotlib.pyplot as plt

def process_eqns(runName, runNum, botID):
    eqns = []
    botID = int(botID)
    with open('data/{}/run{}/eqn{}.txt'.format(runName, runNum, botID)) as file:
        read_eqns = [line.rstrip() for line in file]
    for eqn in read_eqns:
        separate = eqn.split(':')
        clean_eq = separate[1].replace('x0', 'x').strip()
        eqns.append(clean_eq)
    return eqns

def analyze_operators(operators, runName, runNum, botIDs):
    operators_dict = {}
    for op in operators:
        operators_dict[op] = 0

    eqns = []
    for botID in botIDs:
        bot_eqns = process_eqns(runName, runNum, botID)
        eqns.extend(bot_eqns)
    print(eqns)
    for eqn in eqns:
        for op in operators:
            operators_dict[op] += eqn.count(op)

    print(operators_dict)
    heights = []
    for value in operators_dict.values():
        heights.append(value)

    labels = ['cos', 'sin', 'log', 'pow', '*', '+', '/', '-', 'tan', 'exp']
    x = np.arange(len(operators))
    plt.figure()
    plt.bar(x,heights, color='tab:grey')
    plt.xticks(x, labels=labels)
    plt.xlabel('Operators')
    plt.ylabel("Frequency")
    plt.show()

def analyze_lengths(runName, runNum, gens):
    len_dict = {}
    std_dict = {}
    for gen in gens:
        eqns = []
        botIDs = np.load('data/{}/run{}/gen{}_paretonames.npy'.format(runName, runNum, gen)).tolist()
        for botID in botIDs:
            bot_eqns = process_eqns(runName, runNum, botID)
            eqns.extend(bot_eqns)
        lengths = []
        for eqn in eqns:
            lengths.append(len(eqn))
        print("Gen", gen, "Ave Length", np.mean(lengths))
        len_dict[gen] = np.mean(lengths)
        std_dict[gen] = np.std(lengths)

    heights = []
    for value in len_dict.values():
        heights.append(value)
    stds = []
    for value in std_dict.values():
        stds.append(value)

    x = np.arange(len(gens))
    plt.figure()
    plt.bar(x, heights, color='tab:grey', yerr=stds)
    plt.xticks(x, labels=gens)
    plt.xlabel('Generations')
    plt.ylabel("Equation Length")
    plt.show()




if __name__ == '__main__':
    runName = 'bm_quadruped'
    runNum = 6
    botIDs = []
    for gen in [0, 9, 19, 29, 39, 49]:
        botIDs.extend(np.load('data/{}/run{}/gen{}_paretonames.npy'.format(runName, runNum, gen)).tolist())
    botIDs = list(set(botIDs))
    operators = ['cos', 'sin', 'log', '**', '*', '+', '/', '-', 'tan', 'exp']
    analyze_operators(operators, runName, runNum, botIDs)

    gens = [0, 9, 19, 29, 39, 49]
    analyze_lengths(runName, runNum, gens)

