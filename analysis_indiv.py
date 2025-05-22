import numpy as np

class Indiv:
    def __init__(self, fit1, fit2, name):
        self.fit1 = fit1
        self.fit2 = fit2
        self.remove = False
        self.name = name