import sympy as sp
import numpy as np
import torch
from torcheval.metrics import R2Score
import time
import constants as c


def get_r2_score(pred, true):
    # print(pred.shape)
    # print(true.shape)
    assert pred.shape == true.shape, "predicted and true trajectories are not the same shape"
    metric = R2Score()
    metric.update(torch.from_numpy(pred), torch.from_numpy(true))
    score = metric.compute()
    return score.item()

def process_eqns(botID, runName):
    timesteps = 15000
    predicted_traj = np.zeros((2,timesteps))
    times = []
    r2s = []
    sim_traj = np.load('data/{}/sim_trajectories{}.npy'.format(runName, botID))
    try:
        for i in range(0, timesteps):
            start = time.time()
            eqns = []
            with open('data/{}/eqn{}.txt'.format(runName, botID)) as file:
                read_eqns = [line.rstrip() for line in file]
            for eqn in read_eqns:
                separate = eqn.split(':')
                clean_eq = separate[1].replace('x0','x').strip()
                eqns.append(clean_eq)
            for j,eqn in enumerate(eqns):
                eqn = str(eqn)
                eq = sp.sympify(eqn)
                predicted_traj[j][i] = eq.subs('x', i)
            end = time.time()
            times.append(end-start)
            r2 = get_r2_score(predicted_traj[:,i], sim_traj[:,i])
            r2s.append(r2)

    except Exception as e:
        print("-------------------------------------------------------", flush=True)
        print('error', e, flush=True)
        print("-------------------------------------------------------", flush=True)
    
    # np.save('data/{}/r2s{}'.format(runName, botID), np.array(r2s))
    # np.save('data/{}/eqn_times{}'.format(runName, botID), np.array(times))
    # np.save('data/{}/eqn_traj{}'.format(runName, botID), predicted_traj)
    
    
    
        

if __name__ == '__main__':
    run_name = 'bm_per_timestep_save_ood_times/run1'
    bot_name = 1021

    process_eqns(bot_name, run_name)