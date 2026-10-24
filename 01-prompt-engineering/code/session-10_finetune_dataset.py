"""Builds and validates a small fine-tuning dataset in chat-JSONL format.
Each line = one example: system + user + assistant messages. Bad rows are reported, not silently kept."""
import json

SYSTEM = "You are IoBM Helpdesk. Answer in at most 2 sentences, politely, in simple English."
raw = [
    ("How do I reset my LMS password?", "Click 'Forgot password' on the LMS login page and follow the email link. If no email arrives in 10 minutes, contact IT at the helpdesk counter."),
    ("When is the add/drop deadline?", "The add/drop deadline is published in the academic calendar on the student portal. Please check it there, as dates change each semester."),
    ("Can I bring my own laptop to the lab?", "Yes, you can use your own laptop in the lab. Connect to the campus Wi-Fi with your student ID."),
    ("", "This row has no question."),
    ("Where is the library?", "The library is on the ground floor of the main block, next to the cafeteria, and it is open from 8 am to 8 pm on weekdays. Bring your student card to borrow books. Laptops are allowed in the reading area. Group rooms can be booked online."),
]

def valid(q, a):
    if not q.strip(): return "empty question"
    if a.count(".") > 2: return "answer longer than 2 sentences (breaks the style rule)"
    return None

good, report = [], []
for i, (q, a) in enumerate(raw, 1):
    problem = valid(q, a)
    if problem:
        report.append(f"row {i}: REJECTED ({problem})")
        continue
    good.append({"messages": [{"role": "system", "content": SYSTEM},
                              {"role": "user", "content": q},
                              {"role": "assistant", "content": a}]})
    report.append(f"row {i}: ok")

with open("session-10_helpdesk_train.jsonl", "w") as f:
    for ex in good:
        f.write(json.dumps(ex) + "\n")

print("\n".join(report))
print(f"\nKept {len(good)} of {len(raw)} examples -> session-10_helpdesk_train.jsonl")
print("First line:\n" + json.dumps(good[0])[:160] + "...")
