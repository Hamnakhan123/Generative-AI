"""
Session 4 · Mini project (full solution) — A mini TFX-style pipeline with validation gates.

Real-life problem: a lender retrains its loan-default model weekly. Broken data must never
reach production, and a new model is pushed only if it beats the serving one. Each TFX
component (ExampleGen, StatisticsGen, SchemaGen, ExampleValidator, Transform, Trainer,
Evaluator, Pusher) is a small function with the same job. Three weeks are processed.

Run:  python session-04_project_mini_tfx_pipeline.py
"""
import os, io, json, tempfile, contextlib
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import keras

keras.utils.set_random_seed(11)
SERVING_DIR = os.path.join(tempfile.mkdtemp(), "serving", "loan_default")
FEATURES = ["age", "monthly_income", "loan_amount", "years_employed"]


def make_week(seed, n=1500, broken=False):
    r = np.random.default_rng(seed)
    age = r.integers(21, 65, n).astype(float)
    income = r.lognormal(np.log(90_000), 0.5, n)
    loan = r.uniform(50_000, 1_500_000, n)
    years = np.clip(age - 21 - r.integers(0, 5, n), 0, None)
    logit = -2.2 + 2.2 * (loan / (income * 12)) - 0.04 * years - 0.01 * (age - 40)
    default = (r.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    X = np.column_stack([age, income, loan, years])
    if broken:
        X[:, 1] /= 1000                       # income sent in thousands
        X[r.random(n) < 0.08, 0] = np.nan     # 8% missing ages
    return X, default

# ---------------- components ----------------
def example_gen(X, y, seed):
    idx = np.random.default_rng(seed).permutation(len(y)); cut = int(0.8 * len(y))
    return {"train": (X[idx[:cut]], y[idx[:cut]]), "eval": (X[idx[cut:]], y[idx[cut:]])}

def statistics_gen(X):
    return {f: {"mean": float(np.nanmean(X[:, i])), "min": float(np.nanmin(X[:, i])),
                "max": float(np.nanmax(X[:, i])), "missing": float(np.isnan(X[:, i]).mean())}
            for i, f in enumerate(FEATURES)}

def schema_gen(stats):
    """Infer allowed ranges from the first (trusted) week, with 50% head-room."""
    return {f: {"min": s["min"] * 0.5, "max": s["max"] * 1.5, "max_missing": 0.0} for f, s in stats.items()}

def example_validator(stats, schema, ref_stats):
    anomalies = []
    for f in FEATURES:
        s, rule = stats[f], schema[f]
        if s["missing"] > rule["max_missing"]:
            anomalies.append(f"{f}: {s['missing']:.0%} missing")
        if s["min"] < rule["min"] or s["max"] > rule["max"]:
            anomalies.append(f"{f}: values {s['min']:.0f}..{s['max']:.0f} outside schema")
        drift = abs(s["mean"] - ref_stats[f]["mean"]) / (abs(ref_stats[f]["mean"]) + 1e-9)
        if drift > 0.25:
            anomalies.append(f"{f}: mean drifted {drift:.0%}")
    return anomalies

def transform(train_X):
    mu, sd = train_X.mean(0), train_X.std(0)
    return keras.layers.Normalization(mean=mu, variance=sd ** 2)   # becomes part of the model

def trainer(splits):
    X, y = splits["train"]
    model = keras.Sequential([keras.Input((4,)), transform(X),
                              keras.layers.Dense(16, activation="relu"),
                              keras.layers.Dense(1, activation="sigmoid")])
    model.compile("adam", "binary_crossentropy", metrics=[keras.metrics.AUC(name="auc")])
    model.fit(X, y, epochs=30, batch_size=64, verbose=0)
    return model

def evaluator(model, splits, baseline_auc, min_auc=0.70):
    X, y = splits["eval"]
    auc = float(model.evaluate(X, y, verbose=0)[1])
    blessed = auc >= min_auc and auc >= baseline_auc - 0.01      # small tolerance
    return auc, blessed

def pusher(model, version):
    path = os.path.join(SERVING_DIR, str(version))
    with contextlib.redirect_stdout(io.StringIO()):
        model.export(path)
    return path

# ---------------- pipeline run ----------------
ref_stats, schema, serving = None, None, {"version": 0, "auc": 0.0}
weeks = [("Week 1", make_week(1)), ("Week 2", make_week(2)), ("Week 3", make_week(3, broken=True))]
for name, (X, y) in weeks:
    print(f"=== {name}: {len(y)} applications, default rate {y.mean():.1%}")
    stats = statistics_gen(X)
    if schema is None:
        ref_stats, schema = stats, schema_gen(stats)
        print("  SchemaGen        : schema inferred from this trusted batch")
    anomalies = example_validator(stats, schema, ref_stats)
    if anomalies:
        print("  ExampleValidator : BLOCKED ->", "; ".join(anomalies))
        print(f"  Pusher           : skipped, production stays on v{serving['version']}\n")
        continue
    print("  ExampleValidator : no anomalies")
    splits = example_gen(X, y, seed=len(name))
    model = trainer(splits)
    auc, blessed = evaluator(model, splits, serving["auc"])
    print(f"  Trainer/Evaluator: eval AUC {auc:.3f} vs serving {serving['auc']:.3f} -> {'BLESSED' if blessed else 'not blessed'}")
    if blessed:
        version = serving["version"] + 1
        pusher(model, version)
        serving = {"version": version, "auc": auc}
        print(f"  Pusher           : exported SavedModel version {version}")
    print()

print("Versions in the serving folder:", sorted(os.listdir(SERVING_DIR)))
print("Production model:", json.dumps({"version": serving["version"], "eval_auc": round(serving["auc"], 3)}))
