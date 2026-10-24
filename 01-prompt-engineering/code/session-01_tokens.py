"""Rough token estimation: most English text averages ~4 characters per token."""
import re

def estimate_tokens(text: str) -> int:
    words = re.findall(r"\w+|[^\w\s]", text)
    by_chars = len(text) / 4
    by_words = len(words) * 0.75 + sum(1 for w in words if not w.isalnum())
    return round((by_chars + by_words) / 2)

samples = {
    "short question": "What is a prompt?",
    "instruction": "Summarise the attached article in five bullet points for a busy manager.",
    "paragraph": ("Generative AI models predict the next token in a sequence. The quality of the "
                  "answer depends heavily on the clarity, context and constraints in the prompt."),
}
context_window = 8000
for name, text in samples.items():
    t = estimate_tokens(text)
    print(f"{name:15} | chars={len(text):3} | ~tokens={t:3} | % of 8k window={t/context_window:.2%}")

cost_per_1k = 0.0005  # illustrative price in USD per 1,000 input tokens
monthly = 200 * 30 * 1500   # 200 requests/day, 30 days, ~1,500 tokens each
print(f"\nMonthly tokens: {monthly:,}  ->  estimated cost ${monthly/1000*cost_per_1k:.2f}")
