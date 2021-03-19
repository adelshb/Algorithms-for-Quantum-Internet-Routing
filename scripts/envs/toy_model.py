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
Toy Environement for Quantum Internet Network.
"""

from typing import Optional, Union, List, Callable, Dict, Tuple
import random

from qin import QuantumInternetNetwork
from envs_utils import active_nodes

class ToyEnvironement(QuantumInternetNetwork):
    """Toy Environement for Quantum Internet Network."""

    def __init__(self,
                 classical_network: List[List[float]],
                 quantum_network: List[List[float]],
                 state: List[List[float]],
                 action: Tuple,
                 sender: int,
                 reciever: int) -> None:
        """
        Args:
            classical_network: classical network
            quantum_network: initial quantum network
            state: current status of the quantum network
            action: tuple corresponding the to edge to use
        """

        self._classical_network = classical_network
        self._quantum_network = quantum_network
        self._state = state
        self._action = action
        self._sender = sender
        self._reciever = reciever

        self._active_nodes = active_nodes(self._state)


    def reward(self) -> float:
        """ Compute the reward.
        Returns:
            The reward.
        """

        ###

        #TODO

        ###

        return #rew

    def event(self) -> (int, int):
        """ Generate an event. Generate a sender and a reciever. They are selected randomly.
        Returns:
            Vertices label of the sender and reciver.
        """

        nodes = self._active_nodes
        s = random.choice(nodes)
        r = random.choice(nodes.remove(s))
        return (s, r)

    def _run(self
        ) ->  Union[List[List[float]], float]:

        #new_state = 
        #rew = self.reward()

        if self._sender == self._reciever:
            self._sender, self._reciever = self.event()

        return #[new_state, rew]