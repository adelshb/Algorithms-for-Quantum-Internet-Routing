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
Greedy Neighbors Algorithm for Quantum Internet Network Routing proposed in https://arxiv.org/abs/1907.11630.
"""

from src.agents.agent import Agent
import networkx as nx

class GreedyNeighborsAgent(Agent):
    """
    Class for Greedy Neighbors Agent.
    """

    def __init__(self,
                 physical_network: object,
                 virtual_network: object) -> None:
        """
        Args:
            physical_network: classical network
            virtual_network: initial quantum network
        """
        
        # Get parameters
        print("Loading initial parameters...")
        self._physical_network = physical_network
        self._virtual_network = virtual_network

    def policy(self, state, sender, reciever) -> int:
        """ Compute the action.
        Returns:
            The action.
        """
        
        curr = sender    
        minm = self._physical_network.number_of_nodes()

        for v in state.neighbors(curr):
            temp_dist = nx.shortest_path_length(self._physical_network, v, reciever)      
            if temp_dist < minm:
                minm = temp_dist
                temp_curr = v
            curr = temp_curr    
        return curr

    def _run(self, state, sender, reciever, reward):
        action = self.policy(state, sender, reciever)
        return action
