# -*- coding: utf-8 -*-
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Shorthest Path Agent for Quantum Internet Network Routing.
"""

import networkx as nx
from networkx.classes import Graph
from agents.agent import Agent

class ShortestPathAgent(Agent):
    """
    Agent that selects the shortest path between the sender and reciever on the current state of the virtual network.
    """

    def __init__(self,
                 physical_network: Graph,
                 virtual_network: Graph) -> None:
        """
        Args:
            physical_network: classical network
            virtual_network: initial quantum network
        """
        
        # Get parameters
        self._physical_network = physical_network
        self._virtual_network = virtual_network

        # Initialize number of epochs
        self._N = 0

    def policy(self, state, sender, reciever) -> int:
        """ Compute the shortest path and the action is the node right after the source.
        Returns:
            The action.
        """
        
        try:
            path = nx.shortest_path(state, source=sender, target=reciever, weight=None, method='dijkstra')
            return path[1]
        except:
            return sender

    def _run(self, state, sender, reciever, reward):

        action = self.policy(state, sender, reciever)

        return action
