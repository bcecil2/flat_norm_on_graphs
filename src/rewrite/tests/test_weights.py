import os
import sys
import numpy as np
from time import perf_counter
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import flat_norm_rewrite_main as fn
import pytest

def compare_with_paper():
    u = np.array([(-1.0,0.0),(1.0,0.0),(0.0,-1.0),(0.0,1.0)\
                  ,(-1.0,1.0),(1.0,1.0),(1.0,-1.0),(-1.0,-1.0)\
                      ,(-2.0,1.0),(-1.0,2.0),(1.0,2.0),(2.0,1.0)\
                          ,(2.0,-1.0),(1.0,-2.0),(-1.0,-2.0),(-2.0,-1.0)])
    result = fn.solve_weights_system(u)
    print("Ours: ", [result[0],result[5],result[9]])
    print("KRV: ", [0.1221, 0.0476, 0.0454])
    return u,result