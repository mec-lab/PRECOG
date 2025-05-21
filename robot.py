import pyrosim.pyrosim as pyrosim
import contextlib
with contextlib.redirect_stdout(None):
    import pybullet as p
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os 
import constants as c
import time
from process_trajectories_pysr import generate_eqn
import numpy as np
import random


class ROBOT:

    def __init__(self, solutionID, runName, runNum):
        self.solutionID = solutionID
        self.runName = runName
        self.runNum = runNum
        self.robotId = ""
        self.blockId = ""

        while self.robotId == "":
            try:
                self.robotId = p.loadURDF("run{}/body.urdf".format(self.runNum))
            except:
                time.sleep(0.01)
        
        # while self.blockId == "":
        #     try:
        #         self.blockId = p.loadURDF("block.urdf")
        #     except:
        #         time.sleep(0.01)


        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        self.nn = NEURAL_NETWORK("run{}/brain{}.nndf".format(self.runNum, self.solutionID))
        os.system("mv run{}/brain{}.nndf data/{}/".format(self.runNum, self.solutionID, self.runName))
        # os.system("rm run{}/brain{}.nndf".format(self.runNum, self.solutionID))


    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for k,v in self.sensors.items():
            v.Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[str(jointName)] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle*c.motorJointRange)
    def Think(self):
        #replace click with proximity to block
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        click = xPosition
        self.nn.Update(click)

    def Track_Fitness(self, step, f, trajectories):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]

        f.write(str(step)+','+str(xPosition) + ',' + str(yPosition)+','+str(zPosition)+'\n')
        trajectories[0][step] = xPosition
        trajectories[1][step] = yPosition

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        r2_fitness = generate_eqn("run{}/trajectories/trajectory{}.csv".format(self.runNum, self.solutionID), self.solutionID, self.runName)
        f = open("run{}/tmp{}.txt".format(self.runNum, self.solutionID), "w")
        f.write(str(xPosition)+','+str(r2_fitness))
        f.close()
        os.rename("run{}/tmp{}.txt".format(self.runNum, self.solutionID), "run{}/fitness{}.txt".format(self.runNum, self.solutionID))
    #    os.system("rename tmp{}.txt fitness{}.txt".format(self.solutionID, self.solutionID))



        
