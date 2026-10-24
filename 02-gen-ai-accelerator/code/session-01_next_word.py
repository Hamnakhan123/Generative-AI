"""A tiny 'language model': count which word follows which (a bigram model),
then predict the next word. Real LLMs do the same job - predict the next token -
but with billions of learned parameters instead of a word-count table."""
from collections import Counter, defaultdict

corpus = """students learn python in the lab . students learn ai in the class .
teachers explain ai in the class . students ask questions in the lab .
ai helps students learn faster . teachers use ai to plan the class ."""
words = corpus.split()

follows = defaultdict(Counter)
for a, b in zip(words, words[1:]):
    follows[a][b] += 1

def next_word_probs(word):
    c = follows[word]
    total = sum(c.values())
    return {w: n / total for w, n in c.most_common()}

for w in ["students", "in", "ai"]:
    probs = next_word_probs(w)
    print(f"after '{w}':", ", ".join(f"{k} {v:.2f}" for k, v in probs.items()))

# Greedy generation: always pick the most likely next word
word, out = "teachers", ["teachers"]
for _ in range(6):
    word = follows[word].most_common(1)[0][0]
    out.append(word)
print("\ngreedy text:", " ".join(out))
