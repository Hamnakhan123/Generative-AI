"""How 'temperature' reshapes a model's next-token probabilities.
Low temperature -> safe, repetitive; high temperature -> varied, riskier."""
import math

logits = {"class": 2.0, "lab": 1.5, "library": 0.5, "moon": -1.0}  # raw model scores

def softmax(scores, t):
    exps = {k: math.exp(v / t) for k, v in scores.items()}
    z = sum(exps.values())
    return {k: e / z for k, e in exps.items()}

print("Next word after 'Students study in the ...'\n")
print(f"{'temp':>5} " + " ".join(f"{k:>8}" for k in logits))
for t in [0.2, 0.7, 1.0, 1.5]:
    p = softmax(logits, t)
    print(f"{t:>5} " + " ".join(f"{p[k]:>8.2f}" for k in logits))
