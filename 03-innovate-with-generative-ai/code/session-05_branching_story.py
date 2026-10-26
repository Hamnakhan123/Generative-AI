"""
Session 5 · Example 3 — Check an interactive (choose-your-own-path) story.

Interactive stories are graphs: each scene is a node, each choice an edge.
When an AI writes branches, it often leaves dead ends (a choice that points
to a scene that does not exist) or scenes nobody can reach. A breadth-first
search finds every reachable scene, every ending and every broken link.

Run:  python session-05_branching_story.py
"""
from collections import deque

story = {
    "start":       {"text": "Your bot can now write full assignments.",
                    "choices": {"Sell it to classmates": "sell", "Turn it into a tutor": "tutor"}},
    "sell":        {"text": "Money rolls in, then a teacher calls you in.",
                    "choices": {"Confess": "confess", "Deny everything": "deny"}},
    "tutor":       {"text": "The tutor-bot gives hints only. Grades go up.",
                    "choices": {"Enter the innovation fair": "fair_win"}},
    "confess":     {"text": "You lose marks but keep your integrity.", "choices": {}},
    "deny":        {"text": "The logs prove it. Suspension.", "choices": {"Appeal": "appeal"}},  # broken
    "fair_win":    {"text": "You win the fair and a summer internship.", "choices": {}},
    "secret_room": {"text": "A scene the writer forgot to link.", "choices": {}},
}


def analyse(graph, start="start"):
    seen, queue, broken, endings = {start}, deque([(start, [start])]), [], []
    paths = {}
    while queue:
        node, path = queue.popleft()
        choices = graph[node]["choices"]
        if not choices:
            endings.append(node)
            paths[node] = path
        for label, target in choices.items():
            if target not in graph:
                broken.append((node, label, target))
            elif target not in seen:
                seen.add(target)
                queue.append((target, path + [target]))
    unreachable = sorted(set(graph) - seen)
    return endings, broken, unreachable, paths


endings, broken, unreachable, paths = analyse(story)
print("Endings found:", endings)
for e in endings:
    print(f"  shortest path to '{e}': {' -> '.join(paths[e])}")
print("Broken links:", [f"{n} --'{l}'--> {t}" for n, l, t in broken])
print("Unreachable scenes:", unreachable)
print("Story is", "VALID" if not broken and not unreachable else "NOT valid yet: fix the items above")
