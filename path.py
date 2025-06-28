import tkinter as tk
import pygame
import sys
import time
from collections import deque
from datetime import datetime
import os
import heapq

# === Constants ===
GRID_ROWS = 15
GRID_COLS = 15
GRID_SIZE = 600
CELL_SIZE = GRID_SIZE // GRID_ROWS
HEADER_HEIGHT = 60
WINDOW_HEIGHT = GRID_SIZE + HEADER_HEIGHT
FPS = 60

# === Colors ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)
BLUE = (100, 149, 237)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
COLORS = {
    "A*": (0, 255, 127),   # Spring Green
    "Best First Search": (255, 20, 147)  # Deep Pink
}

# === Globals ===
grid = [['empty' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
start_pos = None
goal_pos = None
placement_mode = None
selected_algorithm = None
agent_path = []
timer_start = None
timer_running = False
elapsed_time = 0
algorithm_runs = []
log_directory = "pathhunter_logs"
compare_mode = False
compared_algorithms = []
grid_locked = False
dragging = False

# === Logging ===
def create_log_directory():
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

def generate_log_file(algorithm, path, time_taken, movements):
    create_log_directory()
    safe_algorithm = algorithm.replace('*', 'star').replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{log_directory}/{safe_algorithm}_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write(f"Algorithm: {algorithm}\n")
            f.write(f"Start Position: {start_pos}\n")
            f.write(f"Goal Position: {goal_pos}\n")
            f.write(f"Time Taken: {time_taken:.2f} seconds\n")
            f.write(f"Path Length: {len(path)} steps\n")
            f.write("\nGrid Layout:\n")
            for row in grid:
                f.write(' '.join([cell[0] if cell != 'empty' else '.' for cell in row]) + '\n')
            f.write("\nMovement Sequence:\n")
            for i, (r, c) in enumerate(path):
                if i > 0:
                    prev_r, prev_c = path[i-1]
                    if r < prev_r: direction = "UP"
                    elif r > prev_r: direction = "DOWN"
                    elif c < prev_c: direction = "LEFT"
                    elif c > prev_c: direction = "RIGHT"
                    f.write(f"Step {i}: Move {direction} to ({r}, {c})\n")
                else:
                    f.write(f"Step {i}: Start at ({r}, {c})\n")
    except OSError as e:
        print(f"Error writing log file: {e}")

# === Algorithms ===
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    open_set_hash = {start}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
            
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            
            if not (0 <= neighbor[0] < GRID_ROWS and 0 <= neighbor[1] < GRID_COLS):
                continue
                
            if grid[neighbor[0]][neighbor[1]] == 'obstacle':
                continue
                
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
    
    return []

def best_first_search(start, goal):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {}
    visited = set()
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
            
        if current in visited:
            continue
        visited.add(current)
        
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            
            if not (0 <= neighbor[0] < GRID_ROWS and 0 <= neighbor[1] < GRID_COLS):
                continue
                
            if grid[neighbor[0]][neighbor[1]] == 'obstacle':
                continue
                
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))
    
    return []

def show_no_path_message():
    root = tk.Tk()
    root.title("Path Not Found")
    root.geometry("300x100")
    
    label = tk.Label(root, text="No path found! Goal is surrounded by obstacles.", font=("Helvetica", 12))
    label.pack(pady=20)
    
    button = tk.Button(root, text="OK", command=root.destroy, font=("Helvetica", 12))
    button.pack()
    
    root.mainloop()

# === Tkinter UI for Algorithm Selection ===
def select_algorithm():
    def confirm_selection():
        nonlocal algo_var
        global selected_algorithm
        selected_algorithm = algo_var.get()
        if selected_algorithm:
            root.destroy()
            return True
        return False

    root = tk.Tk()
    root.title("PathHunter - Algorithm Selector")
    root.geometry("400x200")

    tk.Label(root, text="Select Navigation Algorithm", font=("Helvetica", 14)).pack(pady=10)

    algo_var = tk.StringVar(value="")
    algo_options = ["A*", "Best First Search"]
    
    for algo in algo_options:
        tk.Radiobutton(root, text=algo, variable=algo_var, value=algo, 
                      font=("Helvetica", 11)).pack(anchor="w", padx=40)

    confirm_button = tk.Button(root, text="Confirm", command=confirm_selection, 
                             font=("Helvetica", 11))
    confirm_button.pack(pady=10)
    
    def on_closing():
        global selected_algorithm
        selected_algorithm = None
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    
    return selected_algorithm is not None

# === Pygame Grid Setup ===
def run_pygame():
    global placement_mode, start_pos, goal_pos, agent_path
    global timer_start, timer_running, elapsed_time, algorithm_runs
    global compare_mode, compared_algorithms, grid_locked, dragging

    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE, WINDOW_HEIGHT))
    pygame.display.set_caption("PathHunter")
    font = pygame.font.SysFont(None, 20)
    clock = pygame.time.Clock()

    # Buttons
    play_button_center = (560, 25)
    play_button_radius = 20
    compare_button_center = (500, 25)
    compare_button_radius = 20
    reset_button_center = (440, 25)
    reset_button_radius = 20
    home_button_center = (380, 25)
    home_button_radius = 20

    agent_pos = None
    step_index = 0
    agent_movement = ""

    running = True
    while running:
        screen.fill(WHITE)

        # Header Text
        header_text = f"Algorithm: {selected_algorithm} | Mode: {placement_mode or 'None'}"
        header_surface = font.render(header_text, True, BLACK)
        screen.blit(header_surface, (10, 10))

        # Timer Text
        timer_text = f"{elapsed_time:.2f}s" if timer_running else f"{elapsed_time:.2f}s"
        timer_surface = font.render(f"Timer: {timer_text}", True, BLACK)
        screen.blit(timer_surface, (10, 35))

        # Agent Position
        pos_text = f"{agent_pos} : Movement → {agent_movement}" if agent_pos else ""
        pos_surface = font.render(f"Agent: {pos_text}", True, BLACK)
        screen.blit(pos_surface, (200, 35))

        # Draw buttons
        pygame.draw.circle(screen, BLUE, play_button_center, play_button_radius)
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (play_button_center[0] - 5, play_button_center[1] - 10),
                (play_button_center[0] - 5, play_button_center[1] + 10),
                (play_button_center[0] + 10, play_button_center[1]),
            ],
        )

        if len(algorithm_runs) >= 2 and not compare_mode:
            pygame.draw.circle(screen, PURPLE, compare_button_center, compare_button_radius)
            compare_text = font.render("C", True, WHITE)
            screen.blit(compare_text, (compare_button_center[0] - 5, compare_button_center[1] - 8))

        pygame.draw.circle(screen, RED, reset_button_center, reset_button_radius)
        reset_text = font.render("R", True, WHITE)
        screen.blit(reset_text, (reset_button_center[0] - 5, reset_button_center[1] - 8))

        pygame.draw.circle(screen, GREEN, home_button_center, home_button_radius)
        home_text = font.render("H", True, WHITE)
        screen.blit(home_text, (home_button_center[0] - 5, home_button_center[1] - 8))

        # Grid Drawing
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE + HEADER_HEIGHT
                color = WHITE
                if grid[row][col] == 'start':
                    color = GREEN
                elif grid[row][col] == 'goal':
                    color = RED
                elif grid[row][col] == 'obstacle':
                    color = BLACK
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GREY, (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Draw paths from previous runs
        for i, run in enumerate(algorithm_runs):
            if compare_mode or i == len(algorithm_runs) - 1:
                path = run['path']
                color = COLORS.get(run['algorithm'], BLUE)
                for r, c in path:
                    x = c * CELL_SIZE + CELL_SIZE // 2
                    y = r * CELL_SIZE + HEADER_HEIGHT + CELL_SIZE // 2
                    pygame.draw.circle(screen, color, (x, y), 3)

        # Agent
        if agent_pos:
            ar, ac = agent_pos
            x = ac * CELL_SIZE
            y = ar * CELL_SIZE + HEADER_HEIGHT
            agent_color = COLORS.get(selected_algorithm, YELLOW)
            pygame.draw.circle(screen, agent_color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)

        # Comparison visualization
        if compare_mode:
            y_pos = WINDOW_HEIGHT - 20
            max_time = max(run['time'] for run in compared_algorithms) if compared_algorithms else 1
            
            for run in compared_algorithms:
                algo = run['algorithm']
                time_taken = run['time']
                color = COLORS.get(algo, BLUE)
                
                # Draw bar
                bar_width = int((time_taken / max_time) * 200) if max_time > 0 else 0
                pygame.draw.rect(screen, color, (50, y_pos - 15, bar_width, 10))
                
                # Draw label
                label = font.render(f"{algo}: {time_taken:.2f}s", True, color)
                screen.blit(label, (260, y_pos - 15))
                
                y_pos -= 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and not grid_locked:
                if event.key == pygame.K_s:
                    placement_mode = "start"
                elif event.key == pygame.K_g:
                    placement_mode = "goal"
                elif event.key == pygame.K_o:
                    placement_mode = "obstacle"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Play Button
                dx = x - play_button_center[0]
                dy = y - play_button_center[1]
                if dx ** 2 + dy ** 2 <= play_button_radius ** 2 and not grid_locked:
                    if start_pos and goal_pos:
                        grid_locked = True
                        if selected_algorithm == "A*":
                            agent_path = a_star(start_pos, goal_pos)
                        elif selected_algorithm == "Best First Search":
                            agent_path = best_first_search(start_pos, goal_pos)
                        
                        if not agent_path:
                            show_no_path_message()
                            grid_locked = False
                        else:
                            step_index = 0
                            agent_pos = agent_path[0]
                            timer_start = time.time()
                            timer_running = True
                            algorithm_runs.append({
                                'algorithm': selected_algorithm,
                                'path': agent_path.copy(),
                                'time': 0
                            })

                # Compare Button
                dx = x - compare_button_center[0]
                dy = y - compare_button_center[1]
                if dx ** 2 + dy ** 2 <= compare_button_radius ** 2 and len(algorithm_runs) >= 2:
                    compare_mode = not compare_mode
                    if compare_mode:
                        compared_algorithms = algorithm_runs[-2:]

                # Reset Button
                dx = x - reset_button_center[0]
                dy = y - reset_button_center[1]
                if dx ** 2 + dy ** 2 <= reset_button_radius ** 2:
                    agent_pos = None
                    agent_path = []
                    timer_running = False
                    elapsed_time = 0
                    grid_locked = False

                # Home Button - Now working properly
                dx = x - home_button_center[0]
                dy = y - home_button_center[1]
                if dx ** 2 + dy ** 2 <= home_button_radius ** 2:
                    agent_pos = None
                    agent_path = []
                    timer_running = False
                    elapsed_time = 0
                    grid_locked = False
                    running = False

                # Grid Interaction
                elif y >= HEADER_HEIGHT and not grid_locked:
                    row = (y - HEADER_HEIGHT) // CELL_SIZE
                    col = x // CELL_SIZE
                    if row < GRID_ROWS and col < GRID_COLS:
                        if event.button == 1:
                            dragging = True
                            if placement_mode == "start":
                                if start_pos:
                                    r, c = start_pos
                                    grid[r][c] = 'empty'
                                start_pos = (row, col)
                                grid[row][col] = 'start'

                            elif placement_mode == "goal":
                                if goal_pos:
                                    r, c = goal_pos
                                    grid[r][c] = 'empty'
                                goal_pos = (row, col)
                                grid[row][col] = 'goal'

                            elif placement_mode == "obstacle":
                                if grid[row][col] == 'empty':
                                    grid[row][col] = 'obstacle'

                        elif event.button == 3:
                            if grid[row][col] == 'obstacle':
                                grid[row][col] = 'empty'

            elif event.type == pygame.MOUSEMOTION and dragging and not grid_locked:
                x, y = event.pos
                if y >= HEADER_HEIGHT:
                    row = (y - HEADER_HEIGHT) // CELL_SIZE
                    col = x // CELL_SIZE
                    if row < GRID_ROWS and col < GRID_COLS:
                        if placement_mode == "obstacle" and grid[row][col] == 'empty':
                            grid[row][col] = 'obstacle'

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

        # Agent Movement
        if timer_running and agent_path:
            if step_index < len(agent_path):
                agent_pos = agent_path[step_index]
                if step_index > 0:
                    pr, pc = agent_path[step_index - 1]
                    cr, cc = agent_path[step_index]
                    if cr < pr:
                        agent_movement = "UP"
                    elif cr > pr:
                        agent_movement = "DOWN"
                    elif cc < pc:
                        agent_movement = "LEFT"
                    elif cc > pc:
                        agent_movement = "RIGHT"
                step_index += 1
                time.sleep(0.1)
            else:
                timer_running = False
                elapsed_time = time.time() - timer_start
                algorithm_runs[-1]['time'] = elapsed_time
                generate_log_file(selected_algorithm, agent_path, elapsed_time, [])

        pygame.display.flip()
        clock.tick(FPS)
    
    # Return True to indicate we should go back to algorithm selection
    return True

# === Main ===
if __name__ == "__main__":
    while True:
        # Reset run-specific variables
        agent_path = []
        timer_running = False
        elapsed_time = 0
        compare_mode = False
        compared_algorithms = []
        grid_locked = False
        
        # Select algorithm
        if not select_algorithm():
            break
            
        # Run visualization
        should_continue = run_pygame()
        if not should_continue:
            break