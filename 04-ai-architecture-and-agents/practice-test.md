# 📝 Practice Test · Track 4 · AI Architecture and Agents

> 🧭 [⬅ Back to module](README.md) · Generative AI
>
> ⏱️ Suggested time: 60 minutes · Attempt every question before opening the answers.

---

## Part A · Multiple-choice questions (20)

**Q1. In self-attention, the weights for one token are obtained by...**

- A) Counting word frequencies
- B) Averaging all embeddings equally
- C) Softmax of its query's dot products with every key, scaled by √d_k
- D) Multiplying values by positions

<details><summary>Show answer</summary>

✅ **C) Softmax of its query's dot products with every key, scaled by √d_k** — softmax(QKᵀ/√d_k).

</details>

**Q2. Why do transformers need positional encoding?**

- A) To reduce parameters
- B) To mask padding
- C) To speed up softmax
- D) Attention alone ignores word order

<details><summary>Show answer</summary>

✅ **D) Attention alone ignores word order** — Order must be added back.

</details>

**Q3. Compared with an RNN, a transformer layer...**

- A) Cannot use GPUs
- B) Must process tokens one by one
- C) Has no parameters
- D) Connects any two tokens in one step but costs O(n²) in sequence length

<details><summary>Show answer</summary>

✅ **D) Connects any two tokens in one step but costs O(n²) in sequence length** — Parallel, but quadratic.

</details>

**Q4. GPT-style models are...**

- A) Encoder–decoder only
- B) Decoder-only with causal masking
- C) CNNs
- D) Encoder-only

<details><summary>Show answer</summary>

✅ **B) Decoder-only with causal masking** — They generate left to right.

</details>

**Q5. A batch of 64 RGB images 32×32 in TensorFlow has shape...**

- A) (64, 32, 32, 3)
- B) (3, 64, 32, 32)
- C) (32, 32, 64)
- D) (64, 3, 32, 32)

<details><summary>Show answer</summary>

✅ **A) (64, 32, 32, 3)** — Channels-last.

</details>

**Q6. What does @tf.function do?**

- A) Converts to TF Lite
- B) Starts a TF1 session
- C) Downloads a model
- D) Traces Python code into an optimised, saveable graph

<details><summary>Show answer</summary>

✅ **D) Traces Python code into an optimised, saveable graph** — Graph execution in TF2.

</details>

**Q7. For a 3-class problem with integer labels, the right loss is...**

- A) MSE
- B) Sparse categorical cross-entropy
- C) Hinge
- D) Binary cross-entropy

<details><summary>Show answer</summary>

✅ **B) Sparse categorical cross-entropy** — Softmax + integer labels.

</details>

**Q8. Which Keras API do you need for a model with two inputs?**

- A) None
- B) TF Lite
- C) Sequential
- D) Functional (or Subclassing)

<details><summary>Show answer</summary>

✅ **D) Functional (or Subclassing)** — Sequential is a single stack.

</details>

**Q9. When fine-tuning a pre-trained base you should...**

- A) Use a very small learning rate and recompile after unfreezing
- B) Use a large learning rate
- C) Delete the base
- D) Skip validation

<details><summary>Show answer</summary>

✅ **A) Use a very small learning rate and recompile after unfreezing** — Protect the pre-trained weights.

</details>

**Q10. Training accuracy 99%, validation 72%. The best first action is...**

- A) Remove the validation set
- B) Train longer
- C) Raise the learning rate
- D) Add regularisation such as dropout, augmentation and EarlyStopping

<details><summary>Show answer</summary>

✅ **D) Add regularisation such as dropout, augmentation and EarlyStopping** — Classic overfitting.

</details>

**Q11. TF Serving expects models in...**

- A) Docker images only
- B) Versioned SavedModel folders like models/name/1/
- C) A single .py file
- D) CSV files

<details><summary>Show answer</summary>

✅ **B) Versioned SavedModel folders like models/name/1/** — It serves the highest version.

</details>

**Q12. Dynamic-range quantisation in TF Lite typically makes a model about...**

- A) 100x smaller
- B) Unchanged
- C) 2x larger
- D) 4x smaller with similar accuracy

<details><summary>Show answer</summary>

✅ **D) 4x smaller with similar accuracy** — int8 weights.

</details>

**Q13. A Kubernetes HPA sees 4 pods at 140% CPU with a 70% target. Desired pods =**

- A) 6
- B) 4
- C) 8
- D) 2

<details><summary>Show answer</summary>

✅ **C) 8** — ceil(4 × 1.4 ÷ 0.7) = 8.

</details>

**Q14. Which TFX component stops a broken data batch before training?**

- A) Trainer
- B) Pusher
- C) Tuner
- D) ExampleValidator

<details><summary>Show answer</summary>

✅ **D) ExampleValidator** — It checks data against the schema.

</details>

**Q15. A PSI of 0.31 on a key input feature means...**

- A) The model is perfect
- B) A syntax error
- C) Major drift; investigate and retrain
- D) Stable

<details><summary>Show answer</summary>

✅ **C) Major drift; investigate and retrain** — Above 0.25.

</details>

**Q16. In Q-learning, γ (gamma) controls...**

- A) Number of actions
- B) Learning rate
- C) How much future rewards count
- D) Exploration rate

<details><summary>Show answer</summary>

✅ **C) How much future rewards count** — Discount factor.

</details>

**Q17. In the ReAct pattern, after the agent calls a tool it receives...**

- A) The final answer
- B) An Observation (the tool result)
- C) Nothing
- D) A new system prompt

<details><summary>Show answer</summary>

✅ **B) An Observation (the tool result)** — Thought → Action → Observation.

</details>

**Q18. Which framework models an agent as a state graph with conditional edges and human interrupts?**

- A) CrewAI
- B) LangGraph
- C) TFX
- D) AutoGPT

<details><summary>Show answer</summary>

✅ **B) LangGraph** — Stateful graphs.

</details>

**Q19. Ollama is best described as...**

- A) A vector database
- B) A closed LLM from OpenAI
- C) A local runtime that downloads open models and exposes a REST API
- D) A Kubernetes add-on

<details><summary>Show answer</summary>

✅ **C) A local runtime that downloads open models and exposes a REST API** — Port 11434.

</details>

**Q20. A RAG chatbot finds no document above the similarity threshold. It should...**

- A) Pick a random document
- B) Answer from general knowledge
- C) Say it does not know and point to a human contact
- D) Crash

<details><summary>Show answer</summary>

✅ **C) Say it does not know and point to a human contact** — Grounded or nothing.

</details>


## Part B · Scenario questions (3)

### 🧩 Scenario 1 · A mobile app that reads meter photos offline

A utility company wants field staff to photograph electricity meters and read the digits on the phone, even with no signal. They have 50,000 labelled photos from the head office scanner and 300 phone photos. Design the model, training strategy, conversion and evaluation, and say how you would keep it accurate after launch.

<details><summary>✅ Model solution</summary>

**Model and training:**

- A small CNN (or a pre-trained mobile backbone such as MobileNetV2 from `keras.applications`) for digit recognition.
- **Transfer learning:** pre-train on the 50,000 scanner images **with augmentation** (shifts, blur, brightness, noise) so features survive phone conditions; then **fine-tune** on the 300 phone photos with a learning rate around 1e-4, after recompiling.
- Compare with training from scratch on the 300 photos as a baseline.

**Evaluation:** a held-out set of phone photos only; report accuracy, per-digit recall and a confusion matrix (watch 1/7 and 3/8 confusions); measure latency on a mid-range phone.

**Conversion:** `tf.lite.TFLiteConverter` with dynamic-range quantisation (about 4× smaller), then re-check accuracy on the `.tflite` file; consider full-integer quantisation with a representative dataset if the phone has an NPU. Put preprocessing inside the model.

**After launch:** log low-confidence readings (with consent) for staff to verify; monitor the confidence distribution and image statistics for drift (PSI); retrain through a validated pipeline (ExampleValidator, Evaluator blessing) and ship new model versions with the app update or a model download.

</details>


### 🧩 Scenario 2 · Scaling an exam-results prediction API

A university will expose a model that predicts which students need extra support. Traffic is quiet most days but spikes 15× on result day. Design the serving architecture, the retraining pipeline and the safeguards.

<details><summary>✅ Model solution</summary>

**Serving:**

- Export a versioned **SavedModel** with preprocessing inside; serve it with **TF Serving** in Docker (REST for the portal, gRPC for internal batch jobs).
- Run on **Kubernetes**: Deployment with at least 2 replicas, readiness probe, CPU/memory requests and limits, a Service/Ingress, and an **HPA** (e.g. target 70% CPU, 2–30 pods). Pre-scale before the announced result time because autoscalers react within minutes.

**Pipeline (TFX-style):** ExampleGen from the student information system → StatisticsGen → SchemaGen → **ExampleValidator** (missing grades, impossible values, drift) → Transform → Trainer → **Evaluator** (blessing only if AUC beats the current model and performance is similar across departments and genders) → InfraValidator → Pusher to `models/support/N/`.

**Safeguards:** the prediction supports advisers, it never decides alone (human in the loop); explain the main factors to advisers; restrict access to personal data; log predictions for audit; monitor drift each term; roll back by pointing serving to the previous version.

</details>


### 🧩 Scenario 3 · A local admissions assistant agent

The admissions office wants an assistant that answers applicant questions from the prospectus, calculates total fees and scholarships, and can book a campus-visit slot. Applicant data must stay on campus. Describe the model choice, architecture, tools, guardrails and how you would test it.

<details><summary>✅ Model solution</summary>

**Model:** an open model run locally with **Ollama**, for example **Qwen 2.5 7B** at 4-bit (about 5 GB; strong multilingual support helps Urdu-speaking applicants); a smaller 1.5B model for a low-cost fallback. Low temperature (0.1–0.3).

**Architecture:** a ReAct or LangGraph-style agent:

- **RAG** over the prospectus (chunk → embed with a local embedding model → vector store → grounded prompt with citations; below the similarity threshold say "I don't know" and give the office contact).
- **Tools:** `fee_calculator(programme, semesters, scholarship_percent)` implemented in code (never let the model do arithmetic), `visit_slots(date)` and `book_visit(name, email, slot)`.
- **Memory:** a sliding window of recent turns so follow-ups work.

**Guardrails:** step limit; tools validate arguments; booking requires the applicant to confirm the details; no admission decisions or scholarship promises (escalate to staff); treat retrieved text as untrusted (prompt-injection defence); no personal data leaves the server; full audit log.

**Testing:** a fixed set of 50+ questions (fees, deadlines, eligibility, follow-ups, out-of-scope, injection attempts) scored for correctness, citation and refusal; re-run whenever the model, prompt or prospectus changes; pilot with staff before applicants.

</details>

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer</sub>
