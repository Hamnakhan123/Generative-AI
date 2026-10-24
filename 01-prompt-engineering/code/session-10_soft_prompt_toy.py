"""Toy 'soft prompt' (prompt tuning) demo in pure Python.
A frozen 'model' adds up each word's sentiment (x), weighting each word by how much it 'attends'
to the prompt vector: weight = 1 + soft . v. The word vectors and the scoring rule never change.
We learn ONLY the 2-number soft prompt so the frozen model stops being fooled by
complaints that start with a polite word ("great, we waited hours again")."""
VEC = {"great": (1.0, -0.5), "love": (0.9, -0.5), "fast": (0.6, 0.0), "service": (0.1, 0.0),
       "waited": (-0.2, 0.9), "hours": (-0.1, 0.8), "broken": (-0.9, 0.3), "again": (0.0, 0.4)}
data = [("great fast service", 1), ("love the service", 1),
        ("great waited hours again", 0), ("love waited hours", 0), ("broken again", 0)]

def model(sentence, soft):
    score = 0.0
    for w in sentence.split():
        x, y = VEC.get(w, (0.0, 0.0))
        score += x * (1 + soft[0] * x + soft[1] * y)
    return score

def accuracy(soft):
    return sum((model(s, soft) > 0) == bool(l) for s, l in data) / len(data)

def loss(soft):  # hinge loss with margin 0.1
    return sum(max(0.0, 0.1 - (1 if l else -1) * model(s, soft)) for s, l in data)

soft = [0.0, 0.0]
print(f"Before tuning: soft prompt = ({soft[0]:+.2f}, {soft[1]:+.2f}), accuracy = {accuracy(soft):.0%}")
lr, eps = 0.1, 1e-4
for step in range(300):  # numeric gradient descent; only the soft prompt moves, the model stays frozen
    grad = []
    for k in range(2):
        up = soft.copy(); up[k] += eps
        grad.append((loss(up) - loss(soft)) / eps)
    soft = [soft[k] - lr * grad[k] for k in range(2)]
print(f"After tuning : soft prompt = ({soft[0]:+.2f}, {soft[1]:+.2f}), accuracy = {accuracy(soft):.0%}, loss = {loss(soft):.2f}")
for s, l in data:
    print(f"  {s:26} label={'pos' if l else 'neg'}  score={model(s, soft):+.2f}")
