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

from typing import List, Dict, Tuple
import pandas as pd

def parser(data: List[Dict])-> Tuple[object]:

    random = []
    sarsa = []
    for d in data:
        n = max(d['physical network']['nodes'][-1], d['virtual network']['nodes'][-1])

        random.append([n, d['random-agent']])
        for s in d['sarsa']:
            sarsa.append([n, s['param']['epsilon'], s['param']['alpha'], s['param']['gamma'], s['reward']])

    random = pd.DataFrame(random, columns= ['nodes', 'reward'])
    sarsa = pd.DataFrame(sarsa, columns= ['nodes', 'epsilon', 'alpha', 'gamma', 'reward'])
    return random, sarsa