# Algorithms for Quantum Internet Routing
Different implementation of algorithms (greedy, shortest path, Monte Carlo Tree Search, SARSA, etc..) for Quantum Internet Routing. Still under construction...

## Requirements

* Python 3.6+
* NetworkX

```shell
pip install -r requirements.txt
```

## Run a benchmark

The following command will run a benchmark on a cycle networks.

```shell
python src/benchmark.py \
    --epochs 10 \
    --n 8 \
    --dth 3 \
    --mcts_sim_num 500 \
    --c_ucb1 2
```

## License
[Apache License 2.0](https://github.com/adelshb/Algorithms-for-Quantum-Internet-Routing/blob/main/LICENSE)
