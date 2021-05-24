# -*- coding: utf-8 -*-
#
# Written by Adel Sohbi, https://github.com/adelshb
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Random physical and virtual network.
"""

import networkx as nx
from networkx.generators.random_graphs import random_geometric_graph, watts_strogatz_graph

def random_net(n =10, radius = 0.1, dth = 2, p = 0.1):

    # Physical network
    C = random_geometric_graph(n, radius, dim=2, pos=None, p=2, seed=None)
    C.remove_nodes_from(list(nx.isolates(C)))

    # Virtual network
    # small world network
    Q = watts_strogatz_graph(n, k=dth, p=p, seed=None)
    Q.remove_nodes_from(list(nx.isolates(Q)))

    return C, Q