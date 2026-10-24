"""Self-consistency: ask the same CoT question several times, take the majority answer.
The 'model runs' below are SAMPLE reasoning chains (hard-coded) so the demo is reproducible."""
from collections import Counter
import re

question = ("A shop sells pens at Rs 25 each. Ali buys 4 pens and pays with a Rs 500 note. "
            "The shopkeeper gives a 10% discount on the total. How much change does Ali get?")

sample_runs = [
    "4 x 25 = 100. 10% of 100 = 10, so total = 90. Change = 500 - 90 = 410. Answer: 410",
    "Total 100. Discount 10 -> 90. 500 - 90 = 410. Answer: 410",
    "4 pens cost 100. Change before discount = 400. 10% of 400 = 40. Answer: 440",   # flawed chain
    "Cost = 4*25 = 100; after 10% off = 90; change = 410. Answer: 410",
    "100 - 10% = 90. 500 - 90 = 410. Answer: 410",
]

def final_answer(chain):
    return re.search(r"Answer:\s*(\d+)", chain).group(1)

answers = [final_answer(r) for r in sample_runs]
votes = Counter(answers)
print("Question:", question)
for i, (r, a) in enumerate(zip(sample_runs, answers), 1):
    print(f"Run {i}: answer={a}")
best, count = votes.most_common(1)[0]
print("\nVotes:", dict(votes))
print(f"Self-consistent answer: Rs {best}  (confidence {count}/{len(answers)} = {count/len(answers):.0%})")
