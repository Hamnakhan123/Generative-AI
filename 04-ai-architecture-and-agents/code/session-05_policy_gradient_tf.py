"""
Session 5 · Example 3 — Reinforcement learning with TensorFlow: a policy-gradient (REINFORCE) agent.

Problem: an online shop can show one of 4 discount banners. Each banner has an
unknown chance of a purchase (the reward). The agent's policy is a tiny
TensorFlow network (softmax over banners). REINFORCE increases the
log-probability of actions in proportion to (reward - baseline).

Run:  python session-05_policy_gradient_tf.py
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import tensorflow as tf

tf.random.set_seed(4)
rng = np.random.default_rng(4)
BANNERS = ["5% off", "free delivery", "buy 1 get 1", "10% off"]
TRUE_RATE = np.array([0.04, 0.09, 0.06, 0.07])      # hidden from the agent

logits = tf.Variable(tf.zeros(len(BANNERS)))        # the policy's parameters
opt = tf.keras.optimizers.Adam(0.05)
baseline = 0.0

for step in range(1, 3001):
    probs = tf.nn.softmax(logits)
    a = int(rng.choice(len(BANNERS), p=probs.numpy()))
    r = float(rng.random() < TRUE_RATE[a])           # 1 = purchase
    baseline = 0.99 * baseline + 0.01 * r            # running average reward
    with tf.GradientTape() as tape:
        logp = tf.math.log(tf.nn.softmax(logits)[a])
        loss = -logp * (r - baseline)                # REINFORCE objective
    opt.apply_gradients([(tape.gradient(loss, logits), logits)])
    if step in (1, 500, 1500, 3000):
        p = tf.nn.softmax(logits).numpy()
        print(f"step {step:4d}  policy: " + "  ".join(f"{b}={x:.2f}" for b, x in zip(BANNERS, p)))

best = BANNERS[int(np.argmax(tf.nn.softmax(logits).numpy()))]
print(f"\nAgent prefers: {best} | truly best: {BANNERS[int(TRUE_RATE.argmax())]}")
print(f"Expected purchase rate of learned policy: {float(tf.nn.softmax(logits).numpy() @ TRUE_RATE):.3f} "
      f"(random policy: {TRUE_RATE.mean():.3f})")
