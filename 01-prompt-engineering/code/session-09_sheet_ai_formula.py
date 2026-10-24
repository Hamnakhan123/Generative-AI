"""Simulates an '=AI(prompt, cell)' column in a spreadsheet: one prompt template applied per row.
The model call is replaced by a deterministic rule so the demo runs offline (SAMPLE behaviour)."""
rows = [("Order #101", "The parcel arrived broken and support never replied."),
        ("Order #102", "Fast delivery, great packaging, will buy again!"),
        ("Order #103", "Item is okay, but delivery took 9 days.")]
TEMPLATE = "Classify the customer feedback as Positive, Negative or Mixed and give a 5-word reason: {text}"

def fake_model(prompt):
    t = prompt.lower()
    neg = sum(w in t for w in ["broken", "never", "took 9 days", "late"])
    pos = sum(w in t for w in ["fast", "great", "again", "okay"])
    label = "Mixed" if neg and pos else ("Negative" if neg else "Positive")
    reason = {"Negative": "damaged item, no support reply", "Positive": "fast delivery and good packaging",
              "Mixed": "fine product, slow delivery time"}[label]
    return label, reason

print(f"{'Row':11} | {'Label':8} | Reason")
for order, text in rows:
    label, reason = fake_model(TEMPLATE.format(text=text))
    print(f"{order:11} | {label:8} | {reason}")
print("\nPrompt sent per row:\n" + TEMPLATE.format(text=rows[0][1]))
