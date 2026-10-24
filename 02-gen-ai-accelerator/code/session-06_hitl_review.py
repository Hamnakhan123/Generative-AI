"""Human-in-the-loop routing: let AI handle routine, high-confidence items and
send risky or uncertain ones to a person."""
drafts = [
    ("Reply: library timings", 0.95, "low"),
    ("Reply: fee refund request", 0.90, "high"),
    ("Reply: exam re-take policy", 0.62, "medium"),
    ("Reply: Wi-Fi password reset steps", 0.88, "low"),
    ("Reply: harassment complaint", 0.97, "high"),
]

def route(conf, stakes):
    if stakes == "high":
        return "HUMAN writes/approves"
    if conf < 0.75:
        return "HUMAN reviews"
    return "AUTO send + spot-check"

counts = {}
for item, conf, stakes in drafts:
    r = route(conf, stakes)
    counts[r] = counts.get(r, 0) + 1
    print(f"{item:36} conf={conf:.2f} stakes={stakes:6} -> {r}")
print("\n", counts)
