"""
Session 5 · Example 1 — Plan a story's structure before asking AI to write it.

Most stories follow a shape. The classic five-stage arc (exposition, rising
action, climax, falling action, resolution) can be given a share of the total
length. Asking the AI for "a 1,500-word story" gives a saggy middle; asking
for each stage with a word budget and a tension level gives a planned arc.

Run:  python session-05_story_arc.py
Creates: session-05_tension_curve.png   (matplotlib)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TOTAL_WORDS = 1500
ARC = [  # stage, share of words, tension at the END of the stage (0-10), what happens
    ("Exposition",     0.15, 2, "Meet Ayesha, a CS student who builds a homework-helper bot"),
    ("Rising action",  0.40, 7, "The bot starts writing her friends' assignments; a teacher grows suspicious"),
    ("Climax",         0.15, 10, "Ayesha must choose: shut the bot down or let a friend take the blame"),
    ("Falling action", 0.20, 5, "She confesses and redesigns the bot to give hints, not answers"),
    ("Resolution",     0.10, 3, "The tutor-bot wins the campus innovation prize"),
]

start, points = 0, [(0, 1)]
print(f"{'Stage':15}{'Words':>6}{'Range':>13}{'Tension':>8}  Beat")
for stage, share, tension, beat in ARC:
    words = round(TOTAL_WORDS * share)
    print(f"{stage:15}{words:6}{start:>6}-{start + words:<6}{tension:>8}  {beat}")
    start += words
    points.append((start, tension))
print(f"Total: {start} words")

xs, ys = zip(*points)
plt.figure(figsize=(8, 3.5))
plt.plot(xs, ys, marker="o", color="#FF6B1A", linewidth=2)
for (stage, *_), x, y in zip(ARC, xs[1:], ys[1:]):
    plt.annotate(stage, (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
plt.ylim(0, 11.5)
plt.xlabel("Word position in the story")
plt.ylabel("Tension (0-10)")
plt.title("Planned tension curve")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("session-05_tension_curve.png", dpi=80)
print("Saved -> session-05_tension_curve.png")
