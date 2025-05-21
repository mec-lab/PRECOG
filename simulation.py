from robot import ROBOT
from world import WORLD 
import contextlib
with contextlib.redirect_stdout(None):
    import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np 
import random
import matplotlib.pyplot as plt
import math 
import constants as c
import torch

class SIMULATION:

    def __init__(self, directOrGUI, solutionID, runName, runNum, startTime):
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        self.runNum = runNum
        self.runName = runName
        self.startTime = startTime
        self.trajectories = np.zeros((2,c.timesteps))
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        
        self.world = WORLD(solutionID, self.runNum)
        self.robot = ROBOT(solutionID, self.runName, self.runNum)

    def Run(self):
        f = open("run{}/trajectories/trajectory{}.csv".format(self.runNum, self.robot.solutionID), "w")
        f.write('step,x,y,z\n')
        for i in range(c.timesteps):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

            self.robot.Track_Fitness(i,f, self.trajectories)
            if self.directOrGUI != "DIRECT":
                time.sleep(1/300)
        f.close()
        end = time.time()
        np.save('data/{}/simtime{}'.format(self.runName, self.solutionID), [end - float(self.startTime)])
        

    def Get_Fitness(self):
        self.robot.Get_Fitness()
    def __del__(self):
        try:
            p.disconnect()
        except:
            pass
        