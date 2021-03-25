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
                 classical_network: List[List[float]],
                 quantum_network: List[List[float]]) -> None:
        self['classical_network'] = classical_network
        self['quantum_init_network'] = quantum_network
        self['quantum_network_status'] = quantum_network

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
        if state is None or action is None:
            raise ValueError("A State and an Action "
                            "must be supplied to run the environement.")
        return self._run()

    @abstractmethod
    def _run(self) -> Dict:
        raise NotImplementedError()

    @property
    def classical_network(self) -> Optional[List[List[float]]]:
        """ Returns classical network. """
        return self.classical_network

    @classical_network.setter
    def classical_network(self, value: List[List[float]]) -> None:
        """ Sets classical network. """
        self['classical_network'] = value

    @property
    def quantum_network_status(self) -> Optional[List[List[float]]]:
        """ Returns current quantum network status. """
        return self.quantum_network_status

    @quantum_network_status.setter
    def quantum_network_status(self, value: List[List[float]]) -> None:
        """ Sets current quantum network status. """
        self['quantum_network_status'] = value

    @property
    def quantum_init_network(self) -> Optional[List[List[float]]]:
        """ Returns initial quantum network. """
        return self.quantum_init_network

    @quantum_init_network.setter
    def quantum_init_network(self, value: List[List[float]]) -> None:
        """ Sets initial quantum network. """
        self['quantum_init_network'] = value

class QuantumInternetNetworkResult(ABC):
    """ QuantumInternetNetworkResult."""

    def __init__(self):
        super().__init__()

    @property
    def state(self) -> object:
        """ return current state"""
        return self.state

    @state.setter
    def state(self, value: object) -> None:
        """ set estimations values """
        self['state'] = value

    @property
    def reward(self) -> float:
        """ return reward"""
        return self.reward

    @reward.setter
    def state(self, value: float) -> None:
        """ set reward value """
        self['reward'] = value

    @property
    def sender(self) -> int:
        """ return sender's index"""
        return self.sender

    @sender.setter
    def sender(self, value: int) -> None:
        """ set sender's index"""
        self['sender'] = value

    @property
    def reciever(self) -> object:
        """ return reciever's index"""
        return self.reciever

    @state.setter
    def reciever(self, value: object) -> None:
        """ set reciever's index"""
        self['reciever'] = value

    