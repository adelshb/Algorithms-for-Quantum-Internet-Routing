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
Random Environement for Quantum Internet Network.
"""

from typing import List, Dict, Tuple
import random

import networkx as nx

from src.environements.qin import QuantumInternetNetwork, QuantumInternetNetworkResult

class RandomEnvironement(QuantumInternetNetwork):
    """Random Events Environement for Quantum Internet Network."""

    def __init__(self,
                 physical_network: object,
                 virtual_network: object,
                 ) -> None:
        """
        Args:
            physical_network: classical network
            virtual_network: initial quantum network
        """
        
        # Get parameters
        self._physical_network = physical_network
        self._virtual_network = virtual_network
        self._state = virtual_network.copy()
        self._sender, self._reciever = self.gsr_event() 

    def compute_reward(self, refresh, success) -> float:
        """ Compute the reward.
        Returns:
            The reward.
        """

        if refresh:
            return -10
        elif success:
            return 10
        else:
            return 1

    def gsr_event(self) -> Tuple[int, int]:
        """ Generate a sender reciever event. Generate a sender and a reciever. They are selected randomly.
        Returns:
            Vertices label of the sender and reciver.
        """

        paths = []
        # Generate all simple paths with cutoff |V|
        nodes = list(self._physical_network.nodes)
        for n in nodes:
            nodes.remove(n)
            paths.append(list(nx.all_simple_paths(self._physical_network, source=n, target=nodes)))
        paths = [j for i in paths for j in i]
        
        # Randmly select a path and select sender/reciever
        path = random.choice(paths)
        return path[0], path[-1]

        # paths = []
        # while not paths:

        # # Generate all simple paths with cutoff |V|
        #     #nodes = list(self._state.nodes)
        #     nodes = list(self._physical_network.nodes)
        #     for n in nodes:
        #         nodes.remove(n)
        #         paths.append(list(nx.all_simple_paths(self._physical_network, source=n, target=nodes, cutoff=self._physical_network.number_of_nodes())))
        #     paths = [j for i in paths for j in i]
        #     print("#########PATHS",paths)
        #     print("#########PATHS",self._physical_network.edges)
        #     try:
        #         # Randmly select a path and select sender/reciever
        #         path = random.choice(paths)
        #         return path[0], path[-1]
        #     except:
        #         self._state = self._virtual_network.copy()        
            
    def _run(self,
        action: int) ->  Dict:

        refresh = False
        success = False

        # Check if there is a current sender and reciever. Likely to be used as initialization.
        if self._sender == None or self._reciever == None:
            self._sender, self._reciever = self.gsr_event()
            raise Exception('No sender and/or reciever')
        
        # Evolution to the new state.
        if self._state.has_edge(self._sender, action):
            self._state.remove_edge(self._sender, action)
            self._sender = action
        elif self._sender == action:
            self._state = self._virtual_network.copy()
            refresh = True
        elif self._virtual_network.has_edge(self._sender, action):
            self._state = self._virtual_network.copy()
            refresh = True
        else:
            raise Exception('Selected action not possible. There is no edge between the two nodes')

        # Check if the sender reached the reciever.
        if self._sender == self._reciever:
            self._sender, self._reciever = self.gsr_event()
            success = True
        
        # Compute the reward.
        rew = self.compute_reward(refresh, success)

        result = QuantumInternetNetworkResult()
        result.state = self._state.copy()
        result.reward = rew 
        result.sender = self._sender
        result.reciever = self._reciever
        
        return result
