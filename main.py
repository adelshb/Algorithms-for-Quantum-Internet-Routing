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

"""Wrapper for Environement and Agent."""

from argparse import ArgumentParser
from tqdm import tqdm
import os 
import yaml

import networkx as nx

from environements.random import RandomEnvironement
from agents.random import RandomNeighborsAgent
from networks.cycle import cycle_net

_available_environements = [
    "random",
    ]

_available_agents = [
    "random",
    ]

_available_networks = [
    "cycle",
    ]

def main(args):

    # Generate cycle network
    C, Q = cycle_net(n= args.network_param.n, dth = args.network_param.dth)

    # Initialize the Environement, the different parameters and the Agent
    env = RandomEnvironement(physical_network = C, 
                                virtual_network = Q)
    state = env._state
    sender = env._sender
    reciever = env._reciever
    agent = RandomNeighborsAgent(physical_network = C, 
                                    virtual_network = Q)

    R = 0
    for __ in tqdm(range(args.epochs)):
        # Compute action through Agent's policy
        action = agent.run(state= state, sender= sender, reciever= reciever)
        
        # State evolution and compute reward
        result = env.run(action= action)
        
        # Update parameters
        state = result.state
        sender = result.sender
        reciever = result.reciever
        
        R += result.reward

    print("The accumulated reward is: ", R)


if __name__ == "__main__":
    parser = ArgumentParser()

    # Environement
    parser.add_argument("--environement", type=str, default="random", choices=_available_environements)

    # Agent
    parser.add_argument("--agent", type=str, default="random", choices=_available_agents)

    # Networks 
    parser.add_argument("--network", type=str, default="cycle", choices=_available_networks)
    parser.add_argument("--network_param", type=yaml.load, default="{n: 10, dth: 2}")

    # Experiments
    parser.add_argument("--epochs", type=int, default=200)

    # Save data
    parser.add_argument("--path", nargs=1, default=os.getcwd())

    args = parser.parse_args()
    main(args)
