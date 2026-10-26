"""
Session 5 · Example 4 — What TensorFlow Quantum does, simulated with NumPy: a one-qubit variational classifier.

A quantum ML model is a circuit with tunable rotation angles (parameters).
Data is encoded as a rotation, a trainable rotation follows, and we measure
the expectation <Z> in [-1, 1]. A classical optimiser tunes the angle using the
parameter-shift rule:  d<Z>/dθ = (<Z>(θ + π/2) - <Z>(θ - π/2)) / 2
TensorFlow Quantum wraps exactly this loop (circuits from Cirq as Keras layers).

Run:  python session-05_quantum_toy.py
"""
import numpy as np

rng = np.random.default_rng(8)


def ry(angle):
    """Single-qubit rotation about the Y axis."""
    c, s = np.cos(angle / 2), np.sin(angle / 2)
    return np.array([[c, -s], [s, c]])


def expect_z(x, theta):
    state = ry(theta) @ ry(x) @ np.array([1.0, 0.0])     # start in |0>, encode x, apply θ
    return float(state[0] ** 2 - state[1] ** 2)          # <Z> = P(0) - P(1)


# Data: class +1 near angle 0.3, class -1 near angle 2.6 (e.g. two sensor states)
x = np.concatenate([rng.normal(0.3, 0.25, 40), rng.normal(2.6, 0.25, 40)])
y = np.concatenate([np.ones(40), -np.ones(40)])
# Shift the data so the untrained circuit is poor: the classifier must learn θ
x = x + 1.4

theta, lr = 0.0, 0.3
for epoch in range(31):
    preds = np.array([expect_z(xi, theta) for xi in x])
    loss = np.mean((preds - y) ** 2)
    grad = np.mean([2 * (expect_z(xi, theta) - yi) *
                    (expect_z(xi, theta + np.pi / 2) - expect_z(xi, theta - np.pi / 2)) / 2
                    for xi, yi in zip(x, y)])
    if epoch % 10 == 0:
        acc = np.mean(np.sign(preds) == y)
        print(f"epoch {epoch:2d}  theta={theta:+.3f}  loss={loss:.3f}  accuracy={acc:.2f}")
    theta -= lr * grad

print(f"\nLearned rotation θ = {theta:.3f} rad (ideal ≈ -1.40, undoing the shift)")
print("Simulating n qubits needs 2^n amplitudes:", {n: 2 ** n for n in (1, 10, 30, 50)})
