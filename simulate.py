# import pybullet as p
import time
# import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np 
import random
import matplotlib.pyplot as plt
import math 
import constants as c 
from simulation import SIMULATION
import sys 

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
runName = sys.argv[3]
runNum = sys.argv[4]
startTime = sys.argv[5]

simulation = SIMULATION(directOrGUI, solutionID, runName, runNum, startTime)
simulation.Run()
simulation.Get_Fitness()


simulation.__del__()