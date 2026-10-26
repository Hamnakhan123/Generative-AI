"""
Session 1 · Mini project (full solution) — Creator Toolkit Planner.

Problem: a student society must deliver a launch pack for its annual tech
fest: a blog post, a poster, a 30-second promo reel, a narration track and a
5-slide sponsor deck. Budget: Rs 0 (free tiers only). Plan which tool category
to use, the estimated effort with and without AI, and the review step for each
deliverable, then draw a bar chart of the time saved.

Run:  python session-01_project_toolkit_planner.py
Creates: session-01_time_saved.png  (needs matplotlib: pip install matplotlib)
"""
from dataclasses import dataclass

import matplotlib
matplotlib.use("Agg")               # draw to a file, no window needed
import matplotlib.pyplot as plt


@dataclass
class Deliverable:
    name: str
    modality: str
    manual_min: int      # minutes if done fully by hand
    ai_min: int          # minutes WITH AI, including prompting
    review_min: int      # minutes a human spends checking the AI output
    review_step: str

    @property
    def total_ai(self) -> int:
        return self.ai_min + self.review_min

    @property
    def saved_pct(self) -> float:
        return 100 * (self.manual_min - self.total_ai) / self.manual_min


pack = [
    Deliverable("Blog post (600 words)", "text",   120, 25, 20, "Fact-check dates, names, sponsor list"),
    Deliverable("Event poster",          "image",  180, 30, 25, "Check spelling in the image, contrast, logo use"),
    Deliverable("30-sec promo reel",     "video",  300, 60, 40, "Watch at full speed; check captions and music licence"),
    Deliverable("Narration track",       "audio",   90, 15, 10, "Listen for mispronounced names"),
    Deliverable("5-slide sponsor deck",  "slides", 150, 30, 30, "Verify every number and the contact details"),
]

print(f"{'Deliverable':24}{'Modality':9}{'Manual':>8}{'AI+Review':>11}{'Saved':>8}  Review step")
print("-" * 110)
for d in pack:
    print(f"{d.name:24}{d.modality:9}{d.manual_min:>8}{d.total_ai:>11}{d.saved_pct:>7.0f}%  {d.review_step}")

manual = sum(d.manual_min for d in pack)
with_ai = sum(d.total_ai for d in pack)
review = sum(d.review_min for d in pack)
print("-" * 110)
print(f"Total manual: {manual} min ({manual/60:.1f} h) | with AI incl. review: {with_ai} min ({with_ai/60:.1f} h)")
print(f"Review share of AI time: {100*review/with_ai:.0f}%  -> reviewing is a real part of the job")

# Chart: grouped bars, manual vs AI+review
labels = [d.name.split(" (")[0] for d in pack]
x = range(len(pack))
plt.figure(figsize=(8, 4))
plt.bar([i - 0.2 for i in x], [d.manual_min for d in pack], width=0.4, label="Manual", color="#A78BFA")
plt.bar([i + 0.2 for i in x], [d.total_ai for d in pack], width=0.4, label="AI + review", color="#FF6B1A")
plt.xticks(list(x), labels, rotation=15)
plt.ylabel("Minutes")
plt.title("Launch pack: estimated minutes per deliverable")
plt.legend()
plt.tight_layout()
plt.savefig("session-01_time_saved.png", dpi=80)
print("Saved chart -> session-01_time_saved.png")
