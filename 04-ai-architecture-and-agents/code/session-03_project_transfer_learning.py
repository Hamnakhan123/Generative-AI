"""
Session 3 · Mini project (full solution) — Transfer learning when labels are scarce.

Real-life problem: a bank's cheque reader was trained on thousands of clean
digit scans. A new branch installs a cheaper scanner whose images are noisy,
blurred and shifted, and only 3 labelled examples per digit exist (30 images).
We:
  1. pre-train a CNN on the clean scans (the "source" task),
  2. measure it as-is, then reuse its frozen base with a new head,
  3. fine-tune the whole pre-trained network with a tiny learning rate,
  4. compare against training the same CNN from scratch on the 30 images.
This is what keras.applications (MobileNetV2, ResNet50 ... pre-trained on
ImageNet) does at large scale.

Run:  python session-03_project_transfer_learning.py
Creates: session-03_transfer_learning.png
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import keras
from keras import layers
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

keras.utils.set_random_seed(7)
rng = np.random.default_rng(7)
X, y = load_digits(return_X_y=True)
X = (X / 16.0).reshape(-1, 8, 8, 1).astype("float32")
X_src, X_new, y_src, y_new = train_test_split(X, y, test_size=0.5, random_state=7, stratify=y)


def new_scanner(imgs):
    """Simulate the cheap scanner: blur, shift by one pixel, add noise, lower contrast."""
    out = imgs.copy()
    out = (out + np.roll(out, 1, axis=2) + np.roll(out, 1, axis=1)) / 3     # blur + smear
    out = np.roll(out, rng.choice([-1, 1]), axis=2)                          # shift
    out = 0.8 * out + 0.1 + rng.normal(0, 0.08, out.shape)                   # contrast + noise
    return np.clip(out, 0, 1).astype("float32")


X_new = new_scanner(X_new)
few = np.concatenate([np.where(y_new == d)[0][:3] for d in range(10)])      # 3 per digit
test = np.setdiff1d(np.arange(len(y_new)), few)
print(f"clean source scans: {len(y_src)} | new-scanner labelled: {len(few)} | new-scanner test: {len(test)}")


def conv_base():
    return keras.Sequential([
        keras.Input(shape=(8, 8, 1)),
        layers.Conv2D(16, 3, padding="same", activation="relu"),
        layers.MaxPooling2D(2),
        layers.Conv2D(32, 3, padding="same", activation="relu"),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
    ], name="conv_base")


def acc(model):
    return float(model.evaluate(X_new[test], y_new[test], verbose=0)[1])

# 1) Pre-train on clean scans, with augmentation (shifts + noise) so features are robust
base = conv_base()
augment = keras.Sequential([layers.RandomTranslation(0.15, 0.15), layers.GaussianNoise(0.1)])  # train-time only
source_model = keras.Sequential([keras.Input(shape=(8, 8, 1)), augment, base, layers.Dense(10, activation="softmax")])
source_model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
source_model.fit(X_src, y_src, epochs=60, batch_size=32, verbose=0)
acc_asis = acc(source_model)
print(f"0) clean-scan model used as-is on the new scanner: {acc_asis:.3f}")

# 2) Feature extraction: freeze the base, train only a new head on 30 images
base.trainable = False
tl = keras.Sequential([base, layers.Dense(10, activation="softmax")])
tl.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
tl.fit(X_new[few], y_new[few], epochs=150, batch_size=10, verbose=0)
acc_frozen = acc(tl)
print(f"1) frozen base + new head : {acc_frozen:.3f}")

# 3) Fine-tuning: start from the full pre-trained model (same 10 classes, so keep its head),
#    unfreeze everything and train on the 30 new images with a much smaller learning rate
base.trainable = True
source_model.compile(keras.optimizers.Adam(1e-4), "sparse_categorical_crossentropy", metrics=["accuracy"])
source_model.fit(X_new[few], y_new[few], epochs=60, batch_size=10, verbose=0)
acc_ft = acc(source_model)
print(f"2) fine-tuned full model  : {acc_ft:.3f}")

# 4) Baseline: same architecture, random weights, same 30 images
scratch = keras.Sequential([conv_base(), layers.Dense(10, activation="softmax")])
scratch.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
scratch.fit(X_new[few], y_new[few], epochs=150, batch_size=10, verbose=0)
acc_scratch = acc(scratch)
print(f"3) from scratch (baseline): {acc_scratch:.3f}")
print(f"\nFine-tuned transfer vs scratch: {100 * (acc_ft - acc_scratch):+.1f} percentage points")

names = ["From scratch", "Frozen base\n+ new head", "Pre-trained\nas-is", "Fine-tuned"]
vals = [acc_scratch, acc_frozen, acc_asis, acc_ft]
plt.figure(figsize=(7.5, 4.2))
bars = plt.bar(names, vals, color=["#A78BFA", "#FCD34D", "#F43F5E", "#FF6B1A"])
for b_, v in zip(bars, vals):
    plt.text(b_.get_x() + b_.get_width() / 2, v + 0.01, f"{v:.2f}", ha="center")
plt.ylim(0, 1.05); plt.ylabel("Accuracy on new-scanner test images")
plt.title("30 labelled images: transfer learning vs scratch")
plt.tight_layout(); plt.savefig("session-03_transfer_learning.png", dpi=110)
print("Saved chart: session-03_transfer_learning.png")
