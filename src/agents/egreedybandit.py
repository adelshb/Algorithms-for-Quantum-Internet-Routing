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
Epsilon-Greddy Bandit Algorithm.
"""
from typing import Optional

import random

from agents.agent import Agent

class EGreedyBanditAgent(Agent):
    """
    Bandit Agent
    """

    def __init__(self,
                 physical_network: object,
                 virtual_network: object,
                 epsilon: float) -> None:
        """
        Args:
            physical_network: classical network
            virtual_network: initial quantum network
        """
        
        # Get parameters
        self._physical_network = physical_network
        self._virtual_network = virtual_network
        self._epsilon = epsilon

        # Initialize average return
        self._r = {}
        for tup in list(self._virtual_network.edges()):
            self._r[tup] = 0
        # Initialize number of epochs
        self._N = 0

    def policy(self, state, sender, reciever) -> int:
        """ Select the neighboor with maximum average reward with probability (1-epsilon). Othwerwise send a random neighboor.
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
        
        if random.random() < (1 - self._epsilon):
            r = {}
            for key in self._r.keys():
                if sender == key[0] or sender == key[1]:
                    r[key] = self._r[key]
            tup = max(r)
            if sender == tup[0]:
                return tup[1]
            else:
                return tup[0]
        else:  
            return random.choice(neighbors)

    def _run(self, state, sender, reciever, reward):

        if self._N > 0:
            self._r[self._lastaction] += (reward - self._r[self._lastaction])/self._N

        action = self.policy(state, sender, reciever)
        self._N += 1 
        if sender < action:
            self._lastaction = (sender, action)
        else:
            self._lastaction = (action, sender)
        return action
