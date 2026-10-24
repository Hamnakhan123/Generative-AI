"""Leitner-box spaced repetition: cards you get right move to a box reviewed less often.
Pair it with AI-generated flashcards so you study, not just read."""
INTERVAL = {1: 1, 2: 3, 3: 7, 4: 14}   # box -> days until next review

cards = {"What is a token?": 1, "Define hallucination": 1, "What does temperature control?": 1}
# One week of simulated answers: True = recalled correctly
answers = {
    "What is a token?": [True, True, True],
    "Define hallucination": [False, True, True],
    "What does temperature control?": [True, False, True],
}
for card, results in answers.items():
    box, day, log = 1, 0, []
    for ok in results:
        box = min(box + 1, 4) if ok else 1
        day += INTERVAL[box]
        log.append(f"{'right' if ok else 'wrong'}->box{box}")
    print(f"{card:32} {' | '.join(log)}  next review: day {day}")
