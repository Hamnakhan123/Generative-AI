"""
Session 5 · Mini project (full solution) — Story bible + continuity checker.

Real-life problem: you are co-writing a 5-chapter story with an AI for a
children's reading club. Across chapters the AI drifts: names change
spelling, a character's fixed facts change, and banned words for the age
group slip in. This tool:

  1. builds a chapter-by-chapter prompt plan from an arc,
  2. scans each generated chapter against the story bible,
  3. reports every continuity or suitability problem with its chapter number.

Run:  python session-05_project_story_bible.py
"""
import re

BIBLE = {
    "names": {"Zara": ["Zahra", "Sara"], "Moti": ["Motee", "Mothi"]},   # canonical: known wrong variants
    "facts": {"Moti": ("orange cat", ["black cat", "grey cat", "dog"])},  # fixed fact and contradictions
    "banned": ["stupid", "kill", "hate"],                                  # reading-club age rule
}
ARC = ["Zara finds a lost orange cat called Moti",
       "Moti leads Zara to a hidden garden on the school roof",
       "The garden is dying because the water tank leaks",
       "Zara and her class build a rainwater collector",
       "The garden blooms and Moti becomes the school mascot"]

print("PROMPT PLAN")
for i, beat in enumerate(ARC, 1):
    print(f"  Ch{i}: Using the story bible, write ~300 words for ages 7-9: {beat}.")

chapters = {
    1: "Zara found a small orange cat behind the canteen. She named him Moti.",
    2: "Moti ran up the stairs. Zahra followed him to a garden full of plants.",
    3: "The plants looked sad. 'I hate leaks,' said Zara. Moti, the grey cat, sniffed the tank.",
    4: "The class built a collector from old bottles. Zara was proud.",
    5: "Flowers bloomed everywhere and Motee became the mascot.",
}


def check(chapter_no: int, text: str) -> list:
    issues = []
    for canon, variants in BIBLE["names"].items():
        for v in variants:
            if re.search(rf"\b{v}\b", text):
                issues.append(f"name drift: '{v}' should be '{canon}'")
    for who, (fact, contradictions) in BIBLE["facts"].items():
        for c in contradictions:
            if c in text.lower():
                issues.append(f"fact clash: {who} is an {fact}, text says '{c}'")
    for word in BIBLE["banned"]:
        if re.search(rf"\b{word}\b", text, re.I):
            issues.append(f"age rule: avoid the word '{word}'")
    return issues


print("\nCONTINUITY REPORT")
total = 0
for no, text in chapters.items():
    issues = check(no, text)
    total += len(issues)
    print(f"  Ch{no}: " + ("OK" if not issues else " | ".join(issues)))
print(f"\n{total} issue(s) found. Send each flagged chapter back with the bible and the exact fix.")
