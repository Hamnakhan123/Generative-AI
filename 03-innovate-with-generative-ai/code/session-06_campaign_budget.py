"""
Session 6 · Example 2 — Split a campaign budget and forecast results.

Paid social is priced per 1,000 impressions (CPM). From the budget and CPM
we can forecast impressions; a click-through rate (CTR) gives clicks; a
conversion rate gives sign-ups; and cost per acquisition (CPA) = spend / sign-ups.
The CPMs and rates below are ASSUMED planning numbers for a student campaign,
not real market data: replace them with figures from your own ad dashboard.

Run:  python session-06_campaign_budget.py
"""
BUDGET = 50_000  # rupees
channels = {  # share of budget, CPM (Rs), CTR, conversion rate
    "Instagram": (0.40, 180, 0.012, 0.05),
    "Facebook":  (0.25, 120, 0.009, 0.04),
    "YouTube":   (0.20, 250, 0.006, 0.03),
    "LinkedIn":  (0.15, 600, 0.008, 0.08),
}

assert abs(sum(c[0] for c in channels.values()) - 1) < 1e-9, "shares must add up to 100%"
rows, tot = [], {"spend": 0, "imp": 0, "clicks": 0, "signups": 0}
print(f"{'Channel':10}{'Spend':>8}{'Impr.':>10}{'Clicks':>8}{'Sign-ups':>9}{'CPA':>8}")
for name, (share, cpm, ctr, cvr) in channels.items():
    spend = BUDGET * share
    imp = spend / cpm * 1000
    clicks = imp * ctr
    signups = clicks * cvr
    cpa = spend / signups
    print(f"{name:10}{spend:8,.0f}{imp:10,.0f}{clicks:8,.0f}{signups:9,.0f}{cpa:8,.0f}")
    for k, v in zip(tot, (spend, imp, clicks, signups)):
        tot[k] += v
print(f"{'TOTAL':10}{tot['spend']:8,.0f}{tot['imp']:10,.0f}{tot['clicks']:8,.0f}"
      f"{tot['signups']:9,.0f}{tot['spend']/tot['signups']:8,.0f}")
