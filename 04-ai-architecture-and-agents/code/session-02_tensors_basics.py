"""
Session 2 · Example 1 — Tensors: creating, shaping, broadcasting and Variables in TensorFlow.

A tensor is an n-dimensional array with a dtype and a shape. Every image batch,
sentence batch and weight matrix in a neural network is a tensor.

Run:  python session-02_tensors_basics.py
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

print("TensorFlow", tf.__version__, "| eager mode:", tf.executing_eagerly())

# 1) Rank 0..3 tensors
scalar = tf.constant(7)
vector = tf.constant([1.0, 2.0, 3.0])
matrix = tf.constant([[1, 2], [3, 4]], dtype=tf.float32)
batch = tf.zeros([2, 28, 28])            # e.g. 2 grey images of 28x28
for name, t in [("scalar", scalar), ("vector", vector), ("matrix", matrix), ("batch", batch)]:
    print(f"{name:7s} rank={t.ndim} shape={t.shape} dtype={t.dtype.name}")

# 2) Element-wise ops vs matrix multiplication
a = tf.constant([[1., 2.], [3., 4.]])
b = tf.constant([[5., 6.], [7., 8.]])
print("\na * b (element-wise):\n", (a * b).numpy())
print("a @ b (matmul):\n", tf.matmul(a, b).numpy())

# 3) Broadcasting: add a bias vector to every row of a batch
x = tf.reshape(tf.range(6, dtype=tf.float32), [3, 2])
bias = tf.constant([10., 100.])
print("\nx:\n", x.numpy(), "\nx + bias:\n", (x + bias).numpy())

# 4) Reductions and reshaping
scores = tf.constant([[2., 9., 4.], [7., 1., 8.]])
print("\nsum all:", float(tf.reduce_sum(scores)), "| mean per row:", tf.reduce_mean(scores, axis=1).numpy())
print("argmax per row:", tf.argmax(scores, axis=1).numpy(), "| softmax row 0:", tf.nn.softmax(scores[0]).numpy().round(3))
print("reshape (2,3)->(3,2):", tf.reshape(scores, [3, 2]).shape, "| transpose:", tf.transpose(scores).shape)

# 5) Casting: TF does NOT silently mix int and float
try:
    tf.constant(1) + tf.constant(1.5)
except Exception as e:
    print("\nMixing int32 + float32 ->", type(e).__name__)
print("After tf.cast:", float(tf.cast(tf.constant(1), tf.float32) + 1.5))

# 6) Tensors are immutable; Variables hold trainable state
w = tf.Variable([[0.5], [-0.5]])
w.assign_add([[0.1], [0.1]])
print("\nVariable after assign_add:", w.numpy().ravel(), "| trainable:", w.trainable)

# 7) NumPy interop
import numpy as np
n = np.array([1, 2, 3]); t = tf.convert_to_tensor(n)
print("NumPy -> tensor -> NumPy:", t.numpy(), type(t.numpy()).__name__)
