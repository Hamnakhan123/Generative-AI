"""
Session 1 · Example 2 — Scaled dot-product self-attention, step by step in NumPy.

Self-attention lets every word look at every other word and decide how much
each one matters for its own meaning:
    scores  = Q · K^T / sqrt(d_k)      (how well each query matches each key)
    weights = softmax(scores)          (each row sums to 1)
    output  = weights · V              (a weighted mix of the value vectors)

Run:  python session-01_attention_numpy.py
"""
import numpy as np

np.set_printoptions(precision=2, suppress=True)
rng = np.random.default_rng(7)

words = ["the", "cat", "sat", "down"]
d_model, d_k = 6, 4

# 1) Toy embeddings: one row per word (in a real model these are learned)
X = rng.normal(size=(len(words), d_model))

# 2) Learned projection matrices (random here) turn each embedding into Q, K, V
W_q = rng.normal(size=(d_model, d_k))
W_k = rng.normal(size=(d_model, d_k))
W_v = rng.normal(size=(d_model, d_k))
Q, K, V = X @ W_q, X @ W_k, X @ W_v
print("Shapes  X:", X.shape, " Q/K/V:", Q.shape)


def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)   # subtract max for numerical stability
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


# 3) Raw scores, scaled by sqrt(d_k) so softmax does not saturate
scores = Q @ K.T / np.sqrt(d_k)
weights = softmax(scores)
output = weights @ V

print("\nAttention weights (row = word looking, column = word looked at)")
print("        " + "  ".join(f"{w:>5}" for w in words))
for w, row in zip(words, weights):
    print(f"{w:>6}  " + "  ".join(f"{v:5.2f}" for v in row))
print("\nEach row sums to:", weights.sum(axis=1))

for w, row in zip(words, weights):
    print(f"'{w}' attends most to '{words[int(row.argmax())]}' ({row.max():.0%})")

# 4) Why scale? Compare the sharpness of softmax with and without the sqrt(d_k)
big_d = 512
q = rng.normal(size=big_d); keys = rng.normal(size=(4, big_d))
raw = keys @ q
print(f"\nWith d_k={big_d}: unscaled max weight = {softmax(raw).max():.3f}, "
      f"scaled max weight = {softmax(raw / np.sqrt(big_d)).max():.3f}")

# 5) Causal (decoder) mask: a word may not look at future words
mask = np.triu(np.ones((4, 4)), k=1).astype(bool)
masked = np.where(mask, -1e9, scores)
print("\nCausal weights (upper triangle is zero):")
print(softmax(masked))
print("Output vectors shape:", output.shape)
