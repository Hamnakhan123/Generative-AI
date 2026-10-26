"""
Session 5 · Mini project (full solution) — Q-learning delivery robot in a warehouse.

Real-life problem: a warehouse robot must carry parcels from the dock (S) to the
packing desk (G) while avoiding shelves (#) and a wet-floor zone (~) that costs
extra battery. Nobody writes the route: the robot LEARNS it by trial and error.

Q-learning update:  Q[s,a] += α * (r + γ * max_a' Q[s',a'] - Q[s,a])
Rewards: -1 per move, -15 per wet cell, -5 for bumping a shelf, +100 at the desk.
Exploration: ε-greedy, ε decays from 1.0 to 0.05 over 1,000 episodes.

Run:  python session-05_project_delivery_agent.py
Creates: session-05_q_learning_rewards.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GRID = [
    "S..#....",
    ".#.#.##.",
    ".#...#..",
    ".##~~#.#",
    "...~~...",
    "#.##.##.",
    "......#G",
]
H, W = len(GRID), len(GRID[0])
ACTIONS = {0: (-1, 0, "↑"), 1: (1, 0, "↓"), 2: (0, -1, "←"), 3: (0, 1, "→")}
start = next((r, c) for r in range(H) for c in range(W) if GRID[r][c] == "S")
goal = next((r, c) for r in range(H) for c in range(W) if GRID[r][c] == "G")


def step(state, a):
    dr, dc, _ = ACTIONS[a]
    r, c = state[0] + dr, state[1] + dc
    if not (0 <= r < H and 0 <= c < W) or GRID[r][c] == "#":
        return state, -5, False                  # bumped a wall/shelf
    if (r, c) == goal:
        return (r, c), 100, True
    return (r, c), (-15 if GRID[r][c] == "~" else -1), False   # each move costs battery


rng = np.random.default_rng(0)
Q = np.zeros((H, W, 4))
alpha, gamma, episodes = 0.3, 0.99, 2000
rewards = []
for ep in range(episodes):
    eps = max(0.05, 1.0 - ep / 1000)
    s, total = start, 0
    for _ in range(200):
        a = int(rng.integers(4)) if rng.random() < eps else int(Q[s].argmax())
        s2, r, done = step(s, a)
        Q[s][a] += alpha * (r + gamma * Q[s2].max() * (not done) - Q[s][a])
        s, total = s2, total + r
        if done:
            break
    rewards.append(total)

# Follow the learned greedy policy
s, path = start, [start]
while s != goal and len(path) < 60:
    s, _, _ = step(s, int(Q[s].argmax())); path.append(s)

print(f"Average reward, first 50 episodes: {np.mean(rewards[:50]):8.1f}")
print(f"Average reward, last 50 episodes : {np.mean(rewards[-50:]):8.1f}")
print(f"Learned route: {len(path) - 1} moves, reaches goal: {s == goal}, "
      f"wet cells crossed: {sum(GRID[r][c] == '~' for r, c in path)}")

print("\nGreedy policy (arrows) and route (*):")
for r in range(H):
    row = ""
    for c in range(W):
        ch = GRID[r][c]
        if ch in "#SG~" and (r, c) not in path[1:-1]:
            row += ch
        elif (r, c) in path[1:-1]:
            row += "*"
        else:
            row += ACTIONS[int(Q[r, c].argmax())][2]
    print("   " + " ".join(row))

smooth = np.convolve(rewards, np.ones(25) / 25, mode="valid")
plt.figure(figsize=(7.5, 4))
plt.plot(rewards, color="#A78BFA", alpha=.35, label="episode reward")
plt.plot(range(24, episodes), smooth, color="#FF6B1A", lw=2.5, label="25-episode average")
plt.xlabel("Episode"); plt.ylabel("Total reward"); plt.ylim(-400, 120)
plt.title("Q-learning: the robot discovers a short, dry route"); plt.legend(); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig("session-05_q_learning_rewards.png", dpi=110)
print("\nSaved chart: session-05_q_learning_rewards.png")
