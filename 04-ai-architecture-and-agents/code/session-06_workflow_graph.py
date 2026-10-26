"""
Session 6 · Example 2 — A LangGraph-style agent workflow: nodes, shared state and conditional edges.

Nodes update a shared state; conditional edges choose the next node (retry loops,
human approval). Student support tickets: classify -> draft -> check -> approve/send.

Run:  python session-06_workflow_graph.py
"""
from dataclasses import dataclass, field

@dataclass
class State:
    ticket: str
    category: str = ""
    draft: str = ""
    attempts: int = 0
    needs_human: bool = False
    log: list = field(default_factory=list)

# ---------------- nodes ----------------
def classify(s: State):
    t = s.ticket.lower()
    s.category = ("refund" if "refund" in t else "it" if any(w in t for w in ["wifi", "password", "login"])
                  else "exam" if "exam" in t else "general")
    s.log.append(f"classify -> {s.category}")

def draft_reply(s: State):
    s.attempts += 1
    templates = {
        "it": "Please reset your password at the IT portal; if Wi-Fi still fails, visit Room IT-2.",
        "exam": "Your exam schedule is on the student portal under Academics > Exams.",
        "refund": "We have received your refund request. Refunds take 10 working days after approval.",
        "general": "Thanks for writing. A coordinator will reply within 2 working days.",
    }
    s.draft = templates[s.category] if s.attempts > 1 or s.category != "it" else "Try again later."
    s.log.append(f"draft (attempt {s.attempts}) -> '{s.draft[:45]}...'")

def quality_check(s: State) -> str:
    ok = len(s.draft.split()) >= 8                     # e.g. an LLM-as-judge in real systems
    s.log.append(f"quality_check -> {'pass' if ok else 'fail'}")
    return "pass" if ok else ("retry" if s.attempts < 3 else "escalate")

def human_approval(s: State):
    s.needs_human = True
    s.log.append("human_approval -> queued for a staff member (money involved)")

def send(s: State):
    s.log.append("send -> reply emailed to student")

def escalate(s: State):
    s.log.append("escalate -> handed to a human agent")

# ---------------- graph: edges, including conditional ones ----------------
def run(s: State):
    node = "classify"
    while node != "END":
        if node == "classify":
            classify(s); node = "draft"
        elif node == "draft":
            draft_reply(s); node = "check"
        elif node == "check":
            result = quality_check(s)
            node = {"retry": "draft", "escalate": "escalate"}.get(result) or ("approval" if s.category == "refund" else "send")
        elif node == "approval":
            human_approval(s); node = "END"
        elif node == "send":
            send(s); node = "END"
        elif node == "escalate":
            escalate(s); node = "END"
    return s

for ticket in ["My wifi login keeps failing in the library",
               "I want a refund for the hostel deposit",
               "When is my final exam for Data Structures?"]:
    s = run(State(ticket))
    print(f"TICKET: {ticket}")
    for line in s.log:
        print("   ", line)
    print()
