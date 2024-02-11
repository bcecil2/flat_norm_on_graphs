"""
ID: bwukki1
LANG: PYTHON3
TASK: test
"""

import numpy as np
import matplotlib.pyplot as plt 
from sympy import *
from scipy.integrate import quad_vec,quad,trapezoid,fixed_quad
from time import perf_counter
import cubepy as cp


def integrand_2d(x,ui,uj):
    nu = np.array([np.cos(x),np.sin(x)])
    return np.abs(np.dot(ui,nu)*np.dot(uj,nu))

def cpintegrand_2d(x,ui,uj):
    """call with cp.integrate(integrand,0,2*np.pi,([ui],[uj]))"""
    nu = np.zeros((len(x),2))[...,np.newaxis]
    nu[:,0] = np.cos(x)
    nu[:,1] = np.sin(x)
    return np.abs(np.dot(ui,nu)*np.dot(uj,nu))

ui = np.array([1.0,1.0])
uj = np.array([1.0,1.0])

test_number = 100

for i in range(test_number):
    quad_time = []
    quad_vec_time = []
    trap_time = []
    cp_time = []
    fixed_quad_time = []
    t1 = perf_counter()
    quad_vec(integrand_2d,0,2*np.pi,epsabs=1e-08,args=(ui,uj))
    quad_vec_time.append(perf_counter()-t1)
    t2 = perf_counter()
    quad(integrand_2d,0,2*np.pi,args=(ui,uj))
    quad_time.append(perf_counter()-t2)
    t3 = perf_counter()
    x = np.arange(0,2*np.pi,1e-04)
    y = integrand_2d(x,ui,uj)
    trapezoid(y)
    trap_time.append(perf_counter()-t3)
    t4 = perf_counter()
    cp.integrate(cpintegrand_2d, 0, 2*np.pi,([ui],[uj]),itermax=50)
    cp_time.append(perf_counter()-t4)
    t5 = perf_counter()
    fixed_quad(integrand_2d,0,2*np.pi,args=(ui,uj))
    fixed_quad_time.append(perf_counter()-t5)
    
print("vec:", np.mean(np.array(quad_vec_time)))
print("quad:", np.mean(np.array(quad_time)))
print("trapz:", np.mean(np.array(trap_time)))
print("cubepy:", np.mean(np.array(cp_time)))
print("fixed quad:", np.mean(np.array(fixed_quad_time)))

print(np.mean(np.array(quad_vec_time))/np.mean(np.array(quad_time)))

