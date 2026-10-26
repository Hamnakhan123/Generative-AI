"""
Session 7 · Example 3 — When should we post? Engagement by hour and weekday.

Run:  python session-07_best_time.py   (needs session-07_posts.csv)
"""
import pandas as pd

df = pd.read_csv("session-07_posts.csv", parse_dates=["date"])
df["weekday"] = df.date.dt.day_name().str[:3]
df["ER %"] = 100 * df.engagements / df.reach

by_hour = df.groupby("hour")["ER %"].agg(["count", "mean"]).round(2)
print("Engagement rate by posting hour:")
print(by_hour.to_string())
best = by_hour["mean"].idxmax()
print(f"\nBest hour in this data: {best}:00 (n={by_hour.loc[best, 'count']} posts)")

order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
by_day = df.groupby("weekday")["reach"].mean().reindex(order).round(0)
print("\nAverage reach by weekday:")
print(by_day.to_string())
print("\nCaution: under 10 posts per group is a hint, not proof. Re-check monthly.")
