"""
Session 1 · Example 4 — Multi-head attention with Keras, and transformers vs RNNs vs CNNs.

Part A builds a real Keras MultiHeadAttention layer and a full encoder block.
Part B counts how many steps each architecture needs to connect two distant words.

Run:  python session-01_multihead_compare.py
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import keras
from keras import layers

keras.utils.set_random_seed(42)

# ---------- Part A: multi-head attention and an encoder block ----------
seq_len, d_model, heads = 10, 32, 4
x = np.random.default_rng(1).normal(size=(2, seq_len, d_model)).astype("float32")

mha = layers.MultiHeadAttention(num_heads=heads, key_dim=d_model // heads)
out, scores = mha(x, x, return_attention_scores=True)
print("Input  (batch, tokens, d_model):", x.shape)
print("Output (batch, tokens, d_model):", tuple(out.shape))
print("Scores (batch, heads, tokens, tokens):", tuple(scores.shape))
print("Each head's rows sum to 1:", np.allclose(np.asarray(scores).sum(-1), 1, atol=1e-5))


def encoder_block(inputs, d_model=32, heads=4, d_ff=64, rate=0.1):
    """Self-attention + Add&Norm + feed-forward + Add&Norm (the original encoder layer)."""
    attn = layers.MultiHeadAttention(num_heads=heads, key_dim=d_model // heads)(inputs, inputs)
    x = layers.LayerNormalization(epsilon=1e-6)(inputs + layers.Dropout(rate)(attn))
    ff = layers.Dense(d_ff, activation="relu")(x)
    ff = layers.Dense(d_model)(ff)
    return layers.LayerNormalization(epsilon=1e-6)(x + layers.Dropout(rate)(ff))


inp = keras.Input(shape=(seq_len, d_model))
model = keras.Model(inp, encoder_block(inp), name="encoder_block")
print(f"\nEncoder block parameters: {model.count_params():,}")

# ---------- Part B: path length between word 1 and word n ----------
print("\nSteps for information to travel from the first to the last token")
print(f"{'tokens':>7} | {'RNN (sequential)':>16} | {'CNN k=3 layers':>14} | {'Transformer':>11}")
for n in [10, 100, 1000]:
    rnn = n - 1                      # one hidden-state update per token, in order
    cnn = int(np.ceil((n - 1) / 2))  # each kernel-3 layer widens the view by 2
    print(f"{n:>7} | {rnn:>16} | {cnn:>14} | {1:>11}")
