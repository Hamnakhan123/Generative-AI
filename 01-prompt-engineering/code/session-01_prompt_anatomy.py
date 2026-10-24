"""Build a well-structured prompt from its six building blocks."""
from dataclasses import dataclass, field

@dataclass
class Prompt:
    role: str = ""
    context: str = ""
    task: str = ""
    constraints: list = field(default_factory=list)
    output_format: str = ""
    examples: list = field(default_factory=list)

    def render(self) -> str:
        parts = []
        if self.role:        parts.append(f"ROLE: You are {self.role}.")
        if self.context:     parts.append(f"CONTEXT: {self.context}")
        if self.task:        parts.append(f"TASK: {self.task}")
        if self.constraints: parts.append("CONSTRAINTS:\n" + "\n".join(f"- {c}" for c in self.constraints))
        if self.output_format: parts.append(f"OUTPUT FORMAT: {self.output_format}")
        for i, (inp, out) in enumerate(self.examples, 1):
            parts.append(f"EXAMPLE {i}:\nInput: {inp}\nOutput: {out}")
        return "\n\n".join(parts)

def score(p: Prompt) -> int:
    """Very rough 'completeness' score: one point per filled block (max 6)."""
    return sum(bool(x) for x in [p.role, p.context, p.task, p.constraints, p.output_format, p.examples])

weak = Prompt(task="Write about climate change.")
strong = Prompt(
    role="a friendly science teacher for grade 8 students in Karachi",
    context="Students have just studied the water cycle and have 10 minutes left in class.",
    task="Explain how climate change affects rainfall in Pakistan.",
    constraints=["Maximum 120 words", "Use one local example", "Avoid jargon"],
    output_format="3 short bullet points followed by one quiz question",
)
for name, p in [("WEAK", weak), ("STRONG", strong)]:
    print(f"===== {name} PROMPT (completeness {score(p)}/6) =====")
    print(p.render())
    print()
