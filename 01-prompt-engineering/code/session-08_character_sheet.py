"""Bulk character creation: keep a fixed 'character bible' and vary only pose/scene.
Re-using the same seed (where the tool supports it) also helps consistency."""
character = ("Zara, 10-year-old girl, curly black hair in two puffs, round glasses, yellow raincoat, "
             "red sneakers, cheerful expression")
style = "children's book illustration, soft watercolour, white background"
seed = 4821
scenes = ["waving hello", "reading a book under a tree", "jumping in a puddle",
          "looking through a telescope at night", "sharing lunch with a friend"]
for n, scene in enumerate(scenes, 1):
    print(f"Panel {n}: {character}, {scene}, {style} --ar 3:2 --seed {seed}")
print(f"\nCharacter bible: {len(character.split(', '))} fixed traits reused across {len(scenes)} panels")
