# Track 1 · Prompt Engineering

> 🧭 [⬆ Up](../README.md) · Generative AI › **Track 1 · Prompt Engineering**

Prepared by **Hamna Zahid Khan**, Junior Lecturer

## 📌 About this track

Prompt engineering is the skill of telling an AI model exactly what you want. This track starts with the anatomy of a prompt and moves through prompt types, chain-of-thought and self-consistency, real case studies, prompting inside apps and spreadsheets, comparing AI assistants, text-to-image work, advanced strategies, fine-tuning basics and soft prompts, prompt-hacking defences, and a final project.

**By the end you will be able to:**

- Write complete, testable prompts for text, data and image tasks.
- Choose the right technique (zero/few-shot, CoT, chaining, RAG, fine-tuning) for a job.
- Generate and iterate consistent images with the right settings and aspect ratios.
- Defend AI features against prompt injection, leaking and jailbreaks.
- Evaluate prompt versions with a rubric and present the evidence.

## 🧭 Learning path

```mermaid
flowchart LR
    A["1-2 Basics and prompt types"] --> B["3 Advanced reasoning"]
    B --> C["4-6 Case studies, apps, assistants"]
    C --> D["7-8 Visual art and image settings"]
    D --> E["9-10 Expert strategies and tuning"]
    E --> F["11 Prompt hacking and defences"]
    F --> G["12 Final project"]
```

## 🛠️ Setup

- A free account on at least one AI assistant (ChatGPT, Microsoft Copilot or Google Gemini) and one image tool.
- Python 3.10+ for the `code/` folder. Every script runs offline with the standard library (Session 3 also uses `matplotlib`).
- Notebooks open in Jupyter or Google Colab with the badge at the top of each session.

## 🗂️ Sessions

| # | Session | Time |
|---|---|---|
| 1 | [Getting Started with Prompting](session-01-getting-started-with-prompting.md) | 2 hours |
| 2 | [Types of Prompts and Prompt Priming](session-02-types-of-prompts-and-priming.md) | 2 hours |
| 3 | [Unleashing the Power of Prompts: CoT, Self-Consistency, Generated Knowledge](session-03-unleashing-the-power-of-prompts.md) | 2 hours |
| 4 | [Case Studies: Content, Commercials, Social Media and Icons](session-04-case-studies-content-and-social-media.md) | 2 hours |
| 5 | [Prompting in Apps: Spreadsheets, Personal Style and Comparisons](session-05-prompting-in-apps-sheets-and-style.md) | 2 hours |
| 6 | [Comparing AI Assistants: ChatGPT, Copilot and Gemini](session-06-comparing-ai-assistants.md) | 2 hours |
| 7 | [Transforming Text into Visual Art](session-07-text-to-visual-art.md) | 2 hours |
| 8 | [Image Generation Settings: Iterate, Upscale, Remix, Aspect Ratio](session-08-image-generation-settings.md) | 2 hours |
| 9 | [Advanced Prompting Strategies and AI in Spreadsheets](session-09-advanced-prompting-strategies.md) | 2 hours |
| 10 | [Applied Prompting, Fine-Tuning Basics and Soft Prompts](session-10-applied-prompting-and-prompt-tuning.md) | 2 hours |
| 11 | [Prompt Hacking: Injection, Leaking, Jailbreaking and Defences](session-11-prompt-hacking-and-defences.md) | 2 hours |
| 12 | [Final Project: Mastering the Art of Prompting](session-12-final-project-mastering-prompts.md) | 2 hours |

📝 **Module practice test:** [practice-test.md](practice-test.md) — 20 MCQs + 3 scenario questions with solutions.

## 📋 Track cheat-sheet

| Topic | Remember |
|---|---|
| Prompt anatomy | **Role · Task verb · Context · Audience · Format · Constraints · Delimiters · Self-check** |
| Prompt types | Zero-shot (no examples) · One-shot · Few-shot (2–5 examples) · Priming with role and context |
| Reasoning | Chain-of-thought ("step by step") · Self-consistency (several answers, majority vote) · Generated knowledge (facts first, then answer) |
| Content work | Brief → variations → pick → polish; always state platform, audience and length |
| Spreadsheets | Fixed instruction cell, closed label set, spot-check rows, paste values to freeze |
| Assistants | Compare on the same prompt and a scoring matrix: accuracy, citations, format, speed, privacy |
| Image prompts | **Subject · Setting · Style · Lighting · Composition · Colour · Ratio**; negatives for what to avoid |
| Image settings | Explore → Select → Refine (vary subtle/strong, region, remix) → Finalise (upscale); choose ratio first |
| Consistent characters | Character bible + fixed style string + seed or reference image; change only the scene |
| Expert strategies | Decompose, chain prompts, ask questions first, self-critique; low temperature for facts |
| Customising models | Prompt first → RAG for missing facts → fine-tune or prompt-tune for style at scale |
| Soft prompts | Learned vectors in front of the input; base model frozen; tiny and cheap per task |
| Prompt hacking | Injection (direct/indirect) · Leaking · Jailbreaking |
| Defences | Delimit and escape · Sandwich · Filter · Least privilege · Output checks · No secrets in prompts |
| Evaluation | Test set + rubric, one change per version, report evidence |

## ✅ Track checklist

- [ ] Finished all 12 sessions and their lab tasks
- [ ] Scored at least 4/5 on every session quiz
- [ ] Attempted the [practice test](practice-test.md) in 60 minutes
- [ ] Completed the final project with a prompt spec, scores and safety tests

---
<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer</sub>
