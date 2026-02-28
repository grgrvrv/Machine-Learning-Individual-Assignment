# Q-Learning Tower Defense (CDS524 Assignment 1)

A grid-based Tower Defense game built with Python and Pygame, featuring a custom Tabular Q-Learning agent that learns optimal strategic placements.

## Features
- **Two AI Modes**: 
  - `Untrained`: Agent explores the state-action space randomly ($\epsilon=0.4$).
  - `Expert`: Agent exploits a heuristic-initialized Q-table for perfect defense ($\epsilon=0.0$).
- **Dual Weapons**: Melee (High DMG, Short Range) and Sniper (Low DMG, Long Range).
- **Dynamic Routing**: 10x10 grid with dynamically generated enemy paths.

## Requirements
- Python 3.12+
- Pygame (`pip install pygame`)

## How to Run
```bash
python main.py