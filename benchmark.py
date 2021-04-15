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

#from argparse import ArgumentParser
from tqdm import tqdm
import json

import networkx as nx
import numpy as np

from environements.random import RandomEnvironement

from agents.random import RandomNeighborsAgent
from agents.egreedybandit import EGreedyBanditAgent
from agents.sarsa import SARSAAgent

from networks.cycle import cycle_net
from networks.random import random_net

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

def main():

    # Parameters
    nmin = 5
    nmax = 10
    d = 0.5
    epochs = 5
    experiments = 5

    for i in tqdm(range(experiments)):
        
        # Generate random network
        n = np.random.randint(nmin, nmax+1)
        p = np.random.uniform(0, 1)

        C, Q = random_net(n= n, p= p)
        
        DATA = {}
        DATA["physical network"] = {}
        DATA["physical network"]["nodes"] = list(C.nodes())
        DATA["physical network"]["edges"] = list(C.edges())
        DATA["virtual network"] = {}
        DATA["virtual network"]["nodes"] = list(Q.nodes())
        DATA["virtual network"]["edges"] = list(Q.edges())

        # Initialize the Environement, the different parameters and the Agent
        env = RandomEnvironement(physical_network = C, 
                                    virtual_network = Q)

        # Random Agent
        agent = RandomNeighborsAgent(physical_network = C, 
                                    virtual_network = Q)
        R = run_experiment(env, agent, epochs)
        DATA['random-agent'] = R
        SARSA = []
        for e in np.arange(0, 1+d, d):
            for a in np.arange(0, 1+d, d):
                for y in np.arange(0, 1+d, d):

                    D = {}
                    D['epsilon'] = e 
                    D['alpha'] = a 
                    D['gamma'] = y 

                    agent = SARSAAgent(physical_network = C, 
                                virtual_network = Q,
                                epsilon = e,
                                alpha = a,
                                gamma = y)
                    R = run_experiment(env, agent, epochs)
                    D['reward'] = R
                    SARSA.append(D)

        DATA['sarsa'] = SARSA
        with open('data/benchmark-sarsa/benchmark.json', 'w') as fp:
            json.dump(DATA, fp)

if __name__ == "__main__":
    main()
