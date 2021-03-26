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

from typing import List, Dict
import random

from script.envs.qin import QuantumInternetNetwork, QuantumInternetNetworkResult
#from envs_utils import active_nodes

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
        print("Loading initial parameters...")
        self._physical_network = physical_network
        self._virtual_network = virtual_network
        self._state = virtual_network
        self._sender, self._reciever = self.gsr_event() 

    def compute_reward(self, refresh) -> float:
        """ Compute the reward.
        Returns:
            The reward.
        """

        if refresh:
            return -100
        else:
            return 1

    def gsr_event(self) -> (int, int):
        """ Generate a sender reciever event. Generate a sender and a reciever. They are selected randomly.
        Returns:
            Vertices label of the sender and reciver.
        """

        nodes = list(self._state.nodes)
        s = random.choice(nodes)
        nodes.remove(s)
        r = random.choice(nodes)
        return s, r

    def _run(self,
        action: int) ->  Dict:

        refresh = False

        # Check if there is a current sender and reciever. Likely to be used as initialization.
        if self._sender == None or self._reciever == None:
            self._sender, self._reciever = self.gsr_event()
            raise Exception('No sender and/or reciever')
        
        # Evolution to the new state.
        if self._state.has_edge(self._sender, action):
            self._state.remove_edge(self._sender, action)
            self._sender = action
        elif self._virtual_network.has_edge(self._sender, action):
            self.refresh()
            refresh = True
        else:
            raise Exception('Selected action not possible. There is no edge between the two nodes')

        # Compute the reward.
        rew = self.compute_reward(refresh)

        # Check if the sender reached the reciever.
        if self._sender == self._reciever:
            self._sender, self._reciever = self.gsr_event() 

        result = QuantumInternetNetworkResult()
        result.state = self._state
        result.reward = rew 
        result.sender = self._sender
        result.reciever = self._reciever

        return result
