"""
Session 6 · Example 3 — A CrewAI/AutoGen-style multi-agent team: researcher, writer and reviewer.

Each agent has a role and goal; they exchange messages until the reviewer approves.
Real frameworks put an LLM behind each role; here roles are deterministic.

Run:  python session-06_multi_agent_crew.py
"""
FACTS = {  # the researcher's "knowledge base" (would be web search or RAG)
    "solar": ["Pakistan gets 8-9 hours of sunshine a day in many regions",
              "rooftop panels can cut a home's grid bill substantially",
              "net metering lets households sell surplus power back to the grid"],
}

class Agent:
    def __init__(self, name, role, goal):
        self.name, self.role, self.goal = name, role, goal
    def say(self, text):
        print(f"[{self.name} · {self.role}] {text}")

class Researcher(Agent):
    def act(self, topic):
        notes = FACTS.get(topic, [])
        self.say(f"Found {len(notes)} facts on '{topic}'.")
        return notes

class Writer(Agent):
    def act(self, notes, feedback=None):
        words = ["Going solar makes sense:"] + [n[0].upper() + n[1:] + "." for n in notes]
        if feedback and "call to action" in feedback:
            words.append("Ask a certified installer for a free rooftop survey this week.")
        post = " ".join(words)
        self.say(f"Draft v{2 if feedback else 1} ({len(post.split())} words) ready.")
        return post

class Reviewer(Agent):
    def act(self, post):
        issues = []
        if "installer" not in post:
            issues.append("add a call to action")
        if len(post.split()) > 70:
            issues.append("cut to 70 words")
        if issues:
            self.say("Changes requested: " + "; ".join(issues))
            return False, "; ".join(issues).replace("add a ", "")
        self.say("Approved for publishing.")
        return True, ""

crew = [Researcher("Ayesha", "Researcher", "collect accurate facts"),
        Writer("Bilal", "Writer", "write a short persuasive post"),
        Reviewer("Sana", "Reviewer", "check quality and policy")]
researcher, writer, reviewer = crew
print("CREW:", ", ".join(f"{a.name} ({a.goal})" for a in crew), "\n")

notes = researcher.act("solar")
post, feedback, rounds = writer.act(notes), None, 1
approved, feedback = reviewer.act(post)
while not approved and rounds < 3:
    rounds += 1
    post = writer.act(notes, feedback)
    approved, feedback = reviewer.act(post)

print(f"\nFinished in {rounds} round(s). Final post:\n{post}")
