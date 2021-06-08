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
Random Agent for Quantum Internet Network Routing.
"""

#from typing import List, Dict
import random

from agents.agent import Agent

class RandomNeighborsAgent(Agent):
    """
    Agent that selects a random neighbor of the sender. 
    If the reciever and sender are neighboors, the reciever will be picked. 
    If the sender has no neighbor at the current state, a random neighboor
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
        self._physical_network = physical_network
        self._virtual_network = virtual_network

    def policy(self, state, sender, reciever) -> int:
        """ Compute the action.
        Returns:
            The action.
        """
        
        # Collect sender's neighbors on current state
        neighbors = list(state.neighbors(sender))

        if not neighbors:
            # If the sender has no neighbor on the current state collect sender's neighbors on initial virtual netwok
            neighbors = list(self._virtual_network.neighbors(sender))
            if not neighbors:
                raise Exception('The sender has no neighbor.')
            else:
                # Pick a random neighbor from initial virtual network. This will cause a refresh of one/some/all link(s).
                return random.choice(neighbors)
        elif reciever in neighbors:
            return reciever
        else:
            return random.choice(neighbors)

    def _run(self, state, sender, reciever, reward):

        action = self.policy(state, sender, reciever)

        return action
