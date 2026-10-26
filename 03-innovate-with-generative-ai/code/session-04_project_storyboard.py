"""
Session 4 · Mini project (full solution) — Storyboard to edit plan.

Real-life problem: the department wants a 45-second promo video made with AI
clips (text-to-video), an AI voiceover and captions. Before generating
anything (each clip costs credits and time), plan it:

  * a shot list with a text-to-video prompt for every shot,
  * narration per shot, timed at 150 wpm,
  * a check that each shot is long enough for its narration,
  * total runtime vs the 45 s target,
  * a JSON edit plan an editor (or a script) can follow.

Run:  python session-04_project_storyboard.py
Creates: session-04_edit_plan.json
"""
import json

WPM, TARGET = 150, 45
shots = [
    # (shot length s, visual prompt for a text-to-video tool, narration, music cue)
    (6, "Slow drone shot over a university campus at sunrise, warm light, cinematic",
        "Every great career starts with one good decision.", "soft piano in"),
    (8, "Close-up of hands typing code on a laptop, screen glow, shallow depth of field",
        "In our computer science labs you build real projects from week one.", "beat starts"),
    (8, "Students laughing around a whiteboard covered in diagrams, handheld camera",
        "You learn with people who push you, help you and celebrate with you.", "beat"),
    (7, "A robot arm sorting coloured blocks, macro lens, studio lighting",
        "Robotics, AI and data science, taught by practising engineers.", "beat"),
    (8, "Graduates throwing caps in the air, slow motion, golden hour",
        "Our graduates work at startups and global companies.", "swell"),
    (6, "Logo reveal on dark background with orange glow particles",
        "Applications are open. Visit our website today.", "final hit"),
]

plan, t, problems = [], 0.0, []
print(f"{'#':>2} {'Len':>4} {'Talk':>5}  Visual prompt")
for i, (length, visual, narration, music) in enumerate(shots, 1):
    talk = len(narration.split()) / WPM * 60
    flag = "" if talk <= length - 0.5 else "  <-- narration too long for shot"
    if flag:
        problems.append(i)
    print(f"{i:2} {length:4} {talk:5.1f}  {visual[:58]}{flag}")
    plan.append({"shot": i, "start": t, "end": t + length, "visual_prompt": visual,
                 "narration": narration, "music": music, "caption": narration})
    t += length

print(f"\nRuntime {t:.0f} s vs target {TARGET} s -> {'OK' if abs(t - TARGET) <= 2 else 'adjust shots'}")
print("All narration fits its shot" if not problems else f"Rewrite narration for shots {problems}")
with open("session-04_edit_plan.json", "w") as f:
    json.dump({"title": "CS Department Promo", "fps": 30, "shots": plan}, f, indent=2)
print("Saved -> session-04_edit_plan.json")
print("\nFirst entry of the edit plan:")
print(json.dumps(plan[0], indent=2))
