"""Pull action items out of meeting notes - the same structure you should ask an AI
assistant for ("list owner, task, due date as a table"), and a way to check its work."""
import re

notes = """Dept meeting 14 Oct.
Discussed mid-term schedule. Sana will share the room plan by Friday.
Lab 3 PCs are slow - Bilal to raise IT ticket by Monday.
New AI policy draft: Hamna to circulate to faculty by 20 Oct.
Next meeting in two weeks."""

pattern = re.compile(r"(?P<owner>[A-Z][a-z]+) (?:will|to) (?P<task>.+?) by (?P<due>[\w ]+?)\.")
items = [m.groupdict() for m in pattern.finditer(notes)]

print(f"{'Owner':7} | {'Task':38} | Due")
print("-" * 60)
for it in items:
    print(f"{it['owner']:7} | {it['task']:38} | {it['due']}")
print(f"\n{len(items)} action items found")
