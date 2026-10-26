"""
Session 2 · Example 3 — Check social posts against platform rules before posting.

AI happily writes a 400-character post for a platform that cuts off at 280,
or stuffs in 15 hashtags. This checker flags such problems automatically.
Limits below are the commonly published ones at the time of writing; check
each platform's help page because they change.

Run:  python session-02_platform_fit.py
"""
import re

RULES = {
    # platform: (max characters, recommended max hashtags)
    "X (Twitter)": (280, 2),
    "Instagram":   (2200, 5),
    "LinkedIn":    (3000, 3),
    "Facebook":    (63206, 3),
}


def check(platform: str, post: str) -> list:
    limit, max_tags = RULES[platform]
    problems = []
    if len(post) > limit:
        problems.append(f"too long: {len(post)}/{limit} characters")
    tags = re.findall(r"#\w+", post)
    if len(tags) > max_tags:
        problems.append(f"{len(tags)} hashtags (keep to {max_tags} or fewer)")
    if not re.search(r"(register|join|read|sign up|link|visit|comment)", post, re.I):
        problems.append("no call to action")
    return problems


posts = {
    "X (Twitter)": "Our AI Study Skills workshop is this Thursday 3 pm in Lab 4! Learn to quiz yourself "
                   "with AI, build flashcards, and stay within the integrity rules. Free for all "
                   "first-years, snacks included, bring your laptop and your questions, see you there "
                   "#AI #StudySmart #Karachi #Students",
    "LinkedIn":    "Proud to host our first AI Study Skills workshop for first-year students. "
                   "We covered tutor-mode prompting, flashcards and academic integrity. "
                   "Read the full recap at the link in comments. #AI #Education",
}

for platform, post in posts.items():
    issues = check(platform, post)
    status = "OK" if not issues else "FIX -> " + "; ".join(issues)
    print(f"{platform:12} {len(post):4} chars  {status}")
