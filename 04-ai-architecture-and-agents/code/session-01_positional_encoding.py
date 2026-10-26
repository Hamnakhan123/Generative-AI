"""
Session 1 · Example 3 — Sinusoidal positional encoding and why word order needs it.

Attention by itself is order-blind: shuffling the words shuffles the outputs but
does not change them. Transformers add a position signal to each embedding:
    PE[pos, 2i]   = sin(pos / 10000^(2i/d))
    PE[pos, 2i+1] = cos(pos / 10000^(2i/d))

Run:  python session-01_positional_encoding.py
Creates: session-01_positional_encoding.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=3, suppress=True)


def positional_encoding(n_pos, d):
    pos = np.arange(n_pos)[:, None]
    i = np.arange(d // 2)[None, :]
    angle = pos / np.power(10000, 2 * i / d)
    pe = np.zeros((n_pos, d))
    pe[:, 0::2] = np.sin(angle)
    pe[:, 1::2] = np.cos(angle)
    return pe


pe = positional_encoding(50, 16)
print("PE shape:", pe.shape)
print("Position 0:", pe[0, :6])
print("Position 1:", pe[1, :6])

# 1) Order-blindness demo: plain self-attention (Q=K=V=X) on two word orders
def self_attend(X):
    s = X @ X.T / np.sqrt(X.shape[1])
    w = np.exp(s - s.max(1, keepdims=True)); w /= w.sum(1, keepdims=True)
    return w @ X

rng = np.random.default_rng(0)
emb = {w: rng.normal(size=16) for w in ["dog", "bites", "man"]}
a = np.stack([emb[w] for w in ["dog", "bites", "man"]])
b = np.stack([emb[w] for w in ["man", "bites", "dog"]])
out_a, out_b = self_attend(a), self_attend(b)
print("\nWithout positions, 'dog' gets the same vector in both sentences:",
      np.allclose(out_a[0], out_b[2]))
out_a, out_b = self_attend(a + pe[:3]), self_attend(b + pe[:3])
print("With positions added, the vectors differ:", not np.allclose(out_a[0], out_b[2]))

# 2) Nearby positions are more similar than distant ones
def cos(u, v): return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))
print("\nCosine similarity of position 10 with:")
for p in [9, 11, 15, 30, 49]:
    print(f"  position {p:2d}: {cos(pe[10], pe[p]):.3f}")

plt.figure(figsize=(8, 4.2))
plt.imshow(pe.T, aspect="auto", cmap="inferno", origin="lower")
plt.colorbar(label="value")
plt.xlabel("Position in the sentence"); plt.ylabel("Embedding dimension")
plt.title("Sinusoidal positional encoding (50 positions x 16 dims)")
plt.tight_layout(); plt.savefig("session-01_positional_encoding.png", dpi=110)
print("\nSaved chart: session-01_positional_encoding.png")
