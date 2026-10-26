"""
Session 4 · Example 2 — Generate a subtitle (.srt) file from a timed script.

Captions matter: most social video is watched with the sound off, and
captions make content accessible to deaf and hard-of-hearing viewers.
An SRT file is plain text: a number, a time range "HH:MM:SS,mmm --> ...",
the caption text, then a blank line. Video editors (CapCut, Premiere,
DaVinci Resolve) and YouTube all import it.

Long lines are split so that no caption exceeds 42 characters per line,
which is a common broadcast guideline.

Run:  python session-04_srt_maker.py
Creates: session-04_promo.srt
"""
import textwrap

WPM = 150
MAX_CHARS = 42


def stamp(seconds: float) -> str:
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def to_srt(lines):
    blocks, t, n = [], 0.0, 1
    for text in lines:
        # wrap into lines of at most MAX_CHARS, then show 2 lines per caption
        rows = textwrap.wrap(text, MAX_CHARS)
        for k in range(0, len(rows), 2):
            pair = rows[k:k + 2]
            words = sum(len(r.split()) for r in pair)
            dur = max(words / WPM * 60, 1.0)  # at least 1 second on screen
            blocks.append(f"{n}\n{stamp(t)} --> {stamp(t + dur)}\n" + "\n".join(pair) + "\n")
            t += dur
            n += 1
    return "\n".join(blocks)


script = [
    "Ever wished your notes could talk back? Meet StudyBuddy.",
    "Exams pile up, notes are messy, and nobody has time to make flashcards.",
    "StudyBuddy turns your own notes into quizzes and flashcards in seconds, "
    "then reminds you to review just before you forget.",
    "Try it free this week. Link in bio.",
]
srt = to_srt(script)
with open("session-04_promo.srt", "w", encoding="utf-8") as f:
    f.write(srt)
print(srt)
print("Saved -> session-04_promo.srt")
