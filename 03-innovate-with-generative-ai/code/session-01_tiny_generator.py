"""
Session 1 · Example 2 — A tiny "generative model" you can read in one minute.

A real large language model learns probabilities for the next token from
billions of words. Here we do the same thing at toy scale: count which word
follows which in a small corpus (a bigram model), then SAMPLE new sentences.

Key lesson: the model only recombines patterns it has seen. Changing the
random seed changes the output, just like re-generating in a chat tool.

Run:  python session-01_tiny_generator.py
"""
import random
from collections import defaultdict

corpus = """
the poster shows a bright city at night .
the poster uses bold orange text .
the video shows a calm city at sunrise .
the video uses soft music and slow camera moves .
the story follows a young coder at night .
the story uses short scenes and bold choices .
"""

# 1) Learn: for every word, remember all words that came right after it.
follows = defaultdict(list)
words = corpus.split()
for current, nxt in zip(words, words[1:]):
    follows[current].append(nxt)

print("What the model learned after 'the':", sorted(set(follows["the"])))
print("What the model learned after 'uses':", sorted(set(follows["uses"])))


# 2) Generate: start with a word and keep sampling a likely next word.
def generate(start: str, seed: int, max_words: int = 12) -> str:
    rng = random.Random(seed)       # fixed seed => reproducible output
    out = [start]
    while len(out) < max_words:
        options = follows.get(out[-1])
        if not options:
            break
        nxt = rng.choice(options)   # frequent pairs appear more often in the list
        out.append(nxt)
        if nxt == ".":
            break
    return " ".join(out)


print()
for seed in (1, 2, 3, 4):
    print(f"seed {seed}: {generate('the', seed)}")
