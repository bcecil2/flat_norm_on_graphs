import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from scipy.spatial import KDTree

def calculate_tree_graph(points,neighbors=24):
    Tree = KDTree(points)
    graph = np.array([Tree.query(point,neighbors+1) for point in points])
    graph = np.stack(graph)
    return Tree,graph

def calculate_edge_vectors(points,graph):
    lengths = graph[:,0,1:]
    nn = graph[:,1,:].astype(np.int32)
    edges = points[nn[:,1:]]
    vertices = points[nn[:,0]]
    vertices = vertices[:,np.newaxis]
    return edges-vertices,lengths

def flat_norm(points,neighbors = 24):
    if neighbors >= len(points):
        raise Exception("Need more points than neighbors")
    Tree,graph = calculate_tree_graph(points,neighbors)
    vectors,lengths = calculate_edge_vectors(points,graph)
    return 

