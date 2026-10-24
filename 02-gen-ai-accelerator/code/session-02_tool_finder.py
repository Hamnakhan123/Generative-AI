"""Shortlist Gen AI tools for a task by category, free tier and data-safety needs.
The catalogue is a teaching snapshot - tool features and prices change, so check each site."""
TOOLS = [
    # name, category, free tier?, can disable training on chats?
    ("ChatGPT", "text", True, True),
    ("Google Gemini", "text", True, True),
    ("Microsoft Copilot", "text", True, True),
    ("Claude", "text", True, True),
    ("Perplexity", "research", True, True),
    ("NotebookLM", "research", True, True),
    ("Canva Magic Studio", "image", True, False),
    ("Adobe Firefly", "image", True, True),
    ("Midjourney", "image", False, False),
    ("ElevenLabs", "audio", True, False),
    ("Runway", "video", True, False),
    ("GitHub Copilot", "code", True, True),
    ("Gamma", "slides", True, False),
]

def shortlist(category, need_free=True, need_privacy=False):
    return [n for n, c, free, priv in TOOLS
            if c == category and (free or not need_free) and (priv or not need_privacy)]

jobs = [("Summarise 5 research papers with sources", "research", True, True),
        ("Poster for a college event", "image", True, False),
        ("Draft a lesson plan on recursion", "text", True, True),
        ("Pitch deck in 10 minutes", "slides", True, False)]
for job, cat, free, priv in jobs:
    print(f"{job}\n  -> {', '.join(shortlist(cat, free, priv)) or 'no match: relax a filter'}")
