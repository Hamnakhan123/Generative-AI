"""Check an AI screening tool for disparate impact with the four-fifths (80%) rule:
each group's selection rate should be at least 80% of the highest group's rate."""
results = {  # group: (applicants, shortlisted by the AI tool)
    "Group A": (200, 60),
    "Group B": (150, 30),
    "Group C": (100, 27),
}
rates = {g: s / n for g, (n, s) in results.items()}
best = max(rates.values())
print(f"{'Group':8} {'rate':>6} {'ratio':>6}  check")
for g, r in rates.items():
    ratio = r / best
    print(f"{g:8} {r:>6.2f} {ratio:>6.2f}  {'OK' if ratio >= 0.8 else 'POSSIBLE BIAS - investigate'}")
