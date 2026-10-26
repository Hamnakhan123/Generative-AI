"""
Session 2 · Mini project (full solution) — A blog-writing pipeline.

Real-life problem: you must publish a 700-word, search-friendly blog post
every week for the department website. Writing one giant prompt gives a
generic article. A better workflow splits the job into steps:

  1. Outline  -> a word budget for every section
  2. Section prompts -> one focused prompt per section (better quality)
  3. Quality gate -> check the assembled draft: length, keyword use,
     readability, unfinished placeholders

This script builds the prompts and runs the quality gate on a sample draft.
Run:  python session-02_project_blog_pipeline.py
"""
import re

TITLE = "How to Use AI as a Study Partner (Without Cheating)"
KEYWORD = "ai study partner"
TARGET_WORDS = 700
SECTIONS = [  # (heading, share of the word budget)
    ("Introduction", 0.12),
    ("What an AI study partner can and cannot do", 0.22),
    ("Three prompts that make you think", 0.30),
    ("Staying inside the integrity rules", 0.22),
    ("Conclusion and next step", 0.14),
]

# ---------- Step 1: outline with word budgets ----------
print(f"OUTLINE for '{TITLE}' ({TARGET_WORDS} words)")
budget = {h: round(TARGET_WORDS * share) for h, share in SECTIONS}
for h, w in budget.items():
    print(f"  {w:4} words  {h}")
print(f"  ----\n  {sum(budget.values()):4} words total")

# ---------- Step 2: one prompt per section ----------
print("\nSECTION PROMPTS")
for i, (h, w) in enumerate(budget.items(), 1):
    prompt = (f"[{i}/{len(budget)}] Write the section '{h}' of the blog '{TITLE}'. "
              f"About {w} words, audience: first-year students, friendly tone. "
              f"Use the phrase '{KEYWORD}' at most once. End without a summary line.")
    print("  " + prompt)

# ---------- Step 3: quality gate on an assembled draft ----------
draft = """
# How to Use AI as a Study Partner (Without Cheating)
An AI study partner can quiz you, explain hard ideas, and check your reasoning.
It cannot sit your exam. Studies show students who test themselves remember more [SOURCE NEEDED].
## Three prompts that make you think
Ask: give me one hint, not the answer. Ask: quiz me with five questions. Ask: find the gap in my explanation.
Your AI study partner works best when you do the thinking. Your AI study partner should never write graded work.
"""


def quality_gate(text: str) -> list:
    report = []
    words = re.findall(r"[A-Za-z']+", text)
    report.append(("length", len(words) >= 0.9 * TARGET_WORDS, f"{len(words)}/{TARGET_WORDS} words"))
    hits = text.lower().count(KEYWORD)
    density = 100 * hits * len(KEYWORD.split()) / max(len(words), 1)
    report.append(("keyword density", 0.5 <= density <= 2.5, f"{hits} uses = {density:.1f}% (aim 0.5-2.5%)"))
    placeholders = re.findall(r"\[[A-Z ]+\]", text)
    report.append(("placeholders", not placeholders, f"found {placeholders}" if placeholders else "none"))
    found = [h for h, _ in SECTIONS if h.lower() in text.lower()]
    report.append(("sections", len(found) == len(SECTIONS), f"{len(found)}/{len(SECTIONS)} headings present"))
    return report


print("\nQUALITY GATE")
results = quality_gate(draft)
for name, ok, detail in results:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name:16} {detail}")
passed = sum(ok for _, ok, _ in results)
print(f"\n{passed}/{len(results)} checks passed -> {'publish' if passed == len(results) else 'send back for revision'}")

# ---------- Step 4: turn failures into a precise revision prompt ----------
failed = [f"- {name}: {detail}" for name, ok, detail in results if not ok]
if failed:
    print("\nREVISION PROMPT (paste back into the assistant)")
    print("Revise the draft below. Fix ONLY these problems and keep everything else:")
    print("\n".join(failed))
    print("Replace any [SOURCE NEEDED] with a real, named source or delete the claim.")
