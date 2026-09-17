 Classical AI & Search: Adversarial Game Playing Agent

An end-to-end, modular implementation of classical Artificial Intelligence search algorithms applied to the game of **Connect Four** ($6 \times 7$). 

This project explores foundational game-theoretic search concepts:
- **Zero-Sum Adversarial Search & Minimax**
- **Branch Elimination via $\alpha$-$\beta$ Pruning**
- **Heuristic Evaluation Functions & Center Control Theory**
- **Move Ordering Optimization**
- **Monte Carlo Tree Search (MCTS) with UCT**

---

## 1. Why Connect Four?

- **Game Tree Complexity**: $\approx 10^{21}$ total states with $\approx 4.5 \times 10^{12}$ valid reachable positions.
- **Why it matters**: Unlike Tic-Tac-Toe (which has only 255,168 states and can be solved trivially in milliseconds), Connect Four is deep enough that naive brute force search is impossible within reasonable turn limits. It forces the engineer to master **depth-bounded search**, **heuristic evaluation**, and **branch pruning**.

---

## 2. Theoretical Foundations

### A. The Minimax Algorithm
Minimax models two adversarial rational agents:
1. **MAX** ($\text{AI}$): Seeks to maximize the game utility $\max_{a} V(s')$.
2. **MIN** ($\text{Opponent}$): Seeks to minimize MAX's utility $\min_{a} V(s')$.

The value of node $s$ at depth $d$ is defined recursively:
$$V(s) = \begin{cases} 
\text{Utility}(s) & \text{if } s \text{ is terminal} \\
\text{Heuristic}(s) & \text{if } d = 0 \\
\max_{a} V(\text{Result}(s, a)) & \text{if } s \text{ is MAX node} \\
\min_{a} V(\text{Result}(s, a)) & \text{if } s \text{ is MIN node}
\end{cases}$$

### B. Alpha-Beta ($\alpha$-$\beta$) Pruning
$\alpha$-$\beta$ pruning maintains two bounds during recursive traversal:
- $\alpha$: Highest utility guaranteed to MAX so far along the search path.
- $\beta$: Lowest utility guaranteed to MIN so far along the search path.

**Cutoff Condition**: If $\beta \le \alpha$, the current sub-branch cannot affect the final decision and is pruned immediately:
- **Time Complexity with Perfect Ordering**: Reduces branching factor from $b^d$ to $b^{d/2}$.
- In Connect Four ($b \approx 7$), searching to depth 6 requires evaluating $\approx 7^6 \approx 117,649$ states under pure Minimax, but only $\approx 7^3 \approx 343$ states under optimal $\alpha$-$\beta$ search!

### C. Move Ordering
Pruning efficiency is strictly dependent on evaluating the strongest moves first. In Connect Four, **Column 3 (the exact center)** is mathematically involved in **13 distinct 4-in-a-row winning configurations** (more than any other column). By prioritizing column evaluations as `[3, 2, 4, 1, 5, 0, 6]`, alpha and beta bounds tighten much earlier.

### D. Heuristic Evaluation Function
When search terminates at depth cutoff $d = 0$, the heuristic scores all sliding $1 \times 4$ windows across horizontal, vertical, and both diagonal axes:
- 4 player pieces: $+10,000$ (terminal win)
- 3 player pieces + 1 empty: $+100$ (imminent offensive threat)
- 2 player pieces + 2 empty: $+10$ (strategic build)
- 3 opponent pieces + 1 empty: $-150$ (urgent defensive block)
- Center column occupancy bonus: $+6$ per piece

### E. Monte Carlo Tree Search (MCTS)
Unlike Minimax, which requires domain-specific static heuristics, MCTS evaluates states by statistical simulation:
1. **Selection**: Descends tree selecting children that maximize the **Upper Confidence Bound for Trees (UCT)**:
   $$\text{UCT}_i = \frac{W_i}{N_i} + c \sqrt{\frac{\ln(N_{\text{parent}})}{N_i}}$$
2. **Expansion**: Adds untried game states to the search tree.
3. **Simulation (Rollout)**: Plays rapid random rollouts to the terminal state.
4. **Backpropagation**: Propagates outcome back to ancestor nodes.

---

## 3. Project Structure

```
adversarial_game_ai/
├── game/
│   ├── __init__.py
│   ├── constants.py       # Board dimensions (6x7), piece constants, ASCII symbols
│   └── board.py           # 2D NumPy state, gravity physics, victory/draw checks
├── agents/
│   ├── __init__.py
│   ├── base_agent.py      # Abstract agent interface
│   ├── human_agent.py     # Interactive CLI input
│   ├── random_agent.py    # Uniform random baseline
│   ├── heuristic.py       # Window evaluation & center control metrics
│   ├── minimax_agent.py   # Pure Minimax & Alpha-Beta Pruning with telemetry
│   └── mcts_agent.py      # Monte Carlo Tree Search (UCT)
├── tests/
│   ├── __init__.py
│   ├── test_board.py      # Unit tests for gravity, undo, and win conditions
│   └── test_search.py     # Tests for instant win, instant block, and pruning speedup
├── benchmark.py           # Automated empirical comparison and tournament runner
├── main.py                # Interactive CLI menu
├── requirements.txt       # Dependencies (numpy, colorama)
└── README.md              # Technical documentation
```

---

## 4. Empirical Benchmark Results

Running `python benchmark.py` reproduces the empirical efficiency gains from Alpha-Beta pruning:

| Depth | Algorithm | Nodes Visited | Cutoffs | Time (ms) | Node Reduction |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | Pure Minimax | 8 | - | 0.94 | Baseline |
| | $\alpha$-$\beta$ (Unordered) | 8 | 0 | 0.80 | 0.0% |
| **2** | Pure Minimax | 57 | - | 4.90 | Baseline |
| | $\alpha$-$\beta$ (Unordered) | 21 | 6 | 1.71 | **63.2%** |
| **3** | Pure Minimax | 358 | - | 28.84 | Baseline |
| | $\alpha$-$\beta$ (Unordered) | 54 | 9 | 3.23 | **84.9%** |
| **4** | Pure Minimax | 2,465 | - | 185.82 | Baseline |
| | $\alpha$-$\beta$ (Unordered) | 174 | 24 | 18.27 | **92.9%** |
| **5** | Pure Minimax | 15,701 | - | 1,543.58 | Baseline |
| | $\alpha$-$\beta$ (Unordered) | 961 | 135 | 102.08 | **93.9%** |

---

## 5. How to Run

### Install Requirements
```bash
pip install -r requirements.txt
```

### Run Unit Tests
```bash
python -m unittest discover tests
```

### Run the Interactive Game
```bash
python main.py
```

### Run Search Benchmarks & Tournaments
```bash
python benchmark.py
```
