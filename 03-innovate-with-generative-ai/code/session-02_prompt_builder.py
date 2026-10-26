"""
Session 2 · Example 1 — A reusable prompt builder for written content.

A good writing prompt has six parts: Role, Task, Audience, Context,
Format and Constraints (the "RTACFC" checklist used in this session).
This class assembles them and refuses to build a prompt with gaps,
the same way a careful writer checks a brief before starting.

Run:  python session-02_prompt_builder.py
"""
from dataclasses import dataclass, field


@dataclass
class WritingPrompt:
    role: str = ""
    task: str = ""
    audience: str = ""
    context: str = ""
    fmt: str = ""
    constraints: list = field(default_factory=list)

    REQUIRED = ("role", "task", "audience", "fmt")

    def missing(self) -> list:
        """Names of the required parts that are still empty."""
        return [name for name in self.REQUIRED if not getattr(self, name).strip()]

    def build(self) -> str:
        gaps = self.missing()
        if gaps:
            raise ValueError(f"Prompt is incomplete, please fill: {', '.join(gaps)}")
        lines = [
            f"You are {self.role}.",
            f"Task: {self.task}",
            f"Audience: {self.audience}",
        ]
        if self.context:
            lines.append(f'Context: """{self.context}"""')
        lines.append(f"Format: {self.fmt}")
        if self.constraints:
            lines.append("Rules:")
            lines += [f"- {c}" for c in self.constraints]
        return "\n".join(lines)


# 1) A vague prompt is caught before it wastes a generation.
vague = WritingPrompt(task="write a blog about AI")
try:
    vague.build()
except ValueError as err:
    print("Caught:", err)

# 2) A complete prompt for a real assignment.
blog = WritingPrompt(
    role="a friendly tech writer who explains ideas with everyday examples",
    task="Write a 600-word blog post titled 'Five ways AI helps first-year students study smarter'.",
    audience="first-year university students in Karachi, new to AI tools",
    context="The campus allows AI for brainstorming and feedback, not for writing graded work.",
    fmt="H1 title, 80-word intro, five H2 sections with one example each, 60-word conclusion with a call to action",
    constraints=["Plain English, sentences under 20 words", "Mention academic integrity once",
                 "No made-up statistics; write [SOURCE NEEDED] if a number is required"],
)
print("\n" + blog.build())
