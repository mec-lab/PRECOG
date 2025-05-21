from solution import SOLUTION
import constants as c 
import copy 
import os
from selection import survivor_selection
import numpy as np
import time
import random


class PARALLEL_HILL_CLIMBER:

    def __init__(self, run_name, run_num):
        self.runName = run_name
        self.runNum = run_num
        self.bots_to_process = []
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm run{}/brain*.nndf".format(self.runNum))
        os.system("rm run{}/fitness*.txt".format(self.runNum))
        os.makedirs('run{}'.format(self.runNum), exist_ok=True)
        os.makedirs("run{}/trajectories".format(self.runNum), exist_ok=True)
        os.makedirs("data/"+str(self.runName), exist_ok=True)
        os.system("rm run{}/trajectories/*.csv".format(self.runNum))

        self.nextAvaliableID = 0
        self.parents = {}
        self.fitnesses1 = np.zeros((c.populationSize,c.numberOfGenerations))
        self.fitnesses2 = np.zeros((c.populationSize, c.numberOfGenerations))
        self.parent_names = np.zeros((c.populationSize, c.numberOfGenerations))

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvaliableID, self.runName, self.runNum)
            self.nextAvaliableID+=1
        

    
    def Evolve(self, directOrGUI):
        self.directOrGUI = directOrGUI
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(self.directOrGUI, currentGeneration)
            np.save('data/'+str(self.runName)+'/fit1', self.fitnesses1)
            np.save('data/'+str(self.runName)+'/fit2', self.fitnesses2)
            np.save('data/'+str(self.runName)+'/names', self.parent_names)

    
    def Evaluate(self, solutions):
        for parent in solutions.values():
            parent.Start_Simulation(self.directOrGUI)
        for parent in solutions.values():
            parent.Wait_For_Simulation_To_End()

    def Evolve_For_One_Generation(self, directOrGUI, gen):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Select()
        self.Print(gen)

    def Print(self, gen):
        print("\n", "Generation", gen, flush=True)
        for k, v in self.parents.items():
            print("Parent", self.parents[k].myID, 'Fitness1:', self.parents[k].fitness1, "\n", flush=True)
            print("Parent", self.parents[k].myID, 'Fitness2:', self.parents[k].fitness2, "\n", flush=True)
            # print('Fitness 2', self.children[k].fitness2, self.parents[k].fitness2, "\n")
            self.fitnesses1[k][gen] = self.parents[k].fitness1
            self.fitnesses2[k][gen] = self.parents[k].fitness2
            self.parent_names[k][gen] = self.parents[k].myID

    def Spawn(self):
        self.children = {}
        for i, parent in self.parents.items():
            self.children[i] = copy.deepcopy(parent)
            self.children[i].Set_ID(self.nextAvaliableID)
            self.nextAvaliableID +=1 


    def Mutate(self):
        for child in self.children.values():
            child.Mutate()


    def Select(self):
        # population selection
        population = []
        for k,v in self.parents.items():
            population.append(v)
        for k,v in self.children.items():
            population.append(v)
        new_parents, self.bots_to_process = survivor_selection(population, c.populationSize)
        if len(new_parents) > c.populationSize:
            new_parents = random.choices(new_parents, k=c.populationSize)
        new_parents = sorted(new_parents, key=lambda individual:individual.fitness1, reverse=True)

        for i in range(c.populationSize):
            self.parents[i] = new_parents[i]


    def Show_Best(self):
        best_fit = -10
        best_sln = ""
        for k, v in self.parents.items():
            if v.fitness1 > best_fit: 
                best_fit = v.fitness1
                best_sln = v
        best_sln.Start_Simulation("x")

