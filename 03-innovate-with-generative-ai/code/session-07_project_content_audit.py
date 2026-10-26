"""
Session 7 · Mini project (full solution) — A monthly content audit.

Real-life problem: the department's social media lead asks: "What worked
in September, what didn't, and what should we change in October?"
This script answers with data, then builds a prompt so an AI assistant can
turn the numbers into a short written report. Numbers come from code, the
WORDS come from AI, and a human checks both.

Steps:
  1. load and clean the export          4. compare formats and topics
  2. compute KPIs per post              5. chart ER by format (PNG)
  3. top 3 / bottom 3 posts             6. rule-based recommendations + AI prompt

Run:  python session-07_make_data.py  (once)
      python session-07_project_content_audit.py
Creates: session-07_er_by_format.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# 1) load and clean
df = pd.read_csv("session-07_posts.csv")
before = len(df)
df = df[(df.reach > 0) & (df.impressions >= df.reach)].copy()   # impossible rows removed
print(f"Loaded {before} posts, {before - len(df)} removed as invalid")

# 2) KPIs
df["ER"] = 100 * df.engagements / df.reach
df["CTR"] = 100 * df.clicks / df.impressions

# 3) best and worst
cols = ["post_id", "format", "topic", "hour", "reach", "ER"]
print("\nTop 3 posts by engagement rate:")
print(df.nlargest(3, "ER")[cols].round(2).to_string(index=False))
print("\nBottom 3 posts by engagement rate:")
print(df.nsmallest(3, "ER")[cols].round(2).to_string(index=False))

# 4) format and topic comparison (rates from totals)
def rate_table(key):
    g = df.groupby(key)[["engagements", "reach", "clicks", "impressions", "signups"]].sum()
    g["ER %"] = 100 * g.engagements / g.reach
    g["CTR %"] = 100 * g.clicks / g.impressions
    g["posts"] = df.groupby(key).size()
    return g[["posts", "ER %", "CTR %", "signups"]].round(2).sort_values("ER %", ascending=False)

fmt = rate_table("format")
topic = rate_table("topic")
print("\nBy format:\n" + fmt.to_string())
print("\nBy topic:\n" + topic.to_string())

# 5) chart
plt.figure(figsize=(6, 3.2))
plt.bar(fmt.index, fmt["ER %"], color=["#FF6B1A", "#FCD34D", "#A78BFA", "#F43F5E"][:len(fmt)])
avg = 100 * df.engagements.sum() / df.reach.sum()
plt.axhline(avg, color="black", linestyle="--", linewidth=1, label=f"overall {avg:.1f}%")
plt.ylabel("Engagement rate %")
plt.title("September: engagement rate by format")
plt.legend()
plt.tight_layout()
plt.savefig("session-07_er_by_format.png", dpi=80)
print("\nSaved -> session-07_er_by_format.png")

# 6) recommendations from rules, then a prompt for the written report
best_fmt, worst_fmt = fmt.index[0], fmt.index[-1]
hour_er = df.groupby("hour").apply(lambda g: 100 * g.engagements.sum() / g.reach.sum())
recs = [
    f"Shift effort toward {best_fmt} posts ({fmt.loc[best_fmt, 'ER %']:.1f}% ER) and away from "
    f"{worst_fmt} ({fmt.loc[worst_fmt, 'ER %']:.1f}%).",
    f"Schedule posts at {hour_er.idxmax()}:00, the best-performing hour ({hour_er.max():.1f}% ER).",
    f"Topic '{topic['signups'].idxmax()}' drove the most sign-ups ({int(topic['signups'].max())}): "
    "add one more post on it per week.",
    "A/B test two headlines on the next admissions post before scaling.",
]
print("\nRECOMMENDATIONS")
for r in recs:
    print(" -", r)

print("\nPROMPT FOR THE WRITTEN REPORT")
print("You are a social media analyst. Using ONLY the numbers below, write a 150-word report "
      "for the department head: what worked, what did not, three actions for October. "
      "Do not invent any figure.\n" + fmt.to_string() + "\nRecommendations: " + " ".join(recs))
