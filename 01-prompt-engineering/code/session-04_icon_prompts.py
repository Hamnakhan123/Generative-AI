"""Bulk-create consistent icon prompts for an app (style stays fixed, subject changes)."""
STYLE = ("flat vector icon, single subject centred, rounded corners, 2px outline, "
         "palette: deep violet #A78BFA and orange #FF6B1A, white background, no text, 1:1")
subjects = ["calendar", "chat bubble", "graduation cap", "bar chart", "settings gear"]
for i, s in enumerate(subjects, 1):
    print(f"{i}. {s.title():15} -> \"{s} icon, {STYLE}\"")
print(f"\nStyle string length: {len(STYLE)} chars, reused {len(subjects)} times for visual consistency")
