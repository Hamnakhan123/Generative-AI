"""
Session 7 · Example 2 — A text summariser: offline extractive engine + LLM (DeepSeek-R1 / Qwen) prompt via Ollama.

Extractive (TF-IDF sentence scores: offline, never invents facts) and abstractive
(LLM via Ollama: fluent, must be checked). DeepSeek-R1 wraps its reasoning in <think> tags.

Run:  python session-07_summarizer.py
"""
import json, math, re, urllib.request
from collections import Counter

ARTICLE = """Karachi's public transport is changing quickly. The Green Line bus rapid transit
opened at the end of 2021 and now carries large numbers of passengers every day.
Commuters say travel times on the corridor have dropped sharply compared with minibuses.
However, feeder routes are still limited, so many riders walk long distances to reach stations.
The city has also introduced electric buses on several routes to reduce noise and air pollution.
Officials plan to integrate ticketing across lines with a single smart card.
Critics argue that maintenance funding must be secured, or service quality will decline.
Experts recommend publishing ridership data so that planners can match buses to demand.""".replace("\n", " ")

STOP = set("the a an and or of to in on is are was were has have with so that or for by at as be will must can many now still also which this its".split())


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def words(s):
    return [w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP]


def extractive_summary(text, k=3):
    sents = sentences(text)
    docs = [Counter(words(s)) for s in sents]
    df = Counter(w for d in docs for w in d)
    n = len(sents)
    scores = []
    for i, d in enumerate(docs):
        tfidf = sum(c * math.log(n / df[w]) for w, c in d.items())
        scores.append((tfidf / (1 + sum(d.values())) ** 0.5, i))   # mild length normalisation
    keep = sorted(i for _, i in sorted(scores, reverse=True)[:k])  # keep original order
    return [sents[i] for i in keep], {i: round(s, 2) for s, i in scores}


def strip_thinking(reply):
    return re.sub(r"<think>.*?</think>", "", reply, flags=re.S).strip()


summary, scores = extractive_summary(ARTICLE, k=3)
print(f"Article: {len(sentences(ARTICLE))} sentences, {len(ARTICLE.split())} words")
print("\nExtractive summary (3 sentences):")
for s in summary:
    print(" -", s)
print(f"Compression: {sum(len(s.split()) for s in summary)} / {len(ARTICLE.split())} words")

prompt = ("Summarise the article in exactly 3 bullet points of at most 15 words each. "
          "Use only facts from the article; do not add numbers that are not in it.\n\n"
          f'Article: """{ARTICLE}"""')
body = {"model": "deepseek-r1:7b", "prompt": prompt, "stream": False, "options": {"temperature": 0.1}}

print("\nstrip_thinking demo:", repr(strip_thinking("<think>3 bullets: Green Line, feeders...</think>\n- Green Line cut travel times.")))

try:
    urllib.request.urlopen("http://localhost:11434/api/tags", timeout=1)
    req = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    reply = json.loads(urllib.request.urlopen(req, timeout=120).read())["response"]
    print("\nLLM summary:\n" + strip_thinking(reply))
except Exception:
    print("\n(Ollama not running here: the offline extractive summary above is the result.)")
