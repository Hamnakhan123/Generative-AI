"""
Session 3 · Example 3 — An RNN (LSTM) in Keras that forecasts next-hour electricity demand.

Synthetic hourly demand = daily cycle + weekly cycle + noise. The model reads
the last 24 hours and predicts the next hour. We compare it with the naive
"same as last hour" baseline: a model is only useful if it beats the baseline.

Run:  python session-03_lstm_forecast.py
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import keras
from keras import layers

keras.utils.set_random_seed(1)
rng = np.random.default_rng(1)

hours = np.arange(24 * 60)                                   # 60 days of hourly data
demand = (500 + 120 * np.sin(2 * np.pi * (hours - 6) / 24)   # daily peak in the afternoon
          + 40 * np.sin(2 * np.pi * hours / (24 * 7))        # weekly pattern
          + rng.normal(0, 15, hours.size))
mu, sd = demand[:24 * 48].mean(), demand[:24 * 48].std()
z = (demand - mu) / sd

WINDOW = 24
X = np.stack([z[i:i + WINDOW] for i in range(len(z) - WINDOW)])[..., None]
y = z[WINDOW:]
split = 24 * 48 - WINDOW                                      # first 48 days train, last 12 test
X_tr, y_tr, X_te, y_te = X[:split], y[:split], X[split:], y[split:]
print("windows: train", X_tr.shape, "test", X_te.shape)

model = keras.Sequential([
    keras.Input(shape=(WINDOW, 1)),
    layers.LSTM(32),            # reads the 24 hours in order, keeps a memory state
    layers.Dense(1),
])
model.compile(optimizer=keras.optimizers.Adam(0.005), loss="mse", metrics=["mae"])
model.fit(X_tr, y_tr, epochs=15, batch_size=64, validation_split=0.1, verbose=0)

pred = model.predict(X_te, verbose=0).ravel() * sd + mu
true = y_te * sd + mu
naive = X_te[:, -1, 0] * sd + mu                               # "same as last hour"
mae = lambda a, b: float(np.mean(np.abs(a - b)))
print(f"LSTM  MAE: {mae(pred, true):6.1f} MW")
print(f"Naive MAE: {mae(naive, true):6.1f} MW")
print(f"LSTM is {100 * (1 - mae(pred, true) / mae(naive, true)):.0f}% better than the naive baseline")
print("\nFirst 6 test hours (true vs LSTM):")
for t, p in zip(true[:6], pred[:6]):
    print(f"  {t:6.1f}  {p:6.1f}")
print(f"\nLSTM parameters: {model.count_params():,}  (4 gates x (32*(32+1)+32) + dense)")
