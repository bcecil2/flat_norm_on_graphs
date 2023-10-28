import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools


eweight = "euc_weight"

#might be able to improve with np.parition/argparition?
#scikit learn has method as well
def knn(graph, node, n):
    """returns n nearest neighbors for a given node, sorted by weight"""
    return set(map(lambda x: (x[1],x[2],x[0]),
                    sorted([(e[2][eweight], e[0], e[1])
                            for e in graph.edges(node, data=True)])[:n]))

def make_complete(points):
    """
    points : List[[Float]]
    returns: points, edges
    """
    edges = []
    print(points)
    S = set()
    for point1 in points:
        for point2 in points:
            if point1 != point2 and (point2,point1) not in S:
                edges.append((point1,point2))
                S.add((point1,point2))
    
    # connections = itertools.combinations(points,2)
    # com_vert = []
    # com_edges = []
    # for entry in connections:
    #     com_edges.append(entry)
    #     com_vert.append(entry[0])
    #     com_vert.append(entry[1])
               
    # for k in range(0,len(com_edges)):
    #     iterbreak = 0
    #     for i in range(0,len(com_edges)):
    #         iterlen = len(com_edges)-1
    #         for j in range(0,iterlen):
    #             if com_edges[i][0] == com_edges[j][1]:
    #                 if com_edges[i][1] == com_edges[j][0]:
    #                     com_edges.remove(com_edges[i])
    #                     iterbreak = 1
    #                     break
    #         if iterbreak == 1:
    #             break
    return edges

def euclidean_weight(edge):
    point1,point2 = np.array(edge)
    vector = (point2[0] - point1[0],point2[1] - point1[1],point2[2] - point1[2])
    return np.linalg.norm(vector)

def euclidean_graph(points,edges):
    """
    points : List[[Float]]
    edges: List[tuple[Float,Float]]
    returns: networkx graph, edges weighted by euclidean distance
    """
    weighted_edges = [edge + ({eweight: euclidean_weight(edge)},) for edge in edges]
    G = nx.Graph()
    G.add_nodes_from(points)
    G.add_edges_from(weighted_edges)
    return G
    
def split_coords(points):
    """split up the x,y coordinates of a list of points"""
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    z = [points[2] for point in points]
    return x,y,z

def line_midpoint(point1,point2,point3):
    """calculate the midpoint of a line"""
    x1,y1,z1 = point1
    x2,y2,z2 = point2
    return (1/2*(x1+x2),1/2*(y1+y2),1/2*(z1+z2))
  

def get_source_and_sink_cords(G):
    max_x,max_y,max_z = -10000000,-1000000 
    min_x,min_y,min_z = 10000000, 10000000
    for entry in G.nodes:
        if entry not in ["source","sink"]:
            max_x = max(max_x,entry[0])
            max_y = max(max_y,entry[1])
            max_z = max(max_z,entry[2])
            
            min_x = min(min_x,entry[0])
            min_y = min(min_y,entry[1])
            min_z = min(min_z,entry[2])
            
    source = (max_x+1,max_y+1,max_z+1)
    sink = (min_x-1,min_y-1,min_z-1)
    return source,sink

def euclidean_plot_3d(G,labels=True):
    """plot a graph of euclidean points with labeled vertices and weights"""
    
    cap = "capacity"
    
    source_cord,sink_cord = get_source_and_sink_cords(G)
    for entry in G.nodes:
        if not isinstance(entry,str):
            #plt.annotate("({:.2f},{:.2f})".format(*entry),entry)
            None
        elif entry == "source":
            plt.annotate("source", source_cord)
        else:
            plt.annotate("sink", sink_cord)
            
    for u,v,d in G.edges(data=True):
        if u == "source":
            u = source_cord
        elif u == "sink":
            u = sink_cord
        elif v == "source":
            v = source_cord
        elif v == "sink":
            v = sink_cord
        edge = (u,v)
        
            
        if labels:
            midp = line_midpoint(u,v)
            if eweight in d:
                #plt.annotate("d:"+"{:.2f}".format(d[eweight]), midp)
                None
            if cap in d:
                plt.annotate(" fw:" + "{:.2f}".format(d[cap]) , (midp[0], midp[1]))
        plt.plot(*split_coords(edge),'ro-')

def knn_reduced_graph(G,k):
    """reduce a graph to k nearest neighbors"""
    edges = set()
    for n in G.nodes:
        edges = edges.union(knn(G,n,k))
    reduced_graph = nx.Graph()
    reduced_graph.add_nodes_from(G.nodes)
    reduced_graph.add_edges_from(map(lambda x: (x[0],x[1],{eweight:x[2]}), edges))
    return reduced_graph

def get_edge_vectors(G,node):
    """make the list of u vectors for a given node"""
    edges = list(G.edges(node))
    converted_list = np.array(edges)
    return converted_list[:,1]-converted_list[:,0],edges

def add_source_sink(G,A,lamb):
    source = "source"
    sink = "sink"
    G.add_node(source)
    G.add_node(sink)
    for point in G.nodes:
        if point in A:
            G.add_edge(source,point,capacity=lamb)
        elif point not in [source,sink]:
            G.add_edge(sink,point,capacity=lamb)

def min_cut_max_flow(G,in_set,lamb=1):
    add_source_sink(G,in_set,lamb)
    from networkx.algorithms.flow import dinitz,edmonds_karp
    cut_value, partition = nx.minimum_cut(G,"source","sink",flow_func=edmonds_karp)
    max_flow, flow_dict = nx.maximum_flow(G, "source","sink", flow_func=edmonds_karp)
    #euclidean_plot_2d(G)
    keep,_ = partition
    print(len(keep))
    return keep, max_flow
