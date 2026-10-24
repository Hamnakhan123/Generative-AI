"""Redact personal data before pasting text into a public AI tool."""
import re

PATTERNS = [
    ("EMAIL", r"[\w.+-]+@[\w-]+\.[\w.]+"),
    ("CNIC", r"\b\d{5}-\d{7}-\d\b"),
    ("PHONE", r"\b03\d{2}-?\d{7}\b"),
    ("ROLLNO", r"\b[A-Z]{2}\d{2}-\d{4}\b"),
]

def redact(text):
    found = {}
    for label, pat in PATTERNS:
        text, n = re.subn(pat, f"[{label}]", text)
        if n: found[label] = n
    return text, found

msg = ("Student Ayesha Khan (roll CS23-0412, CNIC 42101-1234567-8) emailed "
       "ayesha.k@example.com from 0321-5551234 asking about her grade.")
clean, found = redact(msg)
print(clean)
print("redacted:", found)
