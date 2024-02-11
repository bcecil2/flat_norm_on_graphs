import os
import sys
import numpy as np
from time import perf_counter
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import flat_norm_rewrite_main as fn
import pytest

def generate_disk(radius,N):
    x = np.linspace(-radius,radius,N)
    y = np.linspace(-radius,radius,N)
    x,y = np.meshgrid(x,y)
    cond = x**2+y**2<=radius
    x,y = x[cond], y[cond]
    A = np.column_stack((x,y))
    return A

def test_neighbors_small_exception():
    neighbors = 50
    A = np.linspace(0,1)
    A = np.column_stack((A,A))
    with pytest.raises(Exception):
        fn.flat_norm(A,neighbors)

def test_tree_graph_shape():
    neighbors = 24
    A = generate_disk(1,100)
    numpoints = A.shape[0]
    Tree,graph = fn.calculate_tree_graph(A,neighbors)
    assert graph.shape == (numpoints,2,neighbors+1)
    return

def test_uniform_grid_edge_vectors():
    full_neighbors = 24
    radius = 1
    test_points = 100
    A = generate_disk(radius,test_points)
    numpoints = A.shape[0]
    tree,graph = fn.calculate_tree_graph(A,full_neighbors)
    vectors,lengths = fn.calculate_edge_vectors(A,graph)
    assert vectors.shape == (numpoints,full_neighbors,2)
    assert lengths.shape == (numpoints,full_neighbors)
    E = np.array([[0.0,0.0],[1.0,0],[2.0,0.0]])
    neighbors_small = 2
    tree_small,graph_small = fn.calculate_tree_graph(E,neighbors_small)
    vectors_small,lengths_small = fn.calculate_edge_vectors(E,graph_small)
    test_vectors_small = np.array(
    [[[ 1.,  0.],
      [ 2.,  0.]],

     [[ 1.,  0.],
      [-1.,  0.]],

     [[-1.,  0.],
      [-2.,  0.]]])
    assert np.all(vectors_small == test_vectors_small)
    test_lengths_small = np.array([[1.0,2.0],[1.0,1.0],[1.0,2.0]])
    assert np.all(lengths_small == test_lengths_small)
    return


test_neighbors_small_exception()
