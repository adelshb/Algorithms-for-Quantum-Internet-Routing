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
from networkx.generators.random_graphs import fast_gnp_random_graph

def random_net(n = 10, p = 0.2):

    # Physical network
    C = fast_gnp_random_graph(n, p, seed=None, directed=False)
    C.remove_nodes_from(list(nx.isolates(C)))

    # Virtual network
    Q = fast_gnp_random_graph(n, p, seed=None, directed=False)
    Q.remove_nodes_from(list(nx.isolates(Q)))

    if not list(C.nodes) or not list(Q.nodes):
        C, Q = random_net(n, p+0.01)

    return C, Q