"""
Session 7 · Mini project (full solution) — "CampusBot": a RAG chatbot on Qwen 2.5 via Ollama, with an offline fallback.

Real-life problem: student affairs wants a chatbot that answers ONLY from the handbook
with citations, remembers the conversation for follow-ups, declines out-of-scope questions
with a contact, and runs on a local Qwen 2.5 model via Ollama (offline fallback if not running).
It reuses the handbook and retriever from session-07_rag_search.py (keep both files together).

Run:  python session-07_project_chatbot.py                # scripted demo
      python session-07_project_chatbot.py --interactive  # chat yourself (type 'quit')
"""
import importlib.util, json, re, sys, urllib.request
from collections import Counter, deque

try:
    spec = importlib.util.spec_from_file_location("rag", "session-07_rag_search.py")
    rag = importlib.util.module_from_spec(spec); spec.loader.exec_module(rag)   # DOCS, tokens, retrieve
except FileNotFoundError:            # in the notebook/Colab the RAG cell above already defined them
    import types; rag = types.SimpleNamespace(DOCS=DOCS, tokens=tokens, retrieve=retrieve)

CONTACT = "student.affairs@campus.example (Room A-12, 9 am to 4 pm)"
SYSTEM = ("You are CampusBot, a polite assistant for students. Answer in at most 2 sentences using ONLY "
          "the handbook context, and end with the source file in [brackets]. If the context does not "
          f"answer the question, say you don't know and suggest contacting {CONTACT}.")
MODEL = "qwen2.5:7b"


class CampusBot:
    def __init__(self, memory_turns=3):
        self.history = deque(maxlen=memory_turns * 2)    # sliding window of user/assistant messages
        self.topic = None
        try:
            urllib.request.urlopen("http://localhost:11434/api/tags", timeout=1); self.online = True
        except Exception:
            self.online = False

    def retrieve(self, question):
        ranked, hits = rag.retrieve(question, k=1)
        score = ranked[0][0]
        # A follow-up ("and how many...?", "what about it?") has no topic of its own: reuse the remembered one.
        follow_up = re.match(r"\s*(and|also|what about|how about)\b", question.lower()) or \
            re.search(r"\b(it|that|them|those)\b", question.lower())
        if not hits and self.topic and follow_up:
            return self.topic, score, True
        return (hits[0][1] if hits else None), score, False

    def _llm(self, question, doc):
        context = f"[{doc}] {rag.DOCS[doc]}" if doc else "(no relevant section)"
        messages = [{"role": "system", "content": SYSTEM}, *self.history,
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}]
        body = json.dumps({"model": MODEL, "messages": messages, "stream": False, "options": {"temperature": 0.1}})
        req = urllib.request.Request("http://localhost:11434/api/chat", data=body.encode(),
                                     headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=120).read())["message"]["content"]

    def _fallback(self, question, doc):
        if doc is None:
            return f"I'm sorry, I don't know that from the handbook. Please contact {CONTACT}."
        q = set(rag.tokens(question, expand=True))
        sents = re.split(r"(?<=\.)\s+", rag.DOCS[doc])
        return max(sents, key=lambda s: len(q & set(rag.tokens(s)))) + f" [{doc}]"   # best-overlap sentence

    def ask(self, question):
        doc, score, from_memory = self.retrieve(question)
        answer = self._llm(question, doc) if self.online else self._fallback(question, doc)
        self.topic = doc or self.topic
        self.history.extend([{"role": "user", "content": question}, {"role": "assistant", "content": answer}])
        return answer, doc, score, from_memory


if __name__ == "__main__":
    bot = CampusBot()
    print(f"CampusBot ready | engine: {'Ollama ' + MODEL if bot.online else 'offline extractive fallback'}\n")
    if "--interactive" in sys.argv:
        while (q := input("You: ").strip()).lower() not in {"quit", "exit"}:
            print("Bot:", bot.ask(q)[0], "\n")
        sys.exit()
    stats = Counter()
    for q in ["When are final exams held?", "I was sick and missed one, what now?",
              "How much is the late fine for a library book?", "And how many can I take at once?",
              "Can I pay my fees in parts?", "What is the cafeteria menu today?"]:
        answer, doc, score, mem = bot.ask(q)
        stats["answered" if doc else "declined"] += 1
        tag = f"{doc} via memory" if mem else (f"{doc}, score {score:.2f}" if doc else f"no match, best {score:.2f}")
        print(f"You: {q}\nBot: {answer}\n     ({tag})\n")
    print("Session stats:", dict(stats), f"| memory window holds {len(bot.history)} messages")
