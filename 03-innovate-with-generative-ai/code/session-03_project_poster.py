"""
Session 3 · Mini project (full solution) — Generate an event poster in code.

Real-life problem: image generators often misspell text inside images.
A reliable workflow is: let AI make the ARTWORK, then add the TEXT yourself
in a design tool. This script plays the "design tool" role: it lays out a
4:5 Instagram poster with a headline, details and a call to action, checks
every text colour for WCAG contrast first, and saves a PNG.

Run:  python session-03_project_poster.py
Creates: session-03_poster.png   (needs matplotlib)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch


def luminance(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    l1, l2 = sorted((luminance(a), luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


SPEC = {
    "bg": "#0A0716",
    "headline": ("CODE THE FUTURE", "#FCD34D", 30),
    "sub": ("Inter-university AI Hackathon", "#F5EEFF", 15),
    "details": ("Sat 14 Nov  |  9 am - 9 pm  |  Main Auditorium", "#F5EEFF", 11),
    "cta": ("Register free: scan the QR at the info desk", "#0A0716", 11),
    "cta_bg": "#FF6B1A",
}

# 1) Quality gate: every text/background pair must pass before we draw.
checks = [("headline", SPEC["headline"][1], SPEC["bg"], 3.0),
          ("sub", SPEC["sub"][1], SPEC["bg"], 4.5),
          ("details", SPEC["details"][1], SPEC["bg"], 4.5),
          ("cta", SPEC["cta"][1], SPEC["cta_bg"], 4.5)]
for name, fg, bg, need in checks:
    r = contrast(fg, bg)
    print(f"{name:9} contrast {r:5.2f} (needs {need}) -> {'PASS' if r >= need else 'FAIL'}")
    assert r >= need, f"{name} is not readable; pick another colour"

# 2) Draw the poster: 4:5 portrait, 4 x 5 inches at 120 dpi = 480 x 600 px.
fig = plt.figure(figsize=(4, 5), dpi=120)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 4); ax.set_ylim(0, 5); ax.axis("off")
fig.patch.set_facecolor(SPEC["bg"])
# "artwork" placeholder: glowing circles where AI-generated art would sit
for r, a in [(1.6, 0.10), (1.15, 0.18), (0.75, 0.35)]:
    ax.add_patch(Circle((2, 3.35), r, color="#FF6B1A", alpha=a))
ax.add_patch(Circle((2, 3.35), 0.45, color="#F43F5E", alpha=0.8))
text, colour, size = SPEC["headline"]
ax.text(2, 1.95, text, ha="center", color=colour, fontsize=size * 0.8, weight="bold")
for key, y in (("sub", 1.55), ("details", 1.2)):
    t, c, s = SPEC[key]
    ax.text(2, y, t, ha="center", color=c, fontsize=s * 0.8)
ax.add_patch(FancyBboxPatch((0.35, 0.45), 3.3, 0.45, boxstyle="round,pad=0.05", color=SPEC["cta_bg"]))
t, c, s = SPEC["cta"]
ax.text(2, 0.62, t, ha="center", color=c, fontsize=s * 0.75, weight="bold")
fig.savefig("session-03_poster.png", facecolor=SPEC["bg"])
w, h = fig.get_size_inches() * fig.dpi
print(f"Saved poster -> session-03_poster.png ({int(w)} x {int(h)} px, ratio 4:5)")
