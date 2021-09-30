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

from typing import Optional, List, Tuple
from networkx.classes import Graph

import random
from numpy import ndarray

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
                 rollout_epochs: int = 30,
                 sender_reciever_events: Optional[List[Tuple]] = None,
                 prob_dist: Optional[ndarray] = None,
                 N: Optional[int] = 1000,
                 c: Optional[float] = 2) -> None:
        """
        Args:
            physical_network: classical network.
            virtual_network: initial quantum network.
            sender_reciever_events: list of sender-reciever events. If None, will generate randomly accordingly to the prob_dit input.
            prob_dist: probability distribution on how the environement select sender/reciever.
            N: number of MC simulation.
            c: coeffcient for the UCB1 score.
        """
        
        # Get parameters
        self._physical_network = physical_network
        self._virtual_network = virtual_network
        self._rollout_epochs = rollout_epochs
        self._sr_events = sender_reciever_events
        self._prob_dist = prob_dist
        self._N = N
        self._c = c

        self._sr_event_count = 0
    
    def rollout(self, state: Graph, sender: int) -> float:
        """ Simulate a random routing until network refresh. Return the obtained reward."""

        if self._sr_events==None:
            # env = RandomEnvironement(physical_network = self._physical_network, 
            #                             virtual_network = state,
            #                             prob_dist = self._prob_dist)

            env = RandomEnvironement(physical_network = self._physical_network, 
                                        virtual_network = state)

        else:
            sr_events = self._sr_events[self._sr_event_count:]
            sr_events[0] = (sender, self._sr_events[self._sr_event_count][1])

            

            env = RandomEnvironement(physical_network = self._physical_network,
                                virtual_network = state,
                                sender_reciever_events= sr_events)

        # reward = 0 
        # refresh = False
        # while True:
        #     neighbors = list(state.neighbors(sender))
        #     if refresh or not neighbors:
        #         print(neighbors, reward)
        #         return reward
            
        #     action = random.choice(neighbors)
        #     result = env.run(action=action)

        #     reward += result.reward
        #     state = result.state
        #     sender = result.sender
        #     refresh = result.refresh

        # env = RandomEnvironement(physical_network = self._physical_network,
        #                     virtual_network = state,
        #                     sender_reciever_events= self._sr_events[self._sr_event_count:])
        env = RandomEnvironement(physical_network = self._physical_network,
                            virtual_network = state)

        reward = 0 
        for __ in range(self._rollout_epochs):

            neighbors = list(state.neighbors(sender))
            if not neighbors:
                action = sender
            else:
                action = random.choice(neighbors)

            result = env.run(action= action)

            reward += result.reward
            state = result.state
            sender = result.sender
        # print(reward)
        return reward
    
    def expand(self, state: Graph, sender: int, node:int) -> None:
        """ Expand the Monte Carlo tree"""
        neighbors = list(state.neighbors(sender))
        states = [state.copy().remove_edge(sender,n) for n in neighbors]
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
        return self._tree.action(max(Q, key=Q.get))

    def _run(self, state: Graph, 
                sender: int, 
                reciever: int, 
                reward: float, 
                success: Optional[bool]=False):

        if success:
            self._sr_event_count += 1

        neighbors = list(state.neighbors(sender))
        if reciever in neighbors:
            return reciever
        elif len(neighbors)==0:
            return sender

        # Initialize Monte Carlo tree and current node
        self._tree = MCtree(init_state=state, c= self._c)

        for __ in range(self._N):
            self._curr = 1
            while not self._tree.is_leaf(self._curr):
                succ = self._tree.successors(self._curr)
                ucb1 = [self._tree.ucb1(n) for n in succ]
                self._curr = succ[ucb1.index(max(ucb1))]

            if not self._tree.count(self._curr) == 0:
                if self._curr !=1:
                    neighbors = list(state.neighbors(self._tree.action(self._curr)))
                if len(neighbors)>0:
                    self.expand(state, sender, self._curr)
                    self._curr = self._tree.successors(self._curr)[0]

            mc_reward = self.rollout(state, sender)
            self._tree.backup(self._curr, mc_reward)

        action = self.policy()

        return action