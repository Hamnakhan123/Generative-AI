"""
Session 6 · Example 3 — Back-schedule an event checklist from its date.

Planners work BACKWARDS from the event day: "posters must be printed 10 days
before", "venue booked 30 days before". Give an AI the list of tasks and
lead times, but let code compute the dates (AIs often miscount weekdays).
Tasks that fall on a Sunday are moved to the Saturday before.

Run:  python session-06_event_checklist.py
"""
from datetime import date, timedelta

EVENT = date(2026, 12, 12)   # Saturday 12 December 2026
tasks = [  # (days before event, task, owner)
    (42, "Agree goals, budget and theme", "Lead"),
    (35, "Book auditorium and AV equipment", "Logistics"),
    (28, "Confirm speakers and judges", "Lead"),
    (21, "Launch registration form and social campaign", "Marketing"),
    (14, "Print posters and badges", "Design"),
    (6,  "Send reminder email and agenda", "Marketing"),
    (2,  "Rehearsal and tech check", "Logistics"),
    (0,  "EVENT DAY", "Everyone"),
    (-3, "Send thank-you notes and feedback survey", "Lead"),
]

print(f"Event: {EVENT:%A %d %B %Y}\n")
print(f"{'Due':16}{'D-':>5}  {'Owner':10} Task")
for days, task, owner in sorted(tasks, reverse=True):
    due = EVENT - timedelta(days=days)
    moved = ""
    if due.weekday() == 6:              # Sunday -> Saturday before
        due -= timedelta(days=1)
        moved = "  (moved from Sunday)"
    print(f"{due:%a %d %b %Y}{days:>5}  {owner:10} {task}{moved}")
