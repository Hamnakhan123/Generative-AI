"""
Session 4 · Example 1 — Export a Keras model as a versioned SavedModel, the format TF Serving loads.

TF Serving loads folders like models/iris/1/ and answers POST /v1/models/iris:predict.
We export, reload without any Keras code (as a server would) and show the REST JSON.

Run:  python session-04_savedmodel_export.py
"""
import os, io, json, tempfile, contextlib
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import tensorflow as tf
import keras
from sklearn.datasets import load_iris

keras.utils.set_random_seed(3)
iris = load_iris()
X, y = iris.data.astype("float32"), iris.target
mean, std = X.mean(0), X.std(0)

# Put preprocessing INSIDE the model so clients can send raw measurements
model = keras.Sequential([
    keras.Input(shape=(4,), name="measurements"),
    keras.layers.Normalization(mean=mean, variance=std ** 2),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(3, activation="softmax"),
])
model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(X, y, epochs=200, verbose=0)
print(f"training accuracy: {model.evaluate(X, y, verbose=0)[1]:.3f}")

root = tempfile.mkdtemp()
export_dir = os.path.join(root, "models", "iris", "1")          # <model_name>/<version>
with contextlib.redirect_stdout(io.StringIO()):                  # silence the export log
    model.export(export_dir)
print("\nSavedModel folder (version 1):")
for dirpath, _, files in sorted(os.walk(export_dir)):
    rel = os.path.relpath(dirpath, root)
    for f in sorted(files):
        print(f"  {rel}/{f}")

# Reload with plain TensorFlow: no Keras class or training code needed
loaded = tf.saved_model.load(export_dir)
serve = loaded.signatures["serving_default"]
print("\nSignature inputs :", {k: v.shape for k, v in serve.structured_input_signature[1].items()})
print("Signature outputs:", {k: v.shape for k, v in serve.structured_outputs.items()})

flowers = [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3]]
out = list(serve(tf.constant(flowers, dtype=tf.float32)).values())[0].numpy()

request = {"signature_name": "serving_default", "instances": flowers}
response = {"predictions": [[round(float(v), 4) for v in row] for row in out]}
print("\nREST request body  ->", json.dumps(request))
print("REST response body <-", json.dumps(response))
for f, p in zip(flowers, out):
    print(f"  {f} -> {iris.target_names[p.argmax()]} ({p.max():.0%})")

print("\nServe it:  docker run -p 8501:8501 -v \"$PWD/models/iris:/models/iris\" -e MODEL_NAME=iris tensorflow/serving")
