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

# from abc import ABC, abstractmethod
from typing import List

from networkx.classes import Graph, DiGraph

import numpy as np

class MCtree(object):
    """
    Class for Monte Carlo Tree.

    """

    def __init__(self,
                 init_state: Graph,
                 c: float) -> None:

        # Initialize the Monte Carlo tree with the root node
        state_attrs = {'Q':0, 'N':0, "state": init_state, 'action': None}
        self._tree = DiGraph()
        self._tree.add_node(1, **state_attrs)
        
        # Get parameters
        self._c = c

    def ucb1(self, node: int) -> float:
        """ Compute the UCB1 score """
        ind = list(self._tree.predecessors(node))[0]
        ucb1 = self._tree.nodes[node]['Q'] + self._c * np.sqrt(np.log(self._tree.nodes[ind]['N'])/(self._tree.nodes[node]['N']+0.0001))
        return ucb1
    
    def is_leaf(self, node: int) -> bool:
        """ Check if the given node is a leaf """
        if list(self._tree.successors(node)):
            return False
        else: 
            return True

    def successors(self, node: int) -> List:
        """ Return list of successors of given node """
        return list(self._tree.successors(node))

    def count(self, node: int) -> int:
        """ Return the visit count of a state"""
        return self._tree.nodes[node]['N']

    def Q(self, node: int) -> float:
        """ Return the Q function of a state"""
        return self._tree.nodes[node]['Q']
    
    def action(self, node: int) -> float:
        """ Return the action that lead the predecessor to this node"""
        return self._tree.nodes[node]['action']

    def expand(self, node: int, N: int, states: List[object], actions: List) -> None:
        """ Check if the given node is a leaf """
        V = self._tree.number_of_nodes()
        for n in range(N):
            state_attrs = {'Q':0, 'N':0, "state": states[n], 'action':actions[n]}
            self._tree.add_node(n+V+1, **state_attrs)
            self._tree.add_edge(node,n+V+1)
        return None

    def backup(self, node: int, reward: float) -> None:
        """ Update the Q function and visit count of all nodes from leaf to root """
        # Update leaf
        self._tree.nodes[node]['Q'] += reward
        self._tree.nodes[node]['N'] += 1

        # Update predecessors until root
        curr = node
        while True:
            try:
                curr = list(self._tree.predecessors(curr))[0]
            except:
                return None
            self._tree.nodes[curr]['Q'] += reward
            self._tree.nodes[curr]['N'] += 1