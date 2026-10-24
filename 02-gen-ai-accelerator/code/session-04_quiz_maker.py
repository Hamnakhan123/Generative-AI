"""Build a self-quiz prompt from your own notes, then grade your answers.
Asking AI to quiz you (active recall) beats asking it to explain the topic again."""
notes = ["Generative AI creates new content such as text, images and audio.",
         "A large language model predicts the next token.",
         "Hallucination is a confident but false output."]
prompt = ("You are my study buddy. Using ONLY the notes below, ask me one question at a time, "
          "wait for my answer, then tell me if I am right and why.\nNOTES:\n" +
          "\n".join(f"- {n}" for n in notes))
print(prompt)

key = {"Q1": "next token", "Q2": "false"}
mine = {"Q1": "It predicts the next token", "Q2": "an output that is always true"}
score = sum(key[q] in mine[q].lower() for q in key)
print(f"\nSelf-check score: {score}/{len(key)}")
