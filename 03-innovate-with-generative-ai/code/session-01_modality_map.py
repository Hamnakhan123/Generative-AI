"""
Session 1 · Example 1 — Map a creative task to the right Gen AI modality.

Idea: before opening any tool, decide WHAT kind of output you need
(text, image, audio, video, slides, code). This script does that with
simple keyword rules and prints a starter prompt for each task.

Run:  python session-01_modality_map.py
Only the Python standard library is used.
"""
import re

# Each modality has trigger words and a starter prompt skeleton.
MODALITIES = {
    "text":   {"words": ["essay", "blog", "caption", "email", "report", "script", "post"],
               "tools": "chat assistants (ChatGPT, Gemini, Copilot, Claude)",
               "skeleton": "Act as a {role}. Write a {item} about {topic} for {audience}. Format: {fmt}."},
    "image":  {"words": ["poster", "logo", "illustration", "thumbnail", "photo", "banner"],
               "tools": "image generators (DALL-E, Firefly, Midjourney, Ideogram)",
               "skeleton": "{item} of {topic}, style: {style}, lighting: {light}, aspect ratio {ar}."},
    "audio":  {"words": ["podcast", "voiceover", "jingle", "narration", "music"],
               "tools": "voice and music tools (ElevenLabs, Suno, text-to-speech)",
               "skeleton": "Generate a {item} about {topic}, voice: {voice}, length: {length}."},
    "video":  {"words": ["reel", "video", "short", "trailer", "animation"],
               "tools": "video tools (Runway, Pika, Sora, InVideo, CapCut)",
               "skeleton": "A {length} {item} showing {topic}, camera: {camera}, mood: {mood}."},
    "slides": {"words": ["presentation", "deck", "slides", "pitch"],
               "tools": "slide tools (Gamma, Copilot in PowerPoint, Canva)",
               "skeleton": "Create a {n}-slide deck on {topic} for {audience}; one idea per slide."},
}


def classify(task: str) -> str:
    """Return the modality whose trigger word appears in the task (first match wins).

    We compare WHOLE words. A plain substring test would wrongly find "post"
    inside "poster" and send a poster job to a text tool.
    """
    task_words = set(re.findall(r"[a-z]+", task.lower()))
    for name, info in MODALITIES.items():
        if task_words & set(info["words"]):
            return name
    return "text"  # sensible default: most creative work starts as words


tasks = [
    "Instagram caption for a campus bake sale",
    "Poster for the Spring coding contest",
    "30-second voiceover for the department intro",
    "Reel showing a day in the CS lab",
    "Pitch deck for a student startup",
    "Thank-you note to guest speaker",  # no trigger word -> default
]

print(f"{'Task':45} | {'Modality':8} | Tool category")
print("-" * 100)
for t in tasks:
    m = classify(t)
    print(f"{t:45} | {m:8} | {MODALITIES[m]['tools']}")

print("\nStarter skeleton for the poster task:")
print(MODALITIES["image"]["skeleton"])
