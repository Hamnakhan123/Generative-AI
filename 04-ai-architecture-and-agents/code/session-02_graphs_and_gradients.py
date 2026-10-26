"""
Session 2 · Example 2 — Computational graphs with tf.function and automatic differentiation.

TensorFlow 2 runs eagerly (line by line, like NumPy). Wrapping a Python
function in @tf.function TRACES it once into a graph that TF can optimise,
save and run on other devices. tf.GradientTape records operations so TF can
compute derivatives by the chain rule (backpropagation).

Run:  python session-02_graphs_and_gradients.py
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

# 1) A graph is traced once per input signature
trace_count = 0

@tf.function
def affine(x, w, b):
    global trace_count
    trace_count += 1          # Python side effect: runs only while tracing
    return tf.matmul(x, w) + b

x = tf.ones([4, 3]); w = tf.ones([3, 2]); b = tf.zeros([2])
for _ in range(3):
    affine(x, w, b)
print("Called 3 times with the same shape -> traced", trace_count, "time(s)")
affine(tf.ones([8, 3]), w, b)
print("Called with a new shape          -> traced", trace_count, "time(s)")

graph = affine.get_concrete_function(x, w, b).graph
ops = [op.type for op in graph.get_operations()]
print("Ops inside the graph:", [o for o in ops if o not in ("Placeholder", "NoOp", "Identity")])

# 2) Gradients: y = x^3 + 2x at x = 2  ->  dy/dx = 3x^2 + 2 = 14
x = tf.Variable(2.0)
with tf.GradientTape() as tape:
    y = x ** 3 + 2 * x
print("\ny =", float(y), "| dy/dx =", float(tape.gradient(y, x)))

# 3) Chain rule through a tiny network: loss = (sigmoid(w*x + b) - target)^2
w, b = tf.Variable(0.5), tf.Variable(0.0)
xin, target = tf.constant(2.0), tf.constant(1.0)
with tf.GradientTape() as tape:
    z = w * xin + b
    pred = tf.sigmoid(z)
    loss = (pred - target) ** 2
dw, db = tape.gradient(loss, [w, b])
print(f"pred={float(pred):.4f} loss={float(loss):.4f} dL/dw={float(dw):.4f} dL/db={float(db):.4f}")
# check by hand: dL/dz = 2(pred-target)*pred*(1-pred); dL/dw = dL/dz * x
dz = 2 * (float(pred) - 1) * float(pred) * (1 - float(pred))
print(f"by hand:                    dL/dw={dz*2:.4f} dL/db={dz:.4f}")

# 4) One gradient-descent step lowers the loss
lr = 0.5
w.assign_sub(lr * dw); b.assign_sub(lr * db)
new_loss = (tf.sigmoid(w * xin + b) - target) ** 2
print(f"after one step: loss {float(loss):.4f} -> {float(new_loss):.4f}")

# 5) TF1 'sessions' vs TF2: the same graph, now run by calling the function
print("\nTF1 style: build graph, then sess.run(fetches, feed_dict)")
print("TF2 style: result = my_tf_function(inputs)  # session handled for you")
