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

from agents.agent import Agent

class SARSAAgent(Agent):
    """
    State–action–reward–state–action (SARSA) Agent
    """

    def __init__(self,
                 physical_network: object,
                 virtual_network: object,
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
        n = len(self._edges)
        possible_states = [tuple([int(j) for j in '{:0{}b}'.format(i, n)]) for i in range(2**n)]
        self._Q = {}
        #for r in range(self._size):
        for r in list(self._virtual_network.nodes()):
            self._Q[r] = {}
            #for s in range(self._size):
            for s in list(self._virtual_network.nodes()):
                if s != r:
                    self._Q[r][s]={}
                    for n in list(self._virtual_network.neighbors(s)):
                        self._Q[r][s][n]={}
                        for state in possible_states:
                            self._Q[r][s][n][state]=0

        # Initialize number of epochs
        self._N = 0

    def Qindex(self, state):

        tup =  []
        edges = state.edges()
        for i,e in enumerate(self._edges):
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
                Q[n] =  self._Q[reciever][sender][n][ind]
            return max(Q)
        else:  
            return random.choice(neighbors)

    def _run(self, state, sender, reciever, reward):

        action = self.policy(state, sender, reciever)

        if self._N > 0:
            ind = self.Qindex(state)

            self._Q[reciever][sender][action][ind] += self._alpha * (reward + self._gamma * self._Q[self._lastreciever][self._lastsender][self._lastaction][self.Qindex(self._laststate)] - self._Q[reciever][sender][action][ind])

        self._N += 1
        self._lastsender = sender
        self._lastreciever = reciever
        self._lastaction = action
        self._laststate = state

        return action
