# 🧭 PathHunter: A* vs Best-First Search Pathfinding Visualizer

PathHunter is a Python-based visual simulator that lets users compare the performance of **A\*** and **Greedy Best-First Search (GBFS)** algorithms on a customizable 2D grid.

Built with `pygame` and `tkinter`, the tool features:
- Grid-based path visualization
- Interactive obstacle placement
- Timing comparison between algorithms
- Movement logs saved as `.txt` files

---

## 🚀 Features

- ✅ Select between **A\*** or **Best First Search**
- ✅ Place **Start**, **Goal**, and **Obstacle** cells with key+click
- ✅ Visualize agent path and direction step-by-step
- ✅ Record traversal logs with step sequences and grid snapshots
- ✅ Compare performance using on-screen bars

---

## 🛠 Technologies Used

- Python 3.x  
- `pygame` – visual interface  
- `tkinter` – algorithm selector  
- `heapq` – priority queue for search  
- `datetime`, `os`, `time` – logging and performance timing  

---

## 🧪 Sample Log File Output

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

## How to Use
Launch the program

bash
python pathhunter.py
Select your algorithm in the popup window.

Keyboard controls during Pygame execution:

S → Place Start

G → Place Goal

O → Place Obstacle

Left Click → Place elements

Right Click → Erase obstacles

Play Button (Blue) → Run the algorithm

Compare Button (Purple) → Toggle performance bars

Reset/Restart (Red / Green Buttons) → Clear or return to home

Logs will be saved inside the pathhunter_logs/ folder with timestamps.

## 🌱 Future Ideas
[ ] Add Dijkstra’s Algorithm to the comparison

[ ] GUI enhancements: sliders for grid size, color themes

[ ] Export path images or animations

[ ] Run algorithms in parallel threads


## ✨ Author
Pisupati Sricharan — exploring algorithms, secure systems, and robotics.
