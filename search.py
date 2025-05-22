import os 
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import sys 

run_num = sys.argv[1]
run_name = 'quadruped'+str(run_num)
phc = PARALLEL_HILL_CLIMBER(run_name, run_num)
phc.Evolve("DIRECT")
# phc.Show_Best()
