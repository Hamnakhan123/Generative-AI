"""
Session 4 · Example 3 — Make sound from numbers: a 2-second jingle.

Every audio tool, AI or not, ends up writing samples: numbers that describe
air pressure thousands of times per second. Here we synthesise a short
four-note jingle with pure maths (sine waves), add a fade in/out to avoid
clicks, save it as a WAV file with the standard library, and plot the
waveform. AI music tools do the same final step, only their numbers come
from a neural network instead of a sine formula.

Run:  python session-04_jingle.py
Creates: session-04_jingle.wav and session-04_waveform.png (matplotlib)
"""
import math
import struct
import wave

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RATE = 8000                     # samples per second (phone quality, keeps file small)
NOTES = [("C5", 523.25), ("E5", 659.25), ("G5", 783.99), ("C6", 1046.50)]
NOTE_LEN = 0.5                  # seconds per note
FADE = 0.05                     # 50 ms fade at each note edge

samples = []
for name, freq in NOTES:
    n = int(RATE * NOTE_LEN)
    for i in range(n):
        t = i / RATE
        env = min(1.0, t / FADE, (NOTE_LEN - t) / FADE)   # fade in and out
        samples.append(0.6 * env * math.sin(2 * math.pi * freq * t))

with wave.open("session-04_jingle.wav", "wb") as w:
    w.setnchannels(1)           # mono
    w.setsampwidth(2)           # 16-bit
    w.setframerate(RATE)
    w.writeframes(b"".join(struct.pack("<h", int(s * 32767)) for s in samples))

print(f"Notes: {' '.join(n for n, _ in NOTES)}")
print(f"Samples written: {len(samples)} ({len(samples)/RATE:.1f} s at {RATE} Hz)")
print(f"Peak amplitude: {max(abs(s) for s in samples):.2f} (1.0 = clipping)")
print("Saved -> session-04_jingle.wav")

# Plot the whole jingle plus a zoom on the first 10 ms to see the wave shape
fig, (a, b) = plt.subplots(2, 1, figsize=(8, 4))
a.plot([i / RATE for i in range(len(samples))], samples, color="#FF6B1A", linewidth=0.4)
a.set_title("Jingle waveform (2 s): four notes with fades")
a.set_xlabel("seconds")
zoom = int(RATE * 0.01)
b.plot([1000 * i / RATE for i in range(zoom)], samples[:zoom], color="#A78BFA", marker=".")
b.set_title("First 10 ms: a sine wave fading in")
b.set_xlabel("milliseconds")
fig.tight_layout()
fig.savefig("session-04_waveform.png", dpi=80)
print("Saved -> session-04_waveform.png")
