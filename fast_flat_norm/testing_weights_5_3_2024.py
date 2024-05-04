import numpy as np
import matplotlib.pyplot as plt 
from sympy import *
from flat_norm import get_weights
from flat_norm import flat_norm

# #16 neighbor vectors to the origin, to be sent directly to get_weights
# u = np.array([[(-1.0,0.0),(1.0,0.0),(0.0,-1.0),(0.0,1.0)\
#               ,(-1.0,1.0),(1.0,1.0),(1.0,-1.0),(-1.0,-1.0)\
#                   ,(-2.0,1.0),(-1.0,2.0),(1.0,2.0),(2.0,1.0)\
#                       ,(2.0,-1.0),(1.0,-2.0),(-1.0,-2.0),(-2.0,-1.0)]])
    
# lengths = [np.linalg.norm(u[0],axis=1)]

# print(get_weights(u,lengths))
    
#verifying same test as above but end to end

points = np.array([(0.0,0.0),(-1.0,0.0),(1.0,0.0),(0.0,-1.0),(0.0,1.0)\
              ,(-1.0,1.0),(1.0,1.0),(1.0,-1.0),(-1.0,-1.0)\
                  ,(-2.0,1.0),(-1.0,2.0),(1.0,2.0),(2.0,1.0)\
                      ,(2.0,-1.0),(1.0,-2.0),(-1.0,-2.0),(-2.0,-1.0)])

flat_norm(points,np.ones(len(points)),lamb=1.0,neighbors=16)

print("KRV: ", [0.1221, 0.0476, 0.0454])

