"""
Session 7 · Example 3 — Retrieval-Augmented Generation (RAG): retrieve, then build a grounded prompt.

Retrieve the most similar handbook chunks, then build a prompt that answers ONLY from
them with citations. Real systems use neural embeddings + a vector DB; TF-IDF keeps it offline.

Run:  python session-07_rag_search.py
Creates: session-07_rag_scores.png
"""
import math, re
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DOCS = {
    "attendance.md": "Students must attend at least 75 percent of classes in each course. Below 75 percent the student is not allowed to sit the final exam.",
    "exams.md": "Final exams are held in the last two weeks of the semester. A student who misses an exam for medical reasons may apply for a deferred exam within 7 days with a medical certificate.",
    "fees.md": "Semester fees are due before the first day of classes. A late fee of 5,000 rupees applies after the due date. Fees can be paid in two instalments with approval.",
    "library.md": "The library is open from 8 am to 9 pm on weekdays. Students may borrow up to 4 books for 14 days. The fine for a late book is 50 rupees per day.",
    "wifi.md": "Campus wifi uses your student ID and portal password. If you cannot connect, reset your password on the portal or visit the IT help desk in Block B.",
    "hostel.md": "Hostel rooms are allocated by merit and distance from home. Guests are allowed in the common room until 8 pm. The hostel deposit is refunded within 30 days of leaving.",
}
STOP = set("the a an and or of to in on is are be for by at as it if you your may must can from with within each after per up".split())


# Keyword vectors miss synonyms ("sick" vs "medical"). Neural embeddings learn these
# links automatically; here a small synonym table plays that role.
SYNONYMS = {"sick": "medical", "ill": "medical", "missed": "misses", "pay": "paid", "books": "book",
            "take": "borrow", "internet": "wifi", "parts": "instalments"}


def tokens(text, expand=False):
    ws = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]
    return ws + [SYNONYMS[w] for w in ws if expand and w in SYNONYMS]


df = Counter(w for d in DOCS.values() for w in set(tokens(d)))
N = len(DOCS)


def vec(text, expand=False):
    tf = Counter(tokens(text, expand))
    return {w: c * (math.log((N + 1) / (df.get(w, 0) + 1)) + 1) for w, c in tf.items()}


def cosine(a, b):
    dot = sum(a[w] * b.get(w, 0) for w in a)
    norm = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return dot / norm if norm else 0.0


INDEX = {name: vec(text) for name, text in DOCS.items()}


def retrieve(question, k=2, min_score=0.10, expand=True):
    q = vec(question, expand)
    ranked = sorted(((cosine(q, v), name) for name, v in INDEX.items()), reverse=True)
    return ranked, [(s, n) for s, n in ranked[:k] if s >= min_score]


def grounded_prompt(question, hits):
    context = "\n".join(f"[{n}] {DOCS[n]}" for _, n in hits) or "(no relevant documents found)"
    return ("Answer the question using ONLY the context. Cite sources in [brackets]. "
            "If the context does not contain the answer, say you don't know.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:")


if __name__ == "__main__":      # lets session-07_project_chatbot.py import the retriever
    questions = ["I missed my exam because I was sick, what can I do?",
                 "How much is the fine if I return a library book late?",
                 "Who won the cricket match yesterday?"]
    plain = retrieve(questions[0], expand=False)[0][0]
    print(f"Keyword-only best match for question 1: {plain[1]} ({plain[0]:.2f}) -> below 0.10, nothing retrieved")
    print("With synonym expansion (what embeddings do for you):\n")
    all_ranked = {}
    for q in questions:
        ranked, hits = retrieve(q)
        all_ranked[q] = ranked
        print(f"Q: {q}")
        print("   top matches:", ", ".join(f"{n} ({s:.2f})" for s, n in ranked[:3]))
        print("   used as context:", [n for _, n in hits] or "none -> the model must say it does not know")
    print("\nGrounded prompt for question 2:\n" + grounded_prompt(questions[1], retrieve(questions[1])[1]))

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), sharey=True)
    for ax, q in zip(axes, questions):
        ranked = sorted(all_ranked[q], key=lambda t: t[1])                     # alphabetical rows
        ax.barh([n for _, n in ranked], [sc for sc, _ in ranked], color=["#FF6B1A" if sc >= 0.10 else "#A78BFA" for sc, _ in ranked])
        ax.axvline(0.10, color="#F43F5E", ls="--", lw=1); ax.set_title(q[:34] + "...", fontsize=9); ax.set_xlim(0, 0.8)
    axes[1].set_xlabel("Cosine similarity (dashed line = minimum score)")
    fig.tight_layout(); fig.savefig("session-07_rag_scores.png", dpi=110)
    print("\nSaved chart: session-07_rag_scores.png")
