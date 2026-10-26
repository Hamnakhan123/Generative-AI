"""
Session 4 · Example 2 — Convert a Keras model to TensorFlow Lite, quantise it and run it with the interpreter.

TF Lite (LiteRT) runs models on phones and microcontrollers; dynamic-range
quantisation stores weights as int8 (about 4x smaller).

Run:  python session-04_tflite_convert.py
"""
import os, io, contextlib
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import tensorflow as tf
import keras
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

keras.utils.set_random_seed(5)
X, y = load_digits(return_X_y=True)
X = (X / 16.0).astype("float32")
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=5, stratify=y)

model = keras.Sequential([
    keras.Input(shape=(64,)),
    keras.layers.Dense(256, activation="relu"),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(10, activation="softmax"),
])
model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(X_tr, y_tr, epochs=25, batch_size=32, verbose=0)
keras_acc = model.evaluate(X_te, y_te, verbose=0)[1]
print(f"Keras model: {model.count_params():,} params | test accuracy {keras_acc:.4f}")


def convert(quantize):
    conv = tf.lite.TFLiteConverter.from_keras_model(model)
    if quantize:
        conv.optimizations = [tf.lite.Optimize.DEFAULT]      # dynamic-range int8 weights
    with contextlib.redirect_stdout(io.StringIO()):
        return conv.convert()


def tflite_predict(blob, data):
    interp = tf.lite.Interpreter(model_content=blob)
    inp = interp.get_input_details()[0]; out = interp.get_output_details()[0]
    interp.resize_tensor_input(inp["index"], data.shape); interp.allocate_tensors()
    interp.set_tensor(inp["index"], data); interp.invoke()
    return interp.get_tensor(out["index"])


keras_pred = model.predict(X_te, verbose=0).argmax(1)
print(f"\n{'format':22s} {'size KB':>8s} {'accuracy':>9s} {'agrees with Keras':>18s}")
sizes = {}
for name, q in [("TFLite float32", False), ("TFLite dynamic int8", True)]:
    blob = convert(q)
    pred = tflite_predict(blob, X_te).argmax(1)
    sizes[name] = len(blob) / 1024
    print(f"{name:22s} {sizes[name]:8.1f} {np.mean(pred == y_te):9.4f} {np.mean(pred == keras_pred):17.1%}")
print(f"\nQuantised model is {sizes['TFLite float32'] / sizes['TFLite dynamic int8']:.1f}x smaller.")

# Raw weight storage, for intuition
n = model.count_params()
print(f"Weights alone: {n * 4 / 1024:.1f} KB as float32 vs {n / 1024:.1f} KB as int8")
