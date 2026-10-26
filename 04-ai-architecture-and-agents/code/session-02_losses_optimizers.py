"""
Session 2 · Example 3 — Loss functions by hand vs tf.keras.losses, and optimisers compared.

Run:  python session-02_losses_optimizers.py
Creates: session-02_optimizers.png
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1) Regression loss: Mean Squared Error and Mean Absolute Error
y_true = np.array([3.0, 5.0, 2.0]); y_pred = np.array([2.5, 5.5, 4.0])
mse = np.mean((y_true - y_pred) ** 2); mae = np.mean(np.abs(y_true - y_pred))
print(f"MSE by hand {mse:.4f} | Keras {float(tf.keras.losses.MeanSquaredError()(y_true, y_pred)):.4f}")
print(f"MAE by hand {mae:.4f} | Keras {float(tf.keras.losses.MeanAbsoluteError()(y_true, y_pred)):.4f}")

# 2) Binary cross-entropy: punishes confident wrong answers hard
t = np.array([1., 0., 1.]); p = np.array([0.9, 0.2, 0.6])
bce = -np.mean(t * np.log(p) + (1 - t) * np.log(1 - p))
print(f"BCE by hand {bce:.4f} | Keras {float(tf.keras.losses.BinaryCrossentropy()(t, p)):.4f}")
for prob in [0.9, 0.5, 0.1, 0.01]:
    print(f"  true=1, predicted {prob:<4} -> loss {-np.log(prob):.3f}")

# 3) Categorical cross-entropy with integer labels (3 classes)
labels = np.array([0, 2]); probs = np.array([[0.7, 0.2, 0.1], [0.1, 0.3, 0.6]])
cce = -np.mean(np.log(probs[np.arange(2), labels]))
print(f"Sparse CCE by hand {cce:.4f} | Keras {float(tf.keras.losses.SparseCategoricalCrossentropy()(labels, probs)):.4f}")

# 4) Optimisers on a stretched bowl f(x,y) = x^2 + 10*y^2, starting at (-4, 2)
def run(opt, steps=60):
    v = tf.Variable([-4.0, 2.0]); hist = []
    for _ in range(steps):
        with tf.GradientTape() as tape:
            loss = v[0] ** 2 + 10 * v[1] ** 2
        opt.apply_gradients([(tape.gradient(loss, v), v)])
        hist.append(float(loss))
    return hist

opts = {
    "SGD lr=0.02": tf.keras.optimizers.SGD(0.02),
    "SGD+momentum": tf.keras.optimizers.SGD(0.02, momentum=0.9),
    "RMSprop lr=0.1": tf.keras.optimizers.RMSprop(0.1),
    "Adam lr=0.3": tf.keras.optimizers.Adam(0.3),
}
print("\nLoss after 10 / 30 / 60 steps (start = 56.0)")
plt.figure(figsize=(7.5, 4.2))
for name, opt in opts.items():
    h = run(opt)
    print(f"  {name:15s} {h[9]:9.4f} {h[29]:9.4f} {h[59]:9.5f}")
    plt.plot(h, label=name, lw=2)
plt.yscale("log"); plt.xlabel("Step"); plt.ylabel("Loss (log scale)")
plt.title("Optimisers minimising x^2 + 10y^2"); plt.legend(); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig("session-02_optimizers.png", dpi=110)
print("Saved chart: session-02_optimizers.png")
