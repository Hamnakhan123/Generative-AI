"""'Train' an assistant on your style: extract a style profile from your own writing samples
and paste it into custom instructions."""
import re, statistics
samples = [
    "Quick update: the lab is moved to Room 4. Bring your laptops. Thanks!",
    "Reminder - quiz on Friday. Chapters 3 and 4 only. Good luck, you've got this!",
    "Assignment deadline extended to Monday. Please submit on the portal. Thanks!",
]
sentences = [s for t in samples for s in re.split(r"(?<=[.!?])\s+", t) if s]
words = [w for t in samples for w in re.findall(r"[A-Za-z']+", t)]
profile = {
    "avg_sentence_words": round(statistics.mean(len(s.split()) for s in sentences), 1),
    "exclamations_per_msg": round(sum(t.count("!") for t in samples) / len(samples), 2),
    "uses_contractions": any("'" in w for w in words),
    "common_signoff": max(set(t.split()[-1] for t in samples), key=lambda x: sum(t.endswith(x) for t in samples)),
}
print("Style profile:", profile)
print("\nCustom-instruction prompt:\n"
      f"Write like me: short sentences (~{profile['avg_sentence_words']} words), friendly and direct, "
      f"about {profile['exclamations_per_msg']} exclamation per message, "
      f"{'use' if profile['uses_contractions'] else 'avoid'} contractions, end with '{profile['common_signoff']}'.")
