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

from typing import List

def active_nodes(quantum_network_status: List[List[float]])->List:
    """ Collect all the active nodes (nodes where there is still entanglement with another node)
    Returns:
        List of active nodes.
    """

    nodes = []
    for i,row in enumerate(quantum_network_status):
        for j,val in enumerate(row):
            if val !=0 and j!=i:
                nodes.append(i)
            break

    return nodes