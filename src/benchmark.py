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
from datetime import datetime
import uuid

from tqdm.contrib.concurrent import process_map

import json
import os

import numpy as np

from environements.random import RandomEnvironement

from agents.random import RandomNeighborsAgent
from agents.greed_routing_agent import GreedyNeighborsAgent
from agents.sarsa import SARSAAgent

from networks.cycle import cycle_net
from networks.random import random_net

def benchmark(args):
        
    # Generate random network
    n = np.random.randint(args.nmin, args.nmax+1)

    dth = np.random.randint(1, args.dthmax+1)
    C, Q = cycle_net(n= n, dth= dth)
    
    DATA = {}
    DATA["physical network"] = {}
    DATA["physical network"]["nodes"] = list(C.nodes())
    DATA["physical network"]["edges"] = list(C.edges())
    DATA["virtual network"] = {}
    DATA["virtual network"]["nodes"] = list(Q.nodes())
    DATA["virtual network"]["edges"] = list(Q.edges())

    # Initialize the Environement
    env = RandomEnvironement(physical_network = C, 
                                virtual_network = Q)

    #### Random Agent ###
    agent = RandomNeighborsAgent(physical_network = C, 
                                virtual_network = Q)

    R = run_experiment(env, agent, args.epochs)
    DATA['random-agent'] = R

    #### Greedy Neighbnors Agent ###
    agent = GreedyNeighborsAgent(physical_network = C, 
                                virtual_network = Q)

    R = run_experiment(env, agent, args.epochs)
    DATA['greedy-neighbors-agent'] = R

    # #### SARSA ####
    SARSA = []
    for e in np.arange(0, 1+args.delta, args.delta):
        for a in np.arange(0, 1+args.delta, args.delta):
            for y in np.arange(0, 1+args.delta, args.delta):

                D = {}
                D['param'] = {}
                D['param']['epsilon'] = e 
                D['param']['alpha'] = a 
                D['param']['gamma'] = y 

                agent = SARSAAgent(physical_network = C, 
                            virtual_network = Q,
                            epsilon = e,
                            alpha = a,
                            gamma = y)

                R = run_experiment(env, agent, args.epochs)
                D['reward'] = R
                SARSA.append(D)

    DATA['sarsa'] = SARSA

    # Save data
    with open(args.savepath + '{}.json'.format(uuid.uuid4().hex), 'w') as fp:
        json.dump(DATA, fp)

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
            action = agent.run(state= state, sender= sender, reciever= reciever, reward= result.reward)
        
        # State evolution and compute reward
        result = env.run(action= action)
        
        # Update parameters
        state = result.state
        sender = result.sender
        reciever = result.reciever
        
        r += result.reward
        R.append(r)
    return R

if __name__ == "__main__":
    parser = ArgumentParser()

    # Experiments 
    parser.add_argument("--experiments", type=int, default=10000)
    parser.add_argument("--epochs", type=int, default=200)

    # Agent
    parser.add_argument("--delta", type=float, default=0.1)
    
    # Network
    parser.add_argument("--nmin", type=int, default=5)
    parser.add_argument("--nmax", type=int, default=30)
    parser.add_argument("--dthmax", type=int, default=5)

    # Saving data
    parser.add_argument("--savepath", type=str, default="data/benchmark/") 

    # Multiprocessing
    parser.add_argument("--num_cpu", type=int, default=4) 

    args = parser.parse_args()

    if not os.path.isdir(args.savepath):
        args.savepath += datetime.now().strftime("%Y%m%d%H%M%S")+"/"
        os.makedirs(args.savepath)

    process_map(benchmark, [args]*args.experiments, max_workers=args.num_cpu)