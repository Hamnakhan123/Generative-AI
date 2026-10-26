"""
Session 6 · Example 1 — Critical path of an event plan (CPM).

AI assistants are good at listing tasks for a big job, but they rarely
compute the schedule correctly. The Critical Path Method does:
  * earliest start (ES) of a task = latest earliest-finish of its prerequisites
  * the project length = largest earliest finish
  * latest start (LS) found by walking backwards; slack = LS - ES
  * tasks with zero slack form the CRITICAL PATH: any delay there delays everything.

Run:  python session-06_critical_path.py
"""
tasks = {  # id: (days, prerequisites, description)
    "A": (3, [],          "Define goals, budget, audience"),
    "B": (5, ["A"],       "Book venue and date"),
    "C": (4, ["A"],       "Invite speakers"),
    "D": (6, ["B", "C"],  "Design and print materials"),
    "E": (7, ["B"],       "Run promotion campaign"),
    "F": (2, ["C"],       "Confirm speaker travel"),
    "G": (2, ["D", "E", "F"], "Rehearsal and final checks"),
}

# Forward pass (dict order is already a valid topological order here)
ES, EF = {}, {}
for t, (d, pre, _) in tasks.items():
    ES[t] = max((EF[p] for p in pre), default=0)
    EF[t] = ES[t] + d
length = max(EF.values())

# Backward pass
LF, LS = {}, {}
for t in reversed(list(tasks)):
    succ = [s for s, (_, pre, _) in tasks.items() if t in pre]
    LF[t] = min((LS[s] for s in succ), default=length)
    LS[t] = LF[t] - tasks[t][0]

print(f"{'Task':4} {'Days':>4} {'ES':>3} {'EF':>3} {'LS':>3} {'Slack':>5}  Description")
for t, (d, _, desc) in tasks.items():
    slack = LS[t] - ES[t]
    mark = "  <- critical" if slack == 0 else ""
    print(f"{t:4} {d:4} {ES[t]:3} {EF[t]:3} {LS[t]:3} {slack:5}  {desc}{mark}")
critical = [t for t in tasks if LS[t] == ES[t]]
print(f"\nProject length: {length} days | Critical path: {' -> '.join(critical)}")
