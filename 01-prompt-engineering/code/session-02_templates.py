"""A tiny reusable prompt-template library using string.Template."""
from string import Template

TEMPLATES = {
    "zero_shot": Template("$task\n\nText: \"$text\""),
    "role": Template("You are $role. $task\nAudience: $audience. Keep it under $words words."),
    "priming": Template(
        "For the rest of this chat, act as $role.\n"
        "Rules: $rules\n"
        "Reply only with 'Ready' now. Wait for my first request."),
}

def few_shot(task, examples, query):
    """Build a few-shot prompt: instruction + labelled examples + new input."""
    lines = [task, ""]
    for text, label in examples:
        lines += [f"Review: {text}", f"Sentiment: {label}", ""]
    lines += [f"Review: {query}", "Sentiment:"]
    return "\n".join(lines)

print("--- ZERO-SHOT ---")
print(TEMPLATES["zero_shot"].substitute(task="Classify the sentiment as Positive, Negative or Neutral.",
                                         text="The delivery was late but the biryani was amazing."))
print("\n--- ROLE PROMPT ---")
print(TEMPLATES["role"].substitute(role="a patient maths tutor", task="Explain percentages.",
                                    audience="grade 6 students", words=100))
print("\n--- PRIMING PROMPT ---")
print(TEMPLATES["priming"].substitute(role="an English grammar coach",
      rules="correct my sentence, explain the mistake in one line, give one more example"))
print("\n--- FEW-SHOT PROMPT ---")
print(few_shot("Classify each review as Positive or Negative.",
               [("Battery lasts all day, love it!", "Positive"),
                ("Screen cracked after one week.", "Negative")],
               "Fast charging and a bright display."))
try:
    TEMPLATES["role"].substitute(role="a chef")
except KeyError as e:
    print(f"\nMissing placeholder detected: {e}  -> templates protect you from half-filled prompts")
