"""
Session 4 · Example 3 — How a Kubernetes HorizontalPodAutoscaler sizes a model service over a day.

HPA rule: desired = ceil(pods * utilisation / target). One pod serves ~60 req/s at 100% CPU;
target 70%. We simulate a results-day spike and compare cost with a fixed fleet.

Run:  python session-04_autoscaling.py
Creates: session-04_autoscaling.png
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

POD_CAPACITY_RPS = 60          # requests/second one pod can serve at 100% CPU
TARGET = 0.70                  # HPA target utilisation
MIN_PODS, MAX_PODS = 2, 20
COST_PER_POD_HOUR = 0.05       # USD, illustrative cloud price

# Requests per second each hour (results announced at 10:00 -> spike)
traffic = [20, 15, 10, 10, 12, 20, 40, 90, 160, 260, 900, 720, 480,
           350, 300, 260, 240, 260, 300, 280, 200, 120, 60, 30]

pods = MIN_PODS
history = []
print(f"{'hour':>4} {'rps':>5} {'util before':>12} {'pods':>5} {'util after':>11}")
for hour, rps in enumerate(traffic):
    util = rps / (pods * POD_CAPACITY_RPS)                       # what the HPA observes
    desired = math.ceil(pods * util / TARGET)
    pods_new = max(MIN_PODS, min(MAX_PODS, desired))
    after = rps / (pods_new * POD_CAPACITY_RPS)
    flag = "  <- capped at max, requests queue" if after > 1 else ""
    if 6 <= hour <= 14:                                          # print the busy part of the day
        print(f"{hour:4d} {rps:5d} {util:12.0%} {pods_new:5d} {after:11.0%}{flag}")
    pods = pods_new
    history.append(pods)

peak_pods = math.ceil(max(traffic) / (POD_CAPACITY_RPS * TARGET))
auto_cost = sum(history) * COST_PER_POD_HOUR
fixed_cost = min(peak_pods, MAX_PODS) * 24 * COST_PER_POD_HOUR
print(f"\nPod-hours with autoscaling: {sum(history)} -> ${auto_cost:.2f}/day")
print(f"Fixed fleet sized for peak ({min(peak_pods, MAX_PODS)} pods): {min(peak_pods, MAX_PODS) * 24} pod-hours -> ${fixed_cost:.2f}/day")
print(f"Saving: {100 * (1 - auto_cost / fixed_cost):.0f}%")

fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(range(24), traffic, color="#FCD34D", label="requests/second")
ax1.set_xlabel("Hour of day"); ax1.set_ylabel("Requests per second")
ax2 = ax1.twinx()
ax2.step(range(24), history, where="mid", color="#FF6B1A", lw=2.5, label="pods")
ax2.set_ylabel("Pods running"); ax2.set_ylim(0, MAX_PODS + 2)
ax1.set_title("HPA scaling a model service through a results-day spike")
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.88))
fig.tight_layout(); fig.savefig("session-04_autoscaling.png", dpi=110)
print("Saved chart: session-04_autoscaling.png")
