"""
Session 3 · Example 1 — Build image prompts from parts, plus pixel sizes.

Image generators respond best to a prompt that names, in order:
subject -> setting -> style -> lighting -> composition -> colour palette,
plus an aspect ratio and a "negative prompt" (things to avoid).
This script builds such prompts and converts aspect ratios into pixel sizes
for common uses (posters, slides, stories).

Run:  python session-03_image_prompt_builder.py
"""
from math import gcd


def image_prompt(subject, setting, style, lighting, composition, palette,
                 ratio="1:1", avoid=()):
    parts = [subject, setting, f"{style} style", f"{lighting} lighting",
             composition, f"colour palette: {palette}"]
    prompt = ", ".join(p for p in parts if p)
    prompt += f" --ar {ratio}"
    if avoid:
        prompt += "\nNegative prompt: " + ", ".join(avoid)
    return prompt


def pixels(ratio: str, long_side: int) -> tuple:
    """Width and height for a ratio like '16:9' when the longer side is long_side px."""
    w, h = map(int, ratio.split(":"))
    if w >= h:
        return long_side, round(long_side * h / w)
    return round(long_side * w / h), long_side


basic = image_prompt("a robot reading a book", "", "cartoon", "soft", "", "pastel")
advanced = image_prompt(
    subject="a young woman coding on a laptop, smiling, wearing a dupatta",
    setting="rooftop in Karachi at dusk, city lights behind",
    style="flat vector illustration",
    lighting="warm golden-hour",
    composition="subject on the left third, empty space on the right for a headline",
    palette="deep navy, fire orange, gold",
    ratio="4:5",
    avoid=("text", "watermark", "extra fingers", "distorted face"),
)
print("BASIC PROMPT\n" + basic)
print("\nADVANCED PROMPT\n" + advanced)

print("\nASPECT RATIO -> PIXELS (long side 1920 px)")
for use, ratio in [("Slide / YouTube thumbnail", "16:9"), ("Instagram portrait post", "4:5"),
                   ("Story / Reel", "9:16"), ("Square post", "1:1"), ("A-series poster", "1:1.414")]:
    if "." in ratio:  # A-series paper is 1 : square root of 2
        w, h = round(1920 / 1.414), 1920
    else:
        w, h = pixels(ratio, 1920)
    g = gcd(w, h)
    print(f"  {use:26} {ratio:8} -> {w} x {h} px  (simplest ratio {w//g}:{h//g})")
