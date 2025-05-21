import sympy as sp
import numpy as np
import torch
import time
import pandas as pd
import matplotlib.pyplot as plt

def get_predicted_traj(botID, runName, runNum):
    bot = pd.read_csv('data/{}/run{}/trajectory{}.csv'.format(runName, runNum, botID))
    bot['x'] = pd.to_numeric(bot['x'])
    bot['y'] = pd.to_numeric(bot['y'])
    x = bot['x'].to_numpy()[:10000]
    y = bot['y'].to_numpy()[:10000]
    trajectory = np.stack([x, y], axis=0)
    return trajectory
def process_eqns(botID, runName, runNum):
    timesteps = 10000
    predicted_traj = np.zeros((2 ,timesteps))
    simulated_traj = get_predicted_traj(botID, runName, runNum)
    for i in range(0, timesteps):
        eqns = []
        with open('data/{}/run{}/eqn{}.txt'.format(runName, runNum, botID)) as file:
            read_eqns = [line.rstrip() for line in file]
        for eqn in read_eqns:
            separate = eqn.split(':')
            clean_eq = separate[1].replace('x0', 'x').strip()
            eqns.append(clean_eq)
        for j, eqn in enumerate(eqns):
            eqn = str(eqn)
            eq = sp.simplify(sp.sympify(eqn))
            predicted_traj[j][i] = eq.subs('x', i)
    # eqns = []
    # with open('data/{}/run{}/eqn{}.txt'.format(runName, runNum, botID)) as file:
    #     read_eqns = [line.rstrip() for line in file]
    # for eqn in read_eqns:
    #     separate = eqn.split(':')
    #     clean_eq = separate[1].replace('x0', 'x').strip()
    #     eqns.append(clean_eq)
    # for j, eqn in enumerate(eqns):
    #     eqn = str(eqn)
    #     eq = sp.simplify(sp.sympify(eqn))
    #     print(eq)

    plt.figure()
    plt.plot(simulated_traj[0], label='Simulated X', color='tab:olive', linestyle='solid')
    plt.plot(predicted_traj[0], label="Predicted X", color='tab:olive', linestyle='dashed')
    plt.plot(simulated_traj[1], label='Simulated Y', color='tab:cyan', linestyle='solid')
    plt.plot(predicted_traj[1], label="Predicted Y", color='tab:cyan', linestyle='dashed')
    plt.xlabel("Timesteps")
    plt.ylabel("Robot Position")
    plt.legend()
    plt.show()

    plt.figure()
    plt.plot(simulated_traj[0], simulated_traj[1], color='green', linewidth='4')
    plt.plot(predicted_traj[0], predicted_traj[1], color='purple', linestyle='dashed', linewidth='4')
    plt.show()

if __name__ == '__main__':
    run_name = 'bm_quadruped'
    bot_name = 1091
    run_num = 6

    process_eqns(bot_name, run_name, run_num)