import pandas as pd
from pysr import PySRRegressor
import numpy as np
from torcheval.metrics import R2Score
import torch
import contextlib

def generate_eqn(runName, runNum, botID):
    csv_path = 'data/{}/run{}/trajectory{}.csv'.format(runName, runNum, botID)

    bot = pd.read_csv(csv_path)
    bot['step'] = pd.to_numeric(bot['step'])
    bot['x'] = pd.to_numeric(bot['x'])
    bot['y'] = pd.to_numeric(bot['y'])

    try:
        times = bot['step'].to_numpy()
        times = times.reshape(-1,1)

        x = bot['x'].to_numpy()
        y = bot['y'].to_numpy()
        trajectory = np.stack([x, y], axis=1)

        binary_operators = ['+', '*', '-', '/', '^']
        unary_operators = ['cos', 'sin', 'tan', 'exp', 'log']
        # print('model start')

        with contextlib.redirect_stdout(None):
            model = PySRRegressor(maxsize=20, niterations=15, binary_operators=binary_operators,
                                  unary_operators=unary_operators, maxdepth=7, progress=False,
                                  timeout_in_seconds=90)

            model.fit(times, trajectory)

        # print('model end')
        pred_traj = model.predict(times)
        r2 = get_r2_score(pred_traj, trajectory)

        if np.isnan(r2):
            r2 = -np.inf

        eqn_x, eqn_y = model.sympy()
        f2 = open("data/{}/run{}/eqn{}.txt".format(runName, runNum, botID), "w")
        f2.write("x : {} \n".format(eqn_x))
        f2.write("y : {} \n".format(eqn_y))
        f2.close()
        lenx = len(str(eqn_x))
        leny = len(str(eqn_y))

    except Exception as e:
        r2 = -np.inf
        lenx = -np.inf
        leny = -np.inf
        print(e)

    return r2, lenx, leny

def get_r2_score(pred, true):
    # print(pred.shape)
    # print(true.shape)
    assert pred.shape == true.shape, "predicted and true trajectories are not the same shape"
    metric = R2Score()
    metric.update(torch.from_numpy(pred), torch.from_numpy(true))
    score = metric.compute()
    return score.item()

if __name__ == '__main__':
    runName = 'bm_afpo'
    bots = np.load('data/{}/bestindivs.npy'.format(runName))
    r2s = []
    lenxs = []
    lenys = []
    for i in range(30):
        botID = bots[i]
        r2, lenx, leny = generate_eqn(runName, i, botID)
        r2s.append(r2)
        lenxs.append(lenx)
        lenys.append(lenys)
    print(r2s)
    np.save('data/{}/r2s'.format(runName), np.array(r2s))
