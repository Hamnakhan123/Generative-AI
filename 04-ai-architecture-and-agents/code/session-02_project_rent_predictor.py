"""
Session 2 · Mini project (full solution) — Rent predictor trained with a custom TF loop, then PyTorch.

Real-life problem: a student housing office wants a quick estimate of monthly
rent (thousand Rs) from flat size (100 sq ft units), distance to campus (km)
and number of rooms. We:
  1. generate a realistic synthetic dataset with a known formula + noise,
  2. standardise features and train a linear model with tf.GradientTape + Adam,
  3. report learned weights, train/test RMSE and a sample prediction,
  4. train the same model in PyTorch to compare the two frameworks side by side.

Run:  python session-02_project_rent_predictor.py
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import tensorflow as tf
import torch

rng = np.random.default_rng(42)
tf.random.set_seed(42); torch.manual_seed(42)

# 1) Data: rent = 8 + 4*size - 1.5*distance + 3*rooms + noise
n = 400
size = rng.uniform(4, 15, n); dist = rng.uniform(0.5, 20, n); rooms = rng.integers(1, 5, n)
rent = 8 + 4 * size - 1.5 * dist + 3 * rooms + rng.normal(0, 3, n)
X = np.column_stack([size, dist, rooms]).astype("float32"); y = rent.astype("float32")
idx = rng.permutation(n); tr, te = idx[:320], idx[320:]
mu, sd = X[tr].mean(0), X[tr].std(0)
Xs = (X - mu) / sd

# 2) TensorFlow: explicit training loop
W = tf.Variable(tf.zeros([3])); b = tf.Variable(0.0)
opt = tf.keras.optimizers.Adam(0.5)

@tf.function
def train_step(xb, yb):
    with tf.GradientTape() as tape:
        pred = tf.linalg.matvec(xb, W) + b
        loss = tf.reduce_mean((pred - yb) ** 2)
    opt.apply_gradients(zip(tape.gradient(loss, [W, b]), [W, b]))
    return loss

for epoch in range(300):
    loss = train_step(Xs[tr], y[tr])
    if epoch in (0, 49, 299):
        print(f"[TF] epoch {epoch+1:3d}  train MSE {float(loss):8.3f}")

def rmse(pred, target): return float(np.sqrt(np.mean((pred - target) ** 2)))
tf_pred = Xs @ W.numpy() + b.numpy()
w_raw = W.numpy() / sd; b_raw = b.numpy() - (W.numpy() * mu / sd).sum()
print(f"[TF] test RMSE {rmse(tf_pred[te], y[te]):.2f} thousand Rs")
print("[TF] learned formula: rent = {:.2f} + {:.2f}*size {:+.2f}*km {:+.2f}*rooms".format(b_raw, *w_raw))
print("     true formula:    rent = 8.00 + 4.00*size -1.50*km +3.00*rooms")

flat = np.array([[9.0, 3.0, 2]], dtype="float32")   # 900 sq ft, 3 km, 2 rooms
print(f"[TF] estimate for 900 sq ft, 3 km, 2 rooms: Rs {(((flat-mu)/sd) @ W.numpy() + b.numpy()).item()*1000:,.0f}")

# 3) PyTorch: same model, same data, same optimiser
model = torch.nn.Linear(3, 1)
topt = torch.optim.Adam(model.parameters(), lr=0.5)
xt, yt = torch.tensor(Xs[tr]), torch.tensor(y[tr]).unsqueeze(1)
for epoch in range(300):
    topt.zero_grad()
    loss = torch.mean((model(xt) - yt) ** 2)
    loss.backward(); topt.step()
with torch.no_grad():
    pt_pred = model(torch.tensor(Xs)).squeeze(1).numpy()
print(f"\n[PyTorch] test RMSE {rmse(pt_pred[te], y[te]):.2f} thousand Rs")
print(f"Largest TF vs PyTorch difference on a test flat: Rs {abs(pt_pred[te]-tf_pred[te]).max()*1000:.2f}")
