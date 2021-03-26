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
from typing import Union, Dict, Optional, Tuple, List


class QuantumInternetNetwork(ABC):
    """
    Base class for Quantum Internet Network.

    This method should initialize the module and use an exception if a component of the module is available.
    """
    @abstractmethod
    def __init__(self,
                 physical_network: List[List[float]],
                 virtual_network: List[List[float]]) -> None:
        self['physical_network'] = physical_network
        self['virtual_init_network'] = virtual_network
        self['virtual_network_status'] = virtual_network

    def run(self, action: int):
        """Execute the policy with selected Environement for given State and Action.

        Args:
            action: Action decided by the policy.
        Returns:
            state_end: State an environement.
            reward: reward for the Agent.
        Raises:
            ValueError: If the State or the Action has not been provided
        """
        if action is None:
            raise ValueError("An Action "
                            "must be supplied to run the environement.")
        return self._run(action)

    @abstractmethod
    def _run(self, action: int) -> Dict:
        raise NotImplementedError()

    @property
    def physical_network(self) -> Optional[List[List[float]]]:
        """ Returns physical network. """
        return self.physical_network

    @physical_network.setter
    def physical_network(self, value: List[List[float]]) -> None:
        """ Sets physical network. """
        self['physical_network'] = value

    @property
    def virtual_network_status(self) -> Optional[List[List[float]]]:
        """ Returns current virtual network status. """
        return self.virtual_network_status

    @virtual_network_status.setter
    def virtual_network_status(self, value: List[List[float]]) -> None:
        """ Sets current virtual network status. """
        self['virtual_network_status'] = value

    @property
    def virtual_init_network(self) -> Optional[List[List[float]]]:
        """ Returns initial virtual network. """
        return self.virtual_init_network

    @virtual_init_network.setter
    def virtual_init_network(self, value: List[List[float]]) -> None:
        """ Sets initial virtual network. """
        self['virtual_init_network'] = value

class QuantumInternetNetworkResult(ABC):
    """ QuantumInternetNetworkResult."""

    def __init__(self):
        super().__init__()

    @property
    def state(self) -> object:
        """ return current state"""
        return self._state

    @state.setter
    def state(self, value: object) -> None:
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
    def reciever(self) -> object:
        """ return reciever's index"""
        return self._reciever

    @state.setter
    def reciever(self, value: object) -> None:
        """ set reciever's index"""
        self._reciever = value

    
