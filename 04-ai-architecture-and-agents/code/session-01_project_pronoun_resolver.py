"""
Session 1 · Mini project (full solution) — Resolve "it" with self-attention.

Real-life problem: a support bot reads "The laptop did not fit in the bag because
it was too big." Which noun is "it"? Humans use meaning; transformers use
attention. Here we hand-design small feature embeddings (size, container,
object...) so that the attention pattern is easy to read, then:
  1. compute self-attention for two sentences that differ by ONE word,
  2. report which noun "it" attends to,
  3. draw both attention maps as a heatmap PNG.

Run:  python session-01_project_pronoun_resolver.py
Creates: session-01_attention_heatmap.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Feature axes: [is_object, is_container, is_big, is_small, is_pronoun, is_function_word]
VOCAB = {
    "the": [0, 0, 0, 0, 0, 1], "laptop": [1, 0, .6, .2, 0, 0], "did": [0, 0, 0, 0, 0, 1],
    "not": [0, 0, 0, 0, 0, 1], "fit": [0, 0, 0, 0, 0, .5], "in": [0, 0, 0, 0, 0, 1],
    "bag": [.3, 1, .2, .6, 0, 0], "because": [0, 0, 0, 0, 0, 1], "it": [0, 0, 0, 0, 1, 0],
    "was": [0, 0, 0, 0, 0, 1], "too": [0, 0, 0, 0, 0, 1], "big": [0, 0, 1, 0, 0, 0],
    "small": [0, 0, 0, 1, 0, 0],
}
NOUNS = {"laptop", "bag"}


def contextual_embed(words):
    """Give 'it' the meaning of the adjective that describes it (a stand-in for lower layers)."""
    E = np.array([VOCAB[w] for w in words], dtype=float)
    adj = words[-1]
    E[words.index("it")] += np.array(VOCAB[adj]) * 2   # 'it ... was too big' -> it is big
    return E


def attention(E, W_q, W_k):
    s = (E @ W_q) @ (E @ W_k).T / np.sqrt(W_q.shape[1])
    w = np.exp(s - s.max(1, keepdims=True))
    return w / w.sum(1, keepdims=True)


# Query/key projections: a big pronoun looks for an object; a small pronoun for a container
W_q = np.array([[0, 0], [0, 0], [1.2, 0], [0, 1.2], [.5, .5], [-1, -1]], dtype=float)
W_k = np.array([[1.2, 0], [0, 1.2], [.4, 0], [0, .4], [0, 0], [-1, -1]], dtype=float)

base = "the laptop did not fit in the bag because it was too".split()
results = {}
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
for ax, adj in zip(axes, ["big", "small"]):
    words = base + [adj]
    A = attention(contextual_embed(words), W_q, W_k)
    row = A[words.index("it")]
    noun_scores = {w: row[i] for i, w in enumerate(words) if w in NOUNS}
    winner = max(noun_scores, key=noun_scores.get)
    results[adj] = winner
    print(f"Sentence: {' '.join(words)}.")
    print("  attention from 'it' ->", ", ".join(f"{w}: {s:.2f}" for w, s in noun_scores.items()))
    print(f"  resolved: 'it' = the {winner}\n")
    ax.imshow(A, cmap="inferno")
    ax.set_xticks(range(len(words))); ax.set_xticklabels(words, rotation=60, fontsize=8)
    ax.set_yticks(range(len(words))); ax.set_yticklabels(words, fontsize=8)
    ax.set_title(f"'...it was too {adj}'  ->  it = {winner}")
plt.tight_layout(); plt.savefig("session-01_attention_heatmap.png", dpi=110)

assert results == {"big": "laptop", "small": "bag"}, results
print("Both sentences resolved correctly. Saved chart: session-01_attention_heatmap.png")
