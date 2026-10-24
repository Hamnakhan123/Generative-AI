"""A prompt 'linter': checks a prompt against expert strategies and suggests fixes."""
import re
CHECKS = [
    ("Has an action verb", lambda p: re.match(r"^(write|explain|list|compare|summari[sz]e|create|draft|classify|translate|generate|analy[sz]e|rewrite|act)\b", p.strip(), re.I) or re.search(r"\byou are\b", p, re.I),
     "Start with a clear verb (Write, Explain, Compare...) or a role line."),
    ("States audience", lambda p: re.search(r"\b(for|audience|students|beginners|manager|customers|kids)\b", p, re.I),
     "Say who the output is for."),
    ("Limits length", lambda p: re.search(r"\b(\d+\s*(words|bullets|sentences|lines|characters)|short|brief)\b", p, re.I),
     "Add a length limit (e.g. 'under 120 words')."),
    ("Specifies format", lambda p: re.search(r"\b(table|bullet|json|list|steps|headings|markdown|csv)\b", p, re.I),
     "Ask for a format: table, bullets, JSON..."),
    ("Uses delimiters for input", lambda p: ('"""' in p) or ("###" in p) or ("<text>" in p) or ("Text:" not in p),
     "Wrap pasted input in delimiters like ### or triple quotes."),
    ("Avoids vague words", lambda p: not re.search(r"\b(good|nice|stuff|things|etc)\b", p, re.I),
     "Replace vague words with measurable criteria."),
]

def lint(prompt):
    passed, tips = 0, []
    for name, test, tip in CHECKS:
        if test(prompt): passed += 1
        else: tips.append(f"  - {name}: {tip}")
    return passed, tips

for p in ["Write something good about our product etc.",
          "You are a product marketer. Write 3 bullet points (under 15 words each) for busy managers "
          "explaining why our attendance app saves time. Format: Markdown list."]:
    score, tips = lint(p)
    print(f"PROMPT: {p[:70]}...\nScore: {score}/{len(CHECKS)}")
    print("\n".join(tips) if tips else "  All checks passed")
    print()
