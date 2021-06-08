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
This module implements the abstract base class for quantum internet network modules.
"""

from abc import ABC, abstractmethod
from typing import Dict

from networkx.classes import Graph

class QuantumInternetNetwork(ABC):
    """
    Base class for Quantum Internet Network.

    This method should initialize the module and use an exception if a component of the module is available.
    """
    @abstractmethod
    def __init__(self,
                 physical_network: Graph,
                 virtual_network: Graph) -> None:

        self._physical_network = physical_network
        self._virtual_init_network = virtual_network
        self._virtual_network_state = virtual_network.copy()

    def run(self, action: int):
        """Execute the evolution with selected Environement for given State and Action.

        Args:
            action: Action decided by the policy.
        Returns:
            state_end: State an environement.
            reward: reward for the Agent.
        Raises:
            ValueError: If the Action has not been provided
        """
        if action is None:
            raise ValueError("An Action "
                            "must be supplied to run the environement.")
        return self._run(action)

    @abstractmethod
    def _run(self, action: int) -> Dict:
        raise NotImplementedError()

    @property
    def physical_network(self) -> Graph:
        """ Returns physical network. """
        return self._physical_network

    @physical_network.setter
    def physical_network(self, value: Graph) -> None:
        """ Sets physical network. """
        self._physical_network = value

    @property
    def virtual_network_state(self) -> Graph:
        """ Returns current virtual network state. """
        return self._virtual_network_state

    @virtual_network_state.setter
    def virtual_network_state(self, value: Graph) -> None:
        """ Sets current virtual network state. """
        self._virtual_network_state = value

    @property
    def virtual_init_network(self) -> Graph:
        """ Returns initial virtual network. """
        return self._virtual_init_network

    @virtual_init_network.setter
    def virtual_init_network(self, value: Graph) -> None:
        """ Sets initial virtual network. """
        self._virtual_init_network = value

class QuantumInternetNetworkResult(ABC):
    """ QuantumInternetNetworkResult."""

    def __init__(self):
        super().__init__()

    @property
    def state(self) -> Graph:
        """ return current state"""
        return self._state

    @state.setter
    def state(self, value: Graph) -> None:
        """ set estimations values """
        self._state = value

    @property
    def reward(self) -> float:
        """ return reward"""
        return self._reward

    @reward.setter
    def reward(self, value: float) -> None:
        """ set reward value """
        self._reward = value

    @property
    def sender(self) -> int:
        """ return sender's index"""
        return self._sender

    @sender.setter
    def sender(self, value: int) -> None:
        """ set sender's index"""
        self._sender = value

    @property
    def reciever(self) -> int:
        """ return reciever's index"""
        return self._reciever

    @reciever.setter
    def reciever(self, value: int) -> None:
        """ set reciever's index"""
        self._reciever = value

    
