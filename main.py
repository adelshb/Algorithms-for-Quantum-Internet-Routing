from script.envs.random import RandomEnvironement
import networkx as nx

n = 10
m = 5
C = nx.cycle_graph(n)
Q = nx.nx.gnm_random_graph(n,m)

env = RandomEnvironement(classical_network = C, quantum_network = Q)
