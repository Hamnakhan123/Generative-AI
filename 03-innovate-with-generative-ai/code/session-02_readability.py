"""
Session 2 · Example 2 — Measure readability of an AI draft vs an edited draft.

The Flesch Reading Ease score (0-100, higher = easier) is a classic formula:
    206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
60-70 is "plain English"; under 30 reads like an academic paper.
AI drafts often come out long-winded, so measuring before and after editing
shows whether your "make it simpler" prompt actually worked.

Run:  python session-02_readability.py
"""
import re


def count_syllables(word: str) -> int:
    """Approximate syllables: count vowel groups, drop a silent final 'e'."""
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    n = len(groups)
    if word.endswith("e") and n > 1 and not word.endswith("le"):
        n -= 1
    return max(n, 1)


def readability(text: str) -> dict:
    sentences = max(len(re.findall(r"[.!?]+", text)), 1)
    words = re.findall(r"[A-Za-z']+", text)
    syllables = sum(count_syllables(w) for w in words)
    wps = len(words) / sentences
    spw = syllables / len(words)
    score = 206.835 - 1.015 * wps - 84.6 * spw
    return {"words": len(words), "sentences": sentences,
            "words_per_sentence": round(wps, 1), "flesch": round(score, 1)}


ai_draft = ("Artificial intelligence technologies are increasingly being utilised by "
            "contemporary university students in order to facilitate the comprehension of "
            "complicated academic material, consequently improving educational outcomes "
            "significantly across numerous disciplines.")

edited = ("Many students now use AI to understand hard topics. "
          "It can explain an idea in simple words. "
          "It can quiz you before a test. "
          "Used well, it helps you learn faster.")

for label, text in (("AI first draft", ai_draft), ("Edited version", edited)):
    r = readability(text)
    print(f"{label:15} words={r['words']:3} sentences={r['sentences']} "
          f"words/sentence={r['words_per_sentence']:5} Flesch={r['flesch']}")

print("\nGuide: 90+ very easy | 60-70 plain English | 30-50 difficult | <30 very difficult")
print("Very dense text can even score below 0: one 29-word sentence full of long words does that.")
