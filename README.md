# 🧭 PathHunter: A* vs Best-First Search Pathfinding Visualizer

**PathHunter** is a Python-based visual simulator that compares the performance of **A\*** and **Greedy Best-First Search (GBFS)** algorithms on a customizable 2D grid.

Built using `pygame` and `tkinter`, it features:
- Grid-based path visualization
- Interactive obstacle placement
- Timing comparison between algorithms
- Movement logs saved as `.txt` files

---

## 🚀 Features

- ✅ Algorithm selection: **A\*** or **Best First Search**
- ✅ Keyboard+mouse grid editing (Start, Goal, Obstacles)
- ✅ Real-time path visualization and direction steps
- ✅ Generates detailed log files for every run
- ✅ Visual comparison of performance using bar charts

---

## 🛠 Technologies Used

- **Python 3.x**
- `pygame` – graphical visualization
- `tkinter` – algorithm selection interface
- `heapq` – priority queue logic
- `datetime`, `os`, `time` – logging and performance measurement

---

## 🧪 Sample Log Output

```txt
Algorithm: A*
Start Position: (2, 3)
Goal Position: (10, 12)
Time Taken: 1.27 seconds
Path Length: 18 steps

Grid Layout:
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . S . . . . . . . . . . .
. . . . . . . . . . . . . . .
... (trimmed for brevity)

Movement Sequence:
Step 0: Start at (2, 3)
Step 1: Move DOWN to (3, 3)
Step 2: Move DOWN to (4, 3)
...
Step 17: Move RIGHT to (10, 12)
