"""Final-project helper: score two prompt versions against a rubric and pick the winner.
Scores are from a simulated reviewer (fixed numbers) so the run is reproducible; replace them with your own."""
RUBRIC = {"Clarity of task": 3, "Context & audience": 2, "Output format": 2, "Constraints & safety": 2, "Examples": 1}
scores = {  # marks given per criterion, out of the weight
    "v1 (zero-shot)": {"Clarity of task": 2, "Context & audience": 1, "Output format": 0, "Constraints & safety": 1, "Examples": 0},
    "v2 (role + format + few-shot)": {"Clarity of task": 3, "Context & audience": 2, "Output format": 2, "Constraints & safety": 1, "Examples": 1},
}
total = sum(RUBRIC.values())
print(f"{'Criterion':22}" + "".join(f"{k[:28]:>30}" for k in scores))
for c, w in RUBRIC.items():
    print(f"{c + f' (/{w})':22}" + "".join(f"{scores[k][c]:>30}" for k in scores))
results = {k: sum(v.values()) for k, v in scores.items()}
print(f"{'TOTAL (/' + str(total) + ')':22}" + "".join(f"{results[k]:>30}" for k in scores))
best = max(results, key=results.get)
print(f"\nWinner: {best} ({results[best] / total:.0%}). Weakest criterion overall: "
      f"{min(RUBRIC, key=lambda c: sum(scores[k][c] / RUBRIC[c] for k in scores))}")
