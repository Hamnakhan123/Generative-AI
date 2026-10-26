"""
Session 4 · Example 1 — How long will my narration be?

Text-to-speech and human narrators speak at roughly 130-160 words per minute
(wpm). Before generating any audio, time the script so each scene fits its
video clip. 150 wpm = 2.5 words per second.

Run:  python session-04_script_timer.py
"""
WPM = 150
script = [
    ("Hook",     "Ever wished your notes could talk back? Meet StudyBuddy."),
    ("Problem",  "Exams pile up, notes are messy, and nobody has time to make flashcards."),
    ("Solution", "StudyBuddy turns your own notes into quizzes and flashcards in seconds, "
                 "then reminds you to review just before you forget."),
    ("Proof",    "In our pilot, forty students used it for two weeks."),
    ("CTA",      "Try it free this week. Link in bio."),
]

total = 0.0
print(f"{'Scene':9} {'Words':>5} {'Seconds':>8}  Start-End")
for name, text in script:
    words = len(text.split())
    secs = words / WPM * 60
    print(f"{name:9} {words:5} {secs:8.1f}  {total:5.1f}-{total + secs:5.1f}s")
    total += secs
print(f"Total: {total:.1f} s at {WPM} wpm")
limit = 30
print("Fits a 30-second reel" if total <= limit else f"Too long by {total - limit:.1f} s: cut words")
