import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np 
import random
import matplotlib.pyplot as plt
import math 
import constants as c 
import time
import os 
class WORLD:

    def __init__(self, solutionID, runNum):
        time.sleep(1)
        p.loadSDF("run{}/world{}.sdf".format(runNum, solutionID))
        planeId = p.loadURDF("plane.urdf")
        os.system("rm run{}/world{}.sdf".format(runNum, solutionID))
