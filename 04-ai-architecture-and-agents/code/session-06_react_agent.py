"""
Session 6 · Example 1 — A ReAct agent loop (Reason + Act) with tools, built from scratch.

THINK -> ACT (call a tool) -> OBSERVE, until the agent can answer. In production plan()
is an LLM function-calling request; a rule-based planner keeps this offline and reproducible.

Run:  python session-06_react_agent.py
"""
import json, math, re

# ---------- tools: plain functions with a name, description and JSON arguments ----------
FX = {"USD": 280.5, "EUR": 303.2, "AED": 76.4}           # illustrative PKR rates
FEES = {"BSCS": 145_000, "BBA": 120_000, "BS-AI": 160_000}   # per semester, illustrative

def calculator(expression: str) -> str:
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "error: only arithmetic is allowed"
    return str(round(eval(expression, {"__builtins__": {}}), 2))

def currency(amount: float, frm: str, to: str = "PKR") -> str:
    return f"{amount * FX[frm]:.0f} PKR" if to == "PKR" else f"{amount / FX[to]:.2f} {to}"

def fee_lookup(program: str) -> str:
    return f"{FEES[program]} PKR per semester" if program in FEES else "unknown programme"

TOOLS = {"calculator": calculator, "currency": currency, "fee_lookup": fee_lookup}
SCHEMAS = [
    {"name": "calculator", "description": "Evaluate an arithmetic expression", "parameters": {"expression": "string"}},
    {"name": "currency", "description": "Convert money between currencies", "parameters": {"amount": "number", "frm": "string", "to": "string"}},
    {"name": "fee_lookup", "description": "Semester fee for a programme", "parameters": {"program": "string"}},
]

# ---------- the 'LLM': decides the next step from the question and what it has seen ----------
def plan(question, scratchpad):
    seen = [s["tool"] for s in scratchpad]
    if "fee" in question.lower() and "fee_lookup" not in seen:
        prog = re.search(r"(BSCS|BBA|BS-AI)", question).group(1)
        return {"thought": f"I need the fee for {prog}.", "tool": "fee_lookup", "args": {"program": prog}}
    if "fee_lookup" in seen and "calculator" not in seen:
        fee = int(scratchpad[-1]["observation"].split()[0])
        sems = int(re.search(r"(\d+) semesters", question).group(1))
        return {"thought": f"Total = fee x {sems} semesters.", "tool": "calculator", "args": {"expression": f"{fee}*{sems}"}}
    if "dollars" in question.lower() and "currency" not in seen:
        total = float(scratchpad[-1]["observation"])
        return {"thought": "Convert the total from PKR to USD.", "tool": "currency", "args": {"amount": total, "frm": "PKR", "to": "USD"}}
    return {"thought": "I have everything I need.", "final": scratchpad[-1]["observation"]}

def run_agent(question, max_steps=5):
    print(f"QUESTION: {question}")
    scratchpad = []
    for step in range(1, max_steps + 1):
        decision = plan(question, scratchpad)
        print(f"  Thought {step}: {decision['thought']}")
        if "final" in decision:
            print(f"  FINAL ANSWER: {decision['final']}\n")
            return decision["final"]
        print(f"  Action {step}: {decision['tool']}({json.dumps(decision['args'])})")
        try:
            obs = TOOLS[decision["tool"]](**decision["args"])
        except Exception as e:                       # tools fail: the agent must see the error
            obs = f"error: {e}"
        print(f"  Observation {step}: {obs}")
        scratchpad.append({"tool": decision["tool"], "observation": obs})
    print("  Stopped: step limit reached (a guardrail against endless loops)\n")

print("Tool schemas sent to the model:")
for s in SCHEMAS:
    print("  ", json.dumps(s))
print()
run_agent("What is the total fee for BS-AI over 8 semesters?")
run_agent("What is the total fee for BBA over 8 semesters in dollars?")
print("Guardrail check -> calculator('__import__(\"os\")'):", calculator('__import__("os")'))
