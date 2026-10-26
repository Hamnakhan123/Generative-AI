"""
Session 3 · Example 2 — A CNN in Keras on handwritten digits, with proper evaluation.

Uses scikit-learn's built-in 8x8 digits (1,797 images, no download needed).
Shows: Conv2D + pooling, compile/fit with a validation split, EarlyStopping,
then evaluate(), a confusion matrix and per-class precision/recall.

Run:  python session-03_cnn_digits.py
Creates: session-03_cnn_training.png
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import keras
from keras import layers
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

keras.utils.set_random_seed(42)
X, y = load_digits(return_X_y=True)
X = (X / 16.0).reshape(-1, 8, 8, 1).astype("float32")      # scale 0..1, add channel axis
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("train", X_tr.shape, "test", X_te.shape)

model = keras.Sequential([
    keras.Input(shape=(8, 8, 1)),
    layers.Conv2D(16, 3, padding="same", activation="relu"),   # 16 small pattern detectors
    layers.MaxPooling2D(2),                                     # 8x8 -> 4x4
    layers.Conv2D(32, 3, padding="same", activation="relu"),
    layers.Flatten(),
    layers.Dropout(0.3),
    layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
print(f"CNN parameters: {model.count_params():,}")

stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
hist = model.fit(X_tr, y_tr, validation_split=0.15, epochs=60, batch_size=32, callbacks=[stop], verbose=0)
print("epochs run:", len(hist.history["loss"]), "(early stopping)")

loss, acc = model.evaluate(X_te, y_te, verbose=0)
print(f"test loss {loss:.3f} | test accuracy {acc:.3f}")

pred = model.predict(X_te, verbose=0).argmax(1)
cm = confusion_matrix(y_te, pred)
print("\nConfusion matrix (rows = true digit, cols = predicted):")
print("    " + " ".join(f"{d:3d}" for d in range(10)))
for d, row in enumerate(cm):
    print(f"{d:3d} " + " ".join(f"{v:3d}" for v in row))
print("\n" + classification_report(y_te, pred, digits=3))

plt.figure(figsize=(7.5, 3.8))
plt.plot(hist.history["accuracy"], label="train accuracy", lw=2)
plt.plot(hist.history["val_accuracy"], label="validation accuracy", lw=2)
plt.xlabel("Epoch"); plt.ylabel("Accuracy"); plt.ylim(0, 1.02)
plt.title("CNN on 8x8 digits: learning curves"); plt.legend(); plt.grid(alpha=.3)
plt.tight_layout(); plt.savefig("session-03_cnn_training.png", dpi=110)
print("Saved chart: session-03_cnn_training.png")
