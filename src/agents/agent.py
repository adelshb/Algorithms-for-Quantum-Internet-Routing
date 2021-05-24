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
This module implements the abstract base class for agent modules.
"""

from abc import ABC, abstractmethod
from typing import Union, Dict, Optional, Tuple, List


class Agent(ABC):
    """
    Base class for Agent.

    This method should initialize the module and use an exception if a component of the module is available.
    """
    @abstractmethod
    def __init__(self,
                 physical_network: object,
                 virtual_network: object) -> None:
        self._physical_network = physical_network
        self._virtual_init_network = virtual_network

    def run(self, state: object, sender: int, reciever: int, reward: Optional[float]= None):
        """Execute the policy with selected Environement for given State and Action.
        Args:
            state: current state of the virtual network.
            sender: sender node.
            reciever: reciever node.
        Returns:
            action: action decided by the Agent
        Raises:
            ValueError: If the State or the Action has not been provided
        """
        if sender is None or reciever is None:
            raise ValueError("A sender and/or a reciever"
                            "must be supplied to run the agent.")
                            
        return self._run(state, sender, reciever, reward)

    @abstractmethod
    def _run(self, state: object, sender: int, reciever: int, reward: Optional[float]=None) -> int:
        raise NotImplementedError()

    @property
    def physical_network(self) -> Optional[List[List[float]]]:
        """ Returns physical network. """
        return self._physical_network

    @physical_network.setter
    def physical_network(self, value: List[List[float]]) -> None:
        """ Sets physical network. """
        self._physical_network = value

    @property
    def virtual_init_network(self) -> Optional[List[List[float]]]:
        """ Returns initial virtual network. """
        return self._virtual_init_network

    @virtual_init_network.setter
    def virtual_init_network(self, value: List[List[float]]) -> None:
        """ Sets initial virtual network. """
        self._virtual_init_network = value
