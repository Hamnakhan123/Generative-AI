"""
Session 6 · Mini project (full solution) — An expense-claim agent with tools, memory, guardrails and a human in the loop.

Real-life problem: a finance office wants claims checked against policy with tools
(policy, receipt, budget, duplicate memory), low-risk claims auto-approved, violations
rejected, risky or large claims escalated to a human, and an audit log plus weekly chart.
Hard limits live in code; an LLM could read free-text claims and call the same tools.

Run:  python session-06_project_expense_agent.py
Creates: session-06_expense_decisions.png
"""
from collections import Counter, defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

POLICY = {  # category: max per claim (PKR), receipt required above (PKR)
    "travel": (40_000, 2_000), "meals": (5_000, 1_000), "books": (15_000, 0),
    "equipment": (60_000, 0), "conference": (80_000, 0),
}
AUTO_APPROVE_LIMIT = 25_000          # above this a human must sign, whatever the policy says
BUDGET_LEFT = {"CS": 150_000, "BBA": 60_000, "EE": 90_000}

CLAIMS = [
    {"id": "C01", "who": "Hamza", "dept": "CS", "cat": "books", "amount": 6_500, "receipt": True},
    {"id": "C02", "who": "Maryam", "dept": "BBA", "cat": "meals", "amount": 7_200, "receipt": True},
    {"id": "C03", "who": "Usman", "dept": "EE", "cat": "travel", "amount": 18_000, "receipt": True},
    {"id": "C04", "who": "Hamza", "dept": "CS", "cat": "books", "amount": 6_500, "receipt": True},
    {"id": "C05", "who": "Zainab", "dept": "CS", "cat": "conference", "amount": 72_000, "receipt": True},
    {"id": "C06", "who": "Ali", "dept": "BBA", "cat": "travel", "amount": 3_000, "receipt": False},
    {"id": "C07", "who": "Fatima", "dept": "EE", "cat": "equipment", "amount": 22_000, "receipt": True},
    {"id": "C08", "who": "Saad", "dept": "BBA", "cat": "equipment", "amount": 55_000, "receipt": True},
    {"id": "C09", "who": "Hina", "dept": "CS", "cat": "gifts", "amount": 4_000, "receipt": True},
    {"id": "C10", "who": "Usman", "dept": "EE", "cat": "meals", "amount": 900, "receipt": False},
]

# ---------------- tools ----------------
def policy_lookup(cat):
    return POLICY.get(cat)

def receipt_check(claim, rule):
    return claim["receipt"] or claim["amount"] <= rule[1]

def budget_check(claim):
    return BUDGET_LEFT[claim["dept"]] >= claim["amount"]

memory = defaultdict(list)                        # who -> past (cat, amount)
def duplicate_check(claim):
    return (claim["cat"], claim["amount"]) in memory[claim["who"]]

# ---------------- agent decision ----------------
def decide(claim):
    rule = policy_lookup(claim["cat"])
    if rule is None:
        return "REJECT", f"category '{claim['cat']}' is not reimbursable"
    if duplicate_check(claim):
        return "ESCALATE", "possible duplicate of an earlier claim"
    if claim["amount"] > rule[0]:
        return "REJECT", f"above the {claim['cat']} limit of Rs {rule[0]:,}"
    if not receipt_check(claim, rule):
        return "REJECT", f"receipt required above Rs {rule[1]:,}"
    if not budget_check(claim):
        return "ESCALATE", f"{claim['dept']} budget left Rs {BUDGET_LEFT[claim['dept']]:,} is too low"
    if claim["amount"] > AUTO_APPROVE_LIMIT:
        return "ESCALATE", f"over Rs {AUTO_APPROVE_LIMIT:,}: needs a human signature"
    return "APPROVE", "within policy, receipt OK, budget OK"

audit, totals = [], Counter()
print(f"{'id':4s} {'who':7s} {'dept':4s} {'category':11s} {'amount':>8s}  decision  reason")
for c in CLAIMS:
    decision, reason = decide(c)
    if decision == "APPROVE":
        BUDGET_LEFT[c["dept"]] -= c["amount"]
    memory[c["who"]].append((c["cat"], c["amount"]))
    audit.append({**c, "decision": decision, "reason": reason})
    totals[decision] += c["amount"]
    print(f"{c['id']:4s} {c['who']:7s} {c['dept']:4s} {c['cat']:11s} {c['amount']:8,}  {decision:8s}  {reason}")

counts = Counter(a["decision"] for a in audit)
print("\nSummary:", dict(counts))
print("Amounts :", {k: f"Rs {v:,}" for k, v in totals.items()})
print("Budget left after auto-approvals:", {k: f"Rs {v:,}" for k, v in BUDGET_LEFT.items()})
print(f"Human workload: {counts['ESCALATE']} of {len(CLAIMS)} claims "
      f"({counts['ESCALATE'] / len(CLAIMS):.0%}) instead of 100%")

labels = ["APPROVE", "ESCALATE", "REJECT"]
fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
axes[0].bar(labels, [counts[l] for l in labels], color=["#FCD34D", "#FF6B1A", "#F43F5E"])
axes[0].set_title("Claims by decision"); axes[0].set_ylabel("Number of claims")
axes[1].bar(labels, [totals[l] / 1000 for l in labels], color=["#FCD34D", "#FF6B1A", "#F43F5E"])
axes[1].set_title("Amount by decision"); axes[1].set_ylabel("Thousand PKR")
fig.suptitle("Expense agent: one week of claims")
fig.tight_layout(); fig.savefig("session-06_expense_decisions.png", dpi=110)
print("Saved chart: session-06_expense_decisions.png")
