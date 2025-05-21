import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from pysr import PySRRegressor
import contextlib
import os

run_name = 'bm_afpo'
for i in range(30):
    os.makedirs('data/{}/run{}'.format(run_name, i), exist_ok=True)


