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

from networkx.classes import Graph
from agents.agent import Agent

class RandomNeighborsAgent(Agent):
    """
    Description here
    """

    def __init__(self,
                 physical_network: Graph,
                 virtual_network: Graph) -> None:
        """
        Args:
            physical_network: classical network
            virtual_network: initial quantum network
        """
        
        # Get parameters
        self._physical_network = physical_network
        self._virtual_network = virtual_network

        # Initialize number of epochs
        self._N = 0

    def policy(self, state, sender, reciever) -> int:
        """ Compute the action.
        Returns:
            The action.
        """
        
        ##
        # TO DO HERE # 
        ##
        return action

    def _run(self, state, sender, reciever, reward):

        action = self.policy(state, sender, reciever)

        return action
