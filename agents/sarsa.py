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
import itertools

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
        self._size = max(list(self._virtual_network.nodes())+ list(self._physical_network.nodes()))
        self._alpha = alpha
        self._gamma = gamma

        # Initialize Q function
        possible_states = sum([list(itertools.permutations( [0]*n + [1]*(self._size - n))) for n in range(self._size+1)])
        self._Q = {}
        for r in range(self._size):
            Q[r] = {}
            for s in range(self._size):
                if s != r:
                    Q[r][s]={}
                    neigh = list(self._virtual_network.neighbors(s))
                    for n in neigh:
                        Q[r][s][n]={}
                        for state in possible_states:
                            Q[r][s][n][state]=0

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
                print(sender)
                raise Exception('The sender has no neighbor.')
        
        if random.random() < (1 - self._epsilon):
            ind = self.Qindex(state)
            Q = {}
            for n in neighbors:
                Q[n] =  Q[reciever][sender][n][ind]
            tup = max(Q)
            if sender == tup[0]:
                return tup[1]
            else:
                return tup[0]
        else:  
            return random.choice(neighbors)

        return action

    def _run(self, state, sender, reciever, reward):
            

        action = self.policy(state, sender, reciever)

        if self._N > 0:
            ind = self.Qindex(state)
            Q[reciever][sender][action][ind] += self._alpha * (reward + self._gamma * Q[reciever][sender][self._lastaction][self.Qindex(self._laststate)] - Q[reciever][sender][action][ind])

        self._N += 1 
        self._lastaction = action
        self._laststate = state

        return action
