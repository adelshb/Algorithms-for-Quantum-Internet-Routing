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
Cycle physical network with vitual network with edges between i-th node and all nodes within distance dth on physical network.
"""

import networkx as nx

def cycle_net(n =10, dth= 2):

    # Physical network
    C = nx.cycle_graph(n)

    # Virtual network
    Q = nx.Graph()
    # Add edges up to distance dth in virtual network
    Q.add_edges_from([(i, (i + d) %n ) for i in range(n) for d in range(1, dth+1)])

    return C, Q