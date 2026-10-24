"""Generate a week of social-media prompts from one campaign brief."""
brief = {"brand": "ChaiCorner", "product": "new cardamom iced tea",
         "audience": "university students in Karachi", "tone": "fun, witty", "cta": "Show your student card for 15% off"}
platforms = {"Instagram": "caption under 40 words + 5 hashtags",
             "LinkedIn": "professional post under 80 words about launching a local brand",
             "X": "tweet under 240 characters with 1 emoji",
             "TikTok": "15-second video script with 3 scenes"}
days = ["Mon", "Wed", "Fri", "Sun"]

def make_prompt(platform, spec):
    return (f"You are a social media manager for {brief['brand']}. Write a post for {platform} ({spec}) "
            f"promoting our {brief['product']} for {brief['audience']}. Tone: {brief['tone']}. "
            f"End with: '{brief['cta']}'.")

print(f"{'Day':4} | {'Platform':9} | Prompt")
print("-" * 100)
for day, (platform, spec) in zip(days, platforms.items()):
    p = make_prompt(platform, spec)
    print(f"{day:4} | {platform:9} | {p[:80]}...")
print("\nFull prompt for Instagram:\n" + make_prompt("Instagram", platforms["Instagram"]))
