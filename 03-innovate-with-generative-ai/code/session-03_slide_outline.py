"""
Session 3 · Example 3 — From a topic to a presentation outline that a slide
tool (Gamma, Copilot in PowerPoint, Canva) can turn into a deck.

Two rules keep AI decks readable:
  * one idea per slide, a headline that states the point;
  * at most 6 bullets of at most 6 words each ("6x6 rule").
The script writes a Markdown outline and checks each slide against the rules.

Run:  python session-03_slide_outline.py
"""

deck = {
    "title": "Using AI Safely in Your First Semester",
    "slides": [
        ("AI is a study partner, not a ghost-writer",
         ["Explains hard ideas", "Quizzes you before tests", "Gives feedback on drafts"]),
        ("Three prompts that make you think",
         ["Give me one hint only", "Quiz me with five questions", "Find gaps in my explanation"]),
        ("Know the integrity rules",
         ["Check each course's AI policy", "Disclose permitted AI help",
          "Never submit AI-written graded work", "Never invent references",
          "Keep your drafts as evidence", "Ask your teacher when unsure",
          "Remember that detectors are unreliable"]),
        ("Protect your data",
         ["Never paste CNIC numbers, passwords or grades into free AI tools because they may be stored"]),
    ],
}


def check_slide(bullets):
    issues = []
    if len(bullets) > 6:
        issues.append(f"{len(bullets)} bullets (max 6)")
    long = [b for b in bullets if len(b.split()) > 6]
    if long:
        issues.append(f"{len(long)} bullet(s) over 6 words")
    return issues


lines = [f"# {deck['title']}", ""]
for n, (headline, bullets) in enumerate(deck["slides"], 1):
    lines.append(f"## Slide {n}: {headline}")
    lines += [f"- {b}" for b in bullets]
    lines.append("")
    issues = check_slide(bullets)
    print(f"Slide {n}: {'OK' if not issues else 'FIX -> ' + '; '.join(issues)}")

print("\n--- Markdown outline (paste into a slide tool) ---")
print("\n".join(lines[:8]))
print("...")
