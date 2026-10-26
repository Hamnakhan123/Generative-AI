"""
Session 3 · Example 2 — Is the text on your AI poster readable? (WCAG contrast)

AI tools pick attractive colours, not necessarily readable ones. The Web
Content Accessibility Guidelines (WCAG 2) define a contrast ratio:
    (L_lighter + 0.05) / (L_darker + 0.05)
where L is the "relative luminance" of each colour. Body text needs at least
4.5:1 (AA); large headings need 3:1; 7:1 is the stricter AAA level.

Run:  python session-03_contrast_checker.py
"""


def luminance(hex_colour: str) -> float:
    """Relative luminance of an sRGB colour such as '#FF6B1A'."""
    hex_colour = hex_colour.lstrip("#")
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    r, g, b = linear
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def verdict(ratio: float) -> str:
    if ratio >= 7:
        return "AAA (excellent)"
    if ratio >= 4.5:
        return "AA (good for body text)"
    if ratio >= 3:
        return "large headings only"
    return "FAIL - hard to read"


pairs = [
    ("Cream text on night background", "#F5EEFF", "#0A0716"),
    ("Gold text on night background",  "#FCD34D", "#0A0716"),
    ("Orange text on night background", "#FF6B1A", "#0A0716"),
    ("White text on orange button",    "#FFFFFF", "#FF6B1A"),
    ("Violet text on gold banner",     "#A78BFA", "#FCD34D"),
    ("Grey text on white page",        "#9CA3AF", "#FFFFFF"),
]
print(f"{'Pair':34} {'Ratio':>6}  Verdict")
for name, fg, bg in pairs:
    r = contrast(fg, bg)
    print(f"{name:34} {r:6.2f}  {verdict(r)}")
