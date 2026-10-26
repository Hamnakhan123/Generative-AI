"""
Session 5 · Example 2 — A character bible that keeps AI stories consistent.

Problem: over a long chat the AI "forgets" that the hero has green eyes or
hates coffee. Fix: write each character once as structured data and paste
the same compact "bible" at the top of every chapter prompt.

Run:  python session-05_character_sheet.py
"""
from dataclasses import dataclass, asdict


@dataclass
class Character:
    name: str
    role: str          # protagonist, antagonist, mentor, ...
    age: int
    want: str          # what they consciously chase
    need: str          # what they actually need to learn (drives the arc)
    flaw: str
    voice: str         # how they speak
    details: str       # fixed physical or personal facts

    def card(self) -> str:
        return (f"{self.name} ({self.role}, {self.age}): wants {self.want}; needs {self.need}; "
                f"flaw: {self.flaw}; speaks {self.voice}; fixed facts: {self.details}.")


cast = [
    Character("Ayesha", "protagonist", 19, "to be the best coder in class",
              "to accept help and give credit", "pride", "fast, with tech slang",
              "wears round glasses, drinks chai, never coffee"),
    Character("Sir Kamran", "mentor", 45, "students who think for themselves",
              "to trust that students can change", "stubborn", "calmly, answers questions with questions",
              "grey beard, always carries a red marker"),
    Character("Bilal", "friend / foil", 20, "to pass without effort",
              "to own his mistakes", "laziness", "in jokes to dodge serious talk",
              "plays cricket for the university team"),
]

bible = "STORY BIBLE (keep these facts consistent):\n" + "\n".join("- " + c.card() for c in cast)
print(bible)
print("\nChapter prompt template:")
print(bible.splitlines()[0] + " [paste bible]\nWrite Chapter 3 (about 400 words): "
      "Sir Kamran notices two identical assignments. Stay in Ayesha's point of view.")
print("\nFields stored per character:", list(asdict(cast[0]).keys()))
