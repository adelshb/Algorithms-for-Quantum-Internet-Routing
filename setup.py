from setuptools import setup, find_packages

setup(
   name='Quantum Internet Routing with Reinforcement Learning',
   packages=find_packages(), 
   install_requires=['networkx',
                    'tqdm',
                    'pandas'
                    ])