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

import networkx as nx

from script.envs.random import RandomEnvironement
from script.agents.random import RandomNeighborsAgent

_available_environements = [
    "random",
    ]

_available_agents = [
    "random",
    ]

def main(args):

    n = 10
    m = 2*n
    C = nx.cycle_graph(n)
    Q = nx.nx.gnm_random_graph(n,m)

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
    parser.add_argument("--physical_network", type=int, default=10)
    parser.add_argument("--virtual_network", type=int, default=10)

    # Experiments
    parser.add_argument("--epochs", type=int, default=200)

    # Save data
    parser.add_argument("--path", nargs=1, default=os.getcwd())

    args = parser.parse_args()
    main(args)