"""Aspect ratio -> pixel sizes, and what an upscale does to resolution."""
from math import gcd, sqrt
BASE_PIXELS = 1024 * 1024        # typical base image area (~1 megapixel)
uses = {"1:1": "profile pics, icons", "4:5": "Instagram portrait", "16:9": "YouTube thumbnail, slides",
        "9:16": "Reels/Shorts/Stories", "3:2": "classic photo print", "21:9": "cinematic banner"}
print(f"{'Ratio':6} {'Width':>6} x {'Height':<6} {'Upscaled 2x':>14}   Best for")
for ratio, use in uses.items():
    w, h = map(int, ratio.split(":"))
    scale = sqrt(BASE_PIXELS / (w * h))
    W, H = round(w * scale / 8) * 8, round(h * scale / 8) * 8   # snap to multiples of 8
    print(f"{ratio:6} {W:>6} x {H:<6} {W*2:>6} x {H*2:<6}   {use}")
w, h = 1920, 1080
g = gcd(w, h)
print(f"\n1920x1080 simplifies to {w//g}:{h//g}")
