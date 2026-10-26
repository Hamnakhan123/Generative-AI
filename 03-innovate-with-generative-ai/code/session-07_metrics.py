"""
Session 7 · Example 1 — Compute content KPIs from a dashboard export.

Definitions used (state them in every report, because platforms differ):
  engagement rate (ER) = engagements / reach x 100
  click-through rate (CTR) = clicks / impressions x 100
  conversion rate (CVR) = sign-ups / clicks x 100
Uses pandas because real exports are CSV tables.

Run:  python session-07_make_data.py   (once, creates the CSV)
      python session-07_metrics.py
"""
import pandas as pd

df = pd.read_csv("session-07_posts.csv")
df["ER %"] = 100 * df.engagements / df.reach
df["CTR %"] = 100 * df.clicks / df.impressions
df["CVR %"] = 100 * df.signups / df.clicks.where(df.clicks > 0)

print("Overall (totals, not averages of percentages):")
print(f"  posts={len(df)}  reach={df.reach.sum():,}  ER={100*df.engagements.sum()/df.reach.sum():.2f}%  "
      f"CTR={100*df.clicks.sum()/df.impressions.sum():.2f}%  CVR={100*df.signups.sum()/df.clicks.sum():.2f}%")

by_fmt = df.groupby("format").agg(posts=("post_id", "count"), reach=("reach", "mean"),
                                  eng=("engagements", "sum"), r=("reach", "sum"))
by_fmt["ER %"] = 100 * by_fmt.eng / by_fmt.r
print("\nBy format:")
print(by_fmt[["posts", "reach", "ER %"]].round(1).sort_values("ER %", ascending=False).to_string())
