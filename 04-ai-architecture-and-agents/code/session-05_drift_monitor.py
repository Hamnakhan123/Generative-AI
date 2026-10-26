"""
Session 5 · Example 1 — Monitoring a live AI pipeline for data drift with the Population Stability Index (PSI).

After deployment, the world changes: prices rise, new customer groups arrive.
PSI compares the distribution of a feature in live traffic with training data:
    PSI = sum over bins of (live% - train%) * ln(live% / train%)
Rule of thumb: < 0.10 stable · 0.10-0.25 moderate shift (watch) · > 0.25 major shift (retrain)

Run:  python session-05_drift_monitor.py
"""
import numpy as np

rng = np.random.default_rng(21)


def psi(train, live, bins=10):
    edges = np.quantile(train, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    t = np.histogram(train, edges)[0] / len(train)
    l = np.histogram(live, edges)[0] / len(live)
    t, l = np.clip(t, 1e-4, None), np.clip(l, 1e-4, None)      # avoid log(0)
    return float(np.sum((l - t) * np.log(l / t)))


def verdict(v):
    return "stable" if v < 0.10 else ("WATCH" if v < 0.25 else "RETRAIN")


# Training data for a food-delivery ETA model
train = {
    "order_value_rs": rng.normal(1500, 400, 20000),
    "distance_km": rng.gamma(2.0, 2.0, 20000),
    "hour_of_day": rng.integers(10, 24, 20000).astype(float),
}

# Four weeks of live traffic: inflation slowly raises order values; a new
# suburb opens in week 3 and lengthens distances.
weeks = {
    "week 1": dict(order_value_rs=(1500, 400), distance_shape=2.0, hours=(10, 24)),
    "week 2": dict(order_value_rs=(1560, 410), distance_shape=2.0, hours=(10, 24)),
    "week 3": dict(order_value_rs=(1650, 420), distance_shape=2.6, hours=(10, 24)),
    "week 4": dict(order_value_rs=(1800, 450), distance_shape=3.2, hours=(8, 24)),
}
print(f"{'':8s} {'order_value_rs':>16s} {'distance_km':>14s} {'hour_of_day':>14s}")
for wk, cfg in weeks.items():
    live = {
        "order_value_rs": rng.normal(*cfg["order_value_rs"], 3000),
        "distance_km": rng.gamma(cfg["distance_shape"], 2.0, 3000),
        "hour_of_day": rng.integers(*cfg["hours"], 3000).astype(float),
    }
    cells = []
    for f in train:
        v = psi(train[f], live[f])
        cells.append(f"{v:.3f} {verdict(v):>7s}")
    print(f"{wk:8s} " + " ".join(f"{c:>15s}" for c in cells))

print("\nAction: trigger the retraining pipeline (Session 4) when any feature shows RETRAIN.")
