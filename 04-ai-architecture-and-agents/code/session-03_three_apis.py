"""
Session 3 · Example 1 — One model, three Keras APIs: Sequential, Functional and Subclassing.

All three build the same 64 -> 32 -> 10 classifier. Pick Sequential for plain
stacks, Functional for branches/multiple inputs, Subclassing for custom logic.

Run:  python session-03_three_apis.py
"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import keras
from keras import layers

keras.utils.set_random_seed(0)

# 1) Sequential: a simple stack of layers
seq = keras.Sequential([
    keras.Input(shape=(64,)),
    layers.Dense(32, activation="relu"),
    layers.Dense(10, activation="softmax"),
], name="sequential_api")

# 2) Functional: layers are called on tensors, so graphs can branch and merge
inp = keras.Input(shape=(64,))
h = layers.Dense(32, activation="relu")(inp)
out = layers.Dense(10, activation="softmax")(h)
func = keras.Model(inp, out, name="functional_api")

# 3) Subclassing: write call() yourself (custom control flow allowed)
class Classifier(keras.Model):
    def __init__(self):
        super().__init__(name="subclassed_api")
        self.hidden = layers.Dense(32, activation="relu")
        self.out = layers.Dense(10, activation="softmax")

    def call(self, x, training=False):
        return self.out(self.hidden(x))

sub = Classifier(); sub(np.zeros((1, 64), "float32"))   # build by calling once

for m in (seq, func, sub):
    print(f"{m.name:16s} params = {m.count_params():,}")
print("Check: 64*32+32 + 32*10+10 =", 64 * 32 + 32 + 32 * 10 + 10)

# 4) A Functional model Sequential cannot express: two inputs, one output
text = keras.Input(shape=(20,), name="review_features")
meta = keras.Input(shape=(3,), name="price_stars_days")
merged = layers.concatenate([layers.Dense(16, activation="relu")(text),
                             layers.Dense(4, activation="relu")(meta)])
score = layers.Dense(1, activation="sigmoid", name="will_return")(merged)
multi = keras.Model([text, meta], score, name="two_input_model")
print("\nTwo-input model layers:")
for lyr in multi.layers:
    print(f"  {lyr.name:18s} -> output shape {lyr.output.shape}")
pred = multi.predict([np.ones((2, 20)), np.ones((2, 3))], verbose=0)
print("Prediction shape for 2 customers:", pred.shape)
