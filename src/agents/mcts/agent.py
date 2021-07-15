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
Monte Carlo Tree Search Simulation for Quantum Internet Network Routing.
"""

import networkx as nx
from networkx.classes import Graph

import random
from networkx.classes.function import neighbors
import numpy as np

from agents.agent import Agent
from agents.mcts.tree import MCtree

from environements.random import RandomEnvironement


class MCTSAgent(Agent):
    """
    Monte Carlo Tree Search Simulation. It simulates many possible evolution of the network. Finally it selects the action with best expected reward (highest Q function).
    """

    def __init__(self,
                 physical_network: Graph,
                 virtual_network: Graph,
                 prob_dist: np.Array,
                 N: int = 1000,
                 c: float = 2) -> None:
        """
        Args:
            physical_network: classical network.
            virtual_network: initial quantum network.
            prob_dist: probability distribution on how the environement select sender/reciever.
            N: number of MC simulation.
            c: coeffcient for the UCB1 score.
        """
        
        # Get parameters
        self._physical_network = physical_network
        self._virtual_network = virtual_network
        self._prob_dist = prob_dist
        self._N = N
        self._c = c

        # Initialize Monte Carlo tree and current node
        self._tree = MCtree(init_state=self._virtual_network, c = self._c)
        self._curr = 1
    
    def rollout(self, state: Graph, sender: int) -> float:
        """ Simulate a random routing until network refresh. Return the obtained reward."""

        env = RandomEnvironement(physical_network = self._physical_network, 
                                virtual_network = state,
                                prob_dist = self._prob_dist)

        reward = 0 
        refresh = False
        while True:
            if refresh:
                return reward
            
            action = random.choice(list(state.neighbors(sender)))
            result = env.run(action= action)

            reward += result.reward
            state = result.state
            sender = result.sender
            refresh = result.refresh
    
    def expand(self, state: Graph, node: int) -> None:
        """ Expand the Monte Carlo tree"""
        neighbors = list(state.neighbors(node))
        states = [state.copy().remove_edge(node,n) for n in neighbors]
        self._tree.expand(node=node, N=len(neighbors), states=states, actions=neighbors)
        return None

    def policy(self) -> int:
        """ Select the action with best expected reward (highest Q function).
        Returns:
            The action.
        """
        
        states_ind = self._tree.successors(1)
        Q = {}
        for s in states_ind:
            Q[s]= self._tree.Q(s)

        return self._tree.action(max(Q))

    def _run(self, state: Graph, sender: int, reciever: int, reward: float):

        for __ in range(self._N):
            if not self._tree.is_leaf(self._curr):
                succ = self._tree.successors(self._curr)
                ucb1 = [self._tree.ucb1(n) for n in succ]
                self._curr = succ[ucb1.index(max(ucb1))]

            if self._tree.count(self._curr) == 0:
                self.expand(self._curr)
                self._curr = self._tree.successors(self._curr)[0]

            mc_reward = self.rollout(state, sender)
            self._tree.backup(self._curr, mc_reward)

        action = self.policy()

        return action
