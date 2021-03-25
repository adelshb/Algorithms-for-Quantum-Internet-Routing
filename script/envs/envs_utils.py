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

from typing import List
import networkx as nx

def active_nodes(G: object)->List:
    """ Collect all the active nodes (nodes where there is still entanglement with another node)
    Args:
        G: Graph (networkX graph object representing current status of the quantum network)
    Returns:
        List of active nodes.
    """

    nodes = []
    for i,row in enumerate(G.nodes):
        for j,val in enumerate(row):
            if val !=0 and j!=i:
                nodes.append(i)
            break

    return nodes

def random_graph(vertices: int,
                edges: int,
                seed: None)-> object:
    """Generate random graph"""
    G = nx.gnm_random_graph(n= vertices , m= edges, seed= seed)
    return G