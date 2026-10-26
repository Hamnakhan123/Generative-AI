"""
Session 7 · Data helper — create a SYNTHETIC posts dataset for the examples.

The numbers are invented by a seeded random generator (so everyone gets the
same file); they mimic the columns a social-media dashboard exports.
Run this first:  python session-07_make_data.py
Creates: session-07_posts.csv
"""
import csv
import random
from datetime import date, timedelta

rng = random.Random(42)
FORMATS = {"reel": (1.6, 0.050), "carousel": (1.1, 0.045), "image": (0.8, 0.030), "text": (0.5, 0.020)}
TOPICS = ["admissions", "student life", "research", "events", "tips"]
start = date(2026, 9, 1)

rows = []
for i in range(60):
    fmt = rng.choice(list(FORMATS))
    reach_mult, base_eng = FORMATS[fmt]
    day = start + timedelta(days=i)
    hour = rng.choice([9, 13, 17, 20])
    boost = 1.3 if hour in (17, 20) else 1.0           # evenings do better in this fake audience
    reach = int(rng.gauss(2000, 400) * reach_mult * boost)
    engagements = int(reach * base_eng * rng.uniform(0.7, 1.3))
    clicks = int(reach * rng.uniform(0.004, 0.015))
    signups = int(clicks * rng.uniform(0.02, 0.10))
    rows.append({"post_id": f"P{i+1:02}", "date": day.isoformat(), "hour": hour, "format": fmt,
                 "topic": rng.choice(TOPICS), "impressions": int(reach * 1.4), "reach": reach,
                 "engagements": engagements, "clicks": clicks, "signups": signups})

with open("session-07_posts.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {len(rows)} synthetic posts -> session-07_posts.csv")
print("Columns:", ", ".join(rows[0].keys()))
print("First row:", rows[0])
