"""Score Gen AI risks by likelihood x impact (1-5 each) for one use case:
an AI chatbot that answers student admission questions."""
risks = {
    "Hallucinated fee or deadline": (4, 5),
    "Personal data pasted into chat": (3, 4),
    "Biased tone towards some applicants": (2, 4),
    "Copyright issue in generated images": (1, 2),
    "Service outage on result day": (2, 3),
}
ranked = sorted(risks.items(), key=lambda kv: kv[1][0] * kv[1][1], reverse=True)
print(f"{'Risk':38} L  I  Score  Level")
for name, (l, i) in ranked:
    s = l * i
    level = "HIGH" if s >= 15 else "MEDIUM" if s >= 8 else "LOW"
    print(f"{name:38} {l}  {i}  {s:>5}  {level}")
