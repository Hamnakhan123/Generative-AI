"""
Session 6 · Mini project (full solution) — Campaign planner with a Gantt chart.

Real-life problem: plan a 4-week admissions campaign. Inputs: a launch date,
a list of workstreams with durations and dependencies. Outputs:
  * a dated schedule (computed by the critical path method),
  * a weekly content calendar (which post goes out on which day),
  * a Mermaid gantt block you can paste into any Markdown page,
  * a Gantt chart PNG made with matplotlib.

Run:  python session-06_project_campaign_planner.py
Creates: session-06_gantt.png
"""
from datetime import date, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

START = date(2026, 11, 2)   # Monday
work = {  # id: (name, days, prerequisites)
    "res": ("Audience research with AI", 3, []),
    "msg": ("Key messages and slogan", 2, ["res"]),
    "vis": ("Visual kit: posters, templates", 5, ["msg"]),
    "vid": ("Promo video and captions", 6, ["msg"]),
    "web": ("Landing page copy", 3, ["msg"]),
    "run": ("Campaign live: posts and ads", 14, ["vis", "vid", "web"]),
    "rep": ("Results report", 2, ["run"]),
}

es, ef = {}, {}
for k, (_, d, pre) in work.items():
    es[k] = max((ef[p] for p in pre), default=0)
    ef[k] = es[k] + d
end = max(ef.values())

# backward pass: latest start; zero slack = critical
ls = {}
for k in reversed(list(work)):
    succ = [s for s, (_, _, pre) in work.items() if k in pre]
    lf = min((ls[s] for s in succ), default=end)
    ls[k] = lf - work[k][1]
critical = [k for k in work if ls[k] == es[k]]

print("SCHEDULE")
for k, (name, d, _) in work.items():
    s, e = START + timedelta(es[k]), START + timedelta(ef[k] - 1)
    print(f"  {name:32} {s:%d %b} -> {e:%d %b}  ({d} d)")
print(f"  Finish: {START + timedelta(end - 1):%a %d %b %Y} ({end} days)")
print(f"  Critical path: {' -> '.join(work[k][0] for k in critical)}")

print("\nCONTENT CALENDAR (campaign-live window)")
themes = ["Why study CS here", "Student story", "Lab tour reel", "Scholarship facts", "Q&A live"]
days = {0: "Mon", 2: "Wed", 4: "Fri"}
live = START + timedelta(es["run"])
n = 0
for offset in range(work["run"][1]):
    d = live + timedelta(offset)
    if d.weekday() in days:
        print(f"  {d:%a %d %b}: {themes[n % len(themes)]}")
        n += 1

print("\nMERMAID GANTT")
print("gantt\n    dateFormat YYYY-MM-DD\n    title Admissions campaign")
for k, (name, d, _) in work.items():
    print(f"    {name} :{k}, {START + timedelta(es[k])}, {d}d")

fig, ax = plt.subplots(figsize=(8, 3.5))
for i, (k, (name, d, _)) in enumerate(work.items()):
    ax.barh(i, d, left=es[k], color="#FF6B1A" if k in critical else "#A78BFA")
ax.set_yticks(range(len(work)))
ax.set_yticklabels([v[0] for v in work.values()], fontsize=8)
ax.invert_yaxis()
ax.set_xlabel(f"Days from {START:%d %b %Y} (orange = critical path)")
ax.set_title("Admissions campaign plan")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig("session-06_gantt.png", dpi=80)
print("\nSaved -> session-06_gantt.png")
