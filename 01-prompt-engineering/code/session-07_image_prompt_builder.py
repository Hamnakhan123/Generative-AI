"""Compose image-generation prompts from parts, Midjourney-style parameters included."""
def image_prompt(subject, setting="", style="", lighting="", camera="", ar="1:1", stylize=None, no=None, version=None):
    core = ", ".join(x for x in [subject, setting, style, lighting, camera] if x)
    params = [f"--ar {ar}"]
    if stylize is not None: params.append(f"--stylize {stylize}")
    if no: params.append(f"--no {no}")
    if version: params.append(f"--v {version}")
    return f"{core} {' '.join(params)}"

prompts = [
    image_prompt("a red vintage rickshaw", "busy Karachi street at dusk", "cinematic photo",
                 "neon reflections on wet road", "35mm lens, shallow depth of field", ar="16:9", stylize=250),
    image_prompt("minimal logo of a steaming chai cup", style="flat vector, two colours",
                 ar="1:1", no="text, gradients"),
    image_prompt("portrait of an elderly fisherman", "Gwadar harbour", "oil painting",
                 "golden hour", ar="4:5", stylize=600),
]
for i, p in enumerate(prompts, 1):
    print(f"{i}. /imagine prompt: {p}\n")
