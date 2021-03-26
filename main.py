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
import os 

from script.envs.random import RandomEnvironement
import networkx as nx

_available_environements = [
    "random",
    ]

_available_agents = [
    "random",
    ]

def main(args):

    n = 10
    m = 5
    C = nx.cycle_graph(n)
    Q = nx.nx.gnm_random_graph(n,m)

    env = RandomEnvironement(classical_network = C, quantum_network = Q)


if __name__ == "__main__":
    parser = ArgumentParser()

    # Environement
    parser.add_argument("--environement", type=str, default="random", choices=_available_environements)

    # Agent
    parser.add_argument("--agent", type=str, default="random", choices=_available_agents)

    # Networks 
    parser.add_argument("--physical_network", type=int, default=10)
    parser.add_argument("--virtual_network", type=int, default=10)

    # Save data
    parser.add_argument("--path", nargs=1, default=os.getcwd())

    args = parser.parse_args()
    main(args)