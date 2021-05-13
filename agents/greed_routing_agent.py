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
Template Agent for Quantum Internet Network Routing.
"""

#from typing import List, Dict
import random

from agents.agent import Agent
import networkx as nx

class GreedyNeighborsAgent(Agent):
    """
    Description here
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
        Gphys = self._physical_network
        Gver  = state
        curr = sender
        n = Gphys.number_of_nodes()
    
        minm = n
        for v in Gver.neighbors(curr):
            temp_dist = nx.shortest_path_length(Gphys, v, reciever)
            
            if temp_dist < minm:
                minm = temp_dist
                temp_curr = v
            curr = temp_curr
            
            
        print(Gver.edges(sender))
        print(sender)
        print(curr)
        print(reciever)
        print(minm)
        print(self._virtual_network.edges())
        

        
        
        return curr

    def _run(self, state, sender, reciever, reward):

        action = self.policy(state, sender, reciever)

        return action
