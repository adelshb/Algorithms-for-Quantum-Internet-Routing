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
State–action–reward–state–action (SARSA) Agent for Quantum Internet Network Routing.
"""

import random

from networkx.classes import Graph
from agents.agent import Agent

class SARSAAgent(Agent):
    """
    State–action–reward–state–action (SARSA) Agent
    """

    def __init__(self,
                 physical_network: Graph,
                 virtual_network: Graph,
                 epsilon: float,
                 alpha: float,
                 gamma: float) -> None:
        """
        Args:
            physical_network: classical network
            virtual_network: initial quantum network
        """
        
        # Get parameters
        self._physical_network = physical_network
        self._virtual_network = virtual_network
        self._edges = list(self._virtual_network.edges())
        self._size = max(list(self._virtual_network.nodes())+ list(self._physical_network.nodes()))+1
        self._epsilon = epsilon
        self._alpha = alpha
        self._gamma = gamma

        # Initialize Q function
        self._Q = {}
        self._N = 0

    def Qindex(self, state):

        tup =  []
        edges = state.edges()
        for e in self._edges:
            if e in edges:
                tup.append(1)
            else:
                tup.append(0)
        return tuple(tup)

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
        
        if random.random() < (1 - self._epsilon):
            ind = self.Qindex(state)
            Q = {}
            for n in neighbors:
                try:
                    Q[n] =  self._Q[reciever][sender][n][ind]
                except:
                    pass
                    #Q[n] = 0
            try:
                max(Q) 
            except:
                return random.choice(neighbors)
        else:  
            return random.choice(neighbors)

    def _run(self, state, sender, reciever, reward):

        action = self.policy(state, sender, reciever)
        ind = self.Qindex(state)

        if self._N > 0:

            if reciever not in self._Q:
                self._Q[reciever] = {}
            if sender not in self._Q[reciever]:
                self._Q[reciever][sender] = {}
            if action not in self._Q[reciever][sender]:
                self._Q[reciever][sender][action] = {}
            if ind not in self._Q[reciever][sender][action]:
                self._Q[reciever][sender][action][ind] = 0

            self._Q[reciever][sender][action][ind] += self._alpha * (reward + self._gamma * self._Q[self._lastreciever][self._lastsender][self._lastaction][self.Qindex(self._laststate)] - self._Q[reciever][sender][action][ind])
        elif self._N == 0:
            self._Q[reciever] = {}
            self._Q[reciever][sender] = {}
            self._Q[reciever][sender][action] = {}
            self._Q[reciever][sender][action][ind] = 0

        self._N += 1
        self._lastsender = sender
        self._lastreciever = reciever
        self._lastaction = action
        self._laststate = state.copy()

        return action
