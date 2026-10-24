"""Weighted decision matrix for choosing an AI assistant for a specific job.
Scores (1-5) are a SAMPLE class evaluation; re-score them with your own tests."""
criteria = {"accuracy": 0.30, "citations": 0.25, "speed": 0.15, "integration": 0.20, "cost": 0.10}
scores = {
    "ChatGPT": {"accuracy": 5, "citations": 3, "speed": 4, "integration": 3, "cost": 3},
    "Copilot": {"accuracy": 4, "citations": 5, "speed": 4, "integration": 5, "cost": 4},
    "Gemini":  {"accuracy": 4, "citations": 4, "speed": 5, "integration": 4, "cost": 4},
}
print(f"{'Tool':8} " + " ".join(f"{c[:5]:>6}" for c in criteria) + "   weighted")
results = {}
for tool, s in scores.items():
    total = sum(s[c] * w for c, w in criteria.items())
    results[tool] = total
    print(f"{tool:8} " + " ".join(f"{s[c]:>6}" for c in criteria) + f"   {total:.2f}")
best = max(results, key=results.get)
print(f"\nBest fit for a 'research report with sources' job: {best} ({results[best]:.2f}/5)")
