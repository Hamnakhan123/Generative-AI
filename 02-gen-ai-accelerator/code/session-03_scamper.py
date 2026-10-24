"""Turn the SCAMPER creativity method into seven ready-to-paste brainstorming prompts."""
SCAMPER = {
    "Substitute": "What could we replace in {x} to make it better or cheaper?",
    "Combine": "What could {x} be combined with to create something new?",
    "Adapt": "What idea from another field could be adapted for {x}?",
    "Modify": "What could be made bigger, smaller or different in {x}?",
    "Put to other use": "Who else could use {x}, or for what other purpose?",
    "Eliminate": "What could be removed from {x} without losing its value?",
    "Reverse": "What if we did {x} in the opposite order or from the user's side?",
}
idea = "the university library's book-return process"
for i, (step, q) in enumerate(SCAMPER.items(), 1):
    print(f"{i}. [{step}] {q.format(x=idea)} Give 3 short ideas.")
