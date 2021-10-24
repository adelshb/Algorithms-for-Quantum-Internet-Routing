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

"""Benchmark of different Agents"""

from argparse import ArgumentParser

import numpy as np
import random
import networkx as nx

from networks.cycle import cycle_net

from environements.random import RandomEnvironement

from agents.mcts.agent import MCTSAgent
from agents.greed_routing_agent import GreedyNeighborsAgent
from agents.shortest_path import ShortestPathAgent

def main(args):
    
    # Preparing the benchmark settings
    C, Q = cycle_net(n=args.n, dth=args.dth)

    paths = []
    nodes = list(C.nodes)
    for n in nodes:
        nodes.remove(n)
        for t in nodes:
            try:
                paths.append(list(nx.all_simple_paths(C, source=n, target=t)))
            except:
                pass
    paths = [j for i in paths for j in i]

    v = np.random.rand(len(paths))
    prob_dist = v / np.linalg.norm(v)

    sr_events = []
    for __ in range(100):
        path = random.choices(paths, prob_dist)[0]
        sr_events.append((path[0], path[-1]))


    # MCTS
    env = RandomEnvironement(physical_network = C, 
                                virtual_network = Q,
                                sender_reciever_events= sr_events)

    agent = MCTSAgent(physical_network= C,
                     virtual_network = Q,
                     N = args.mcts_sim_num,
                     c = args.c_ucb1)

    R = run_experiment(env, agent, epochs=args.epochs)
    print("MCTS (no knowledge): ", R[-1])

    # MCTS with Schedule
    env = RandomEnvironement(physical_network = C, 
                                    virtual_network = Q,
                                    sender_reciever_events= sr_events)

    agent = MCTSAgent(physical_network= C,
                    virtual_network = Q,
                    sender_reciever_events= sr_events,
                    N = args.mcts_sim_num,
                    c = args.c_ucb1)

    R = run_experiment(env, agent, epochs=args.epochs)
    print("MCTS (schedule knowledge): ", R[-1])

    # Greedy
    env = RandomEnvironement(physical_network = C, 
                                    virtual_network = Q,
                                    sender_reciever_events= sr_events)

    agent = GreedyNeighborsAgent(physical_network= C,
                    virtual_network = Q)

    R = run_experiment(env, agent, epochs=args.epochs)
    print("Greedy: ", R[-1])

    # Shortest Path
    env = RandomEnvironement(physical_network = C, 
                                    virtual_network = Q,
                                    sender_reciever_events= sr_events)

    agent = ShortestPathAgent(physical_network= C,
                    virtual_network = Q)

    R = run_experiment(env, agent, epochs=args.epochs)
    print("Shortest Path: ", R[-1])

def run_experiment(env, agent, epochs):

    state = env._state
    sender = env._sender
    reciever = env._reciever
    R = []    

    r = 0
    for __ in range(epochs):
        # Compute action through Agent's policy
        if __ == 0:
            action = agent.run(state= state, sender= sender, reciever= reciever)
        else:
            action = agent.run(state= state, sender= sender, reciever= reciever, reward= result.reward, success=success)

        # State evolution and compute reward
        result = env.run(action= action)
        
        # Update parameters
        state = result.state
        sender = result.sender
        reciever = result.reciever
        success = result.success
        
        r += result.reward
        R.append(r)
    return R

if __name__ == "__main__":
    parser = ArgumentParser()

    # Benchmark 
    parser.add_argument("--epochs", type=int, default=50)
    
    # Network
    parser.add_argument("--n", type=int, default=12)
    parser.add_argument("--dth", type=int, default=3)

    # MCTS
    parser.add_argument("--mcts_sim_num", type=int, default=2000)
    parser.add_argument("--c_ucb1", type=float, default=2.0)

    args = parser.parse_args()
    main(args)