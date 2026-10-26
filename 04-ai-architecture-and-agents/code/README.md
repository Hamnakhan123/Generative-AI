# 💻 Code · Track 4 · AI Architecture and Agents

> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Every script below is complete and runnable on its own, and each one is used by a session page that shows the real output it produced. Files named `*_project_*.py` are the full solutions to each session's real-life mini project.

[⬅ Back to the track](../README.md)

## ⚙️ Setup

```bash
pip install tensorflow scikit-learn matplotlib torch   # torch only for Session 2's mini project
cd code
python session-01_attention_numpy.py
```

All outputs on the session pages were produced by running these files with **TensorFlow 2.21 / Keras 3** and PyTorch 2.x on Python 3.12 (CPU). Small numeric differences on other machines or versions are normal.

Notebooks (`.ipynb`) contain every Python example of a session, already executed with saved output. Open them from the Colab badge at the top of each session page (Colab has TensorFlow pre-installed), or locally with `jupyter notebook`.

Session 7 scripts talk to a local LLM through [Ollama](https://ollama.com) when it is running (`ollama pull qwen2.5:7b`, `ollama pull deepseek-r1:7b`) and fall back to an offline engine otherwise. Run `python session-07_project_chatbot.py --interactive` to chat with CampusBot.

## 📂 Files

### [Session 1 · Transformers and the Attention Mechanism](../session-01-transformers-and-attention.md)

| File | What it does | How to run |
|---|---|---|
| [`session-01-transformers-and-attention.ipynb`](session-01-transformers-and-attention.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-01-transformers-and-attention.ipynb` |
| [`session-01_attention_numpy.py`](session-01_attention_numpy.py) | Scaled dot-product self-attention, step by step in NumPy. | `python session-01_attention_numpy.py` |
| [`session-01_positional_encoding.py`](session-01_positional_encoding.py) | Sinusoidal positional encoding and why word order needs it. | `python session-01_positional_encoding.py` |
| [`session-01_multihead_compare.py`](session-01_multihead_compare.py) | Multi-head attention with Keras, and transformers vs RNNs vs CNNs. | `python session-01_multihead_compare.py` |
| [`session-01_project_pronoun_resolver.py`](session-01_project_pronoun_resolver.py) | Mini project (full solution) — Resolve "it" with self-attention. | `python session-01_project_pronoun_resolver.py` |
| [`session-01_positional_encoding.png`](session-01_positional_encoding.png) | Heatmap of the sinusoidal positional encoding | created by `python session-01_positional_encoding.py` |
| [`session-01_attention_heatmap.png`](session-01_attention_heatmap.png) | Attention maps for the two pronoun sentences | created by `python session-01_project_pronoun_resolver.py` |

### [Session 2 · TensorFlow for Deep Learning Operations](../session-02-tensorflow-deep-learning-operations.md)

| File | What it does | How to run |
|---|---|---|
| [`session-02-tensorflow-deep-learning-operations.ipynb`](session-02-tensorflow-deep-learning-operations.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-02-tensorflow-deep-learning-operations.ipynb` |
| [`session-02_tensors_basics.py`](session-02_tensors_basics.py) | Tensors: creating, shaping, broadcasting and Variables in TensorFlow. | `python session-02_tensors_basics.py` |
| [`session-02_graphs_and_gradients.py`](session-02_graphs_and_gradients.py) | Computational graphs with tf.function and automatic differentiation. | `python session-02_graphs_and_gradients.py` |
| [`session-02_losses_optimizers.py`](session-02_losses_optimizers.py) | Loss functions by hand vs tf.keras.losses, and optimisers compared. | `python session-02_losses_optimizers.py` |
| [`session-02_project_rent_predictor.py`](session-02_project_rent_predictor.py) | Mini project (full solution) — Rent predictor trained with a custom TF loop, then PyTorch. | `python session-02_project_rent_predictor.py` |
| [`session-02_optimizers.png`](session-02_optimizers.png) | Loss curves of SGD, momentum, RMSprop and Adam | created by `python session-02_losses_optimizers.py` |

### [Session 3 · Mastering the Keras API for Model Development](../session-03-keras-api-model-development.md)

| File | What it does | How to run |
|---|---|---|
| [`session-03-keras-api-model-development.ipynb`](session-03-keras-api-model-development.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-03-keras-api-model-development.ipynb` |
| [`session-03_three_apis.py`](session-03_three_apis.py) | One model, three Keras APIs: Sequential, Functional and Subclassing. | `python session-03_three_apis.py` |
| [`session-03_cnn_digits.py`](session-03_cnn_digits.py) | A CNN in Keras on handwritten digits, with proper evaluation. | `python session-03_cnn_digits.py` |
| [`session-03_lstm_forecast.py`](session-03_lstm_forecast.py) | An RNN (LSTM) in Keras that forecasts next-hour electricity demand. | `python session-03_lstm_forecast.py` |
| [`session-03_project_transfer_learning.py`](session-03_project_transfer_learning.py) | Mini project (full solution) — Transfer learning when labels are scarce. | `python session-03_project_transfer_learning.py` |
| [`session-03_cnn_training.png`](session-03_cnn_training.png) | CNN training and validation accuracy curves | created by `python session-03_cnn_digits.py` |
| [`session-03_transfer_learning.png`](session-03_transfer_learning.png) | Accuracy of scratch vs transfer-learning strategies | created by `python session-03_project_transfer_learning.py` |

### [Session 4 · Scalable Deployment: Serving, Lite, Kubernetes and TFX](../session-04-scalable-deployment.md)

| File | What it does | How to run |
|---|---|---|
| [`session-04-scalable-deployment.ipynb`](session-04-scalable-deployment.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-04-scalable-deployment.ipynb` |
| [`session-04_savedmodel_export.py`](session-04_savedmodel_export.py) | Export a Keras model as a versioned SavedModel, the format TF Serving loads. | `python session-04_savedmodel_export.py` |
| [`session-04_tflite_convert.py`](session-04_tflite_convert.py) | Convert a Keras model to TensorFlow Lite, quantise it and run it with the interpreter. | `python session-04_tflite_convert.py` |
| [`session-04_autoscaling.py`](session-04_autoscaling.py) | How a Kubernetes HorizontalPodAutoscaler sizes a model service over a day. | `python session-04_autoscaling.py` |
| [`session-04_project_mini_tfx_pipeline.py`](session-04_project_mini_tfx_pipeline.py) | Mini project (full solution) — A mini TFX-style pipeline with validation gates. | `python session-04_project_mini_tfx_pipeline.py` |
| [`session-04_k8s_deployment.yaml`](session-04_k8s_deployment.yaml) | Kubernetes Deployment, Service and HorizontalPodAutoscaler for TF Serving | `kubectl apply -f session-04_k8s_deployment.yaml` (needs a cluster) |
| [`session-04_autoscaling.png`](session-04_autoscaling.png) | Traffic vs pods chart from the HPA simulation | created by `python session-04_autoscaling.py` |

### [Session 5 · Real-World AI Pipelines and Reinforcement Learning](../session-05-ai-pipelines-and-reinforcement-learning.md)

| File | What it does | How to run |
|---|---|---|
| [`session-05-ai-pipelines-and-reinforcement-learning.ipynb`](session-05-ai-pipelines-and-reinforcement-learning.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-05-ai-pipelines-and-reinforcement-learning.ipynb` |
| [`session-05_drift_monitor.py`](session-05_drift_monitor.py) | Monitoring a live AI pipeline for data drift with the Population Stability Index (PSI). | `python session-05_drift_monitor.py` |
| [`session-05_policy_gradient_tf.py`](session-05_policy_gradient_tf.py) | Reinforcement learning with TensorFlow: a policy-gradient (REINFORCE) agent. | `python session-05_policy_gradient_tf.py` |
| [`session-05_quantum_toy.py`](session-05_quantum_toy.py) | What TensorFlow Quantum does, simulated with NumPy: a one-qubit variational classifier. | `python session-05_quantum_toy.py` |
| [`session-05_project_delivery_agent.py`](session-05_project_delivery_agent.py) | Mini project (full solution) — Q-learning delivery robot in a warehouse. | `python session-05_project_delivery_agent.py` |
| [`session-05_q_learning_rewards.png`](session-05_q_learning_rewards.png) | Reward-per-episode learning curve of the delivery robot | created by `python session-05_project_delivery_agent.py` |

### [Session 6 · Understanding AI Agents and Agent Frameworks](../session-06-understanding-ai-agents.md)

| File | What it does | How to run |
|---|---|---|
| [`session-06-understanding-ai-agents.ipynb`](session-06-understanding-ai-agents.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-06-understanding-ai-agents.ipynb` |
| [`session-06_react_agent.py`](session-06_react_agent.py) | A ReAct agent loop (Reason + Act) with tools, built from scratch. | `python session-06_react_agent.py` |
| [`session-06_workflow_graph.py`](session-06_workflow_graph.py) | A LangGraph-style agent workflow: nodes, shared state and conditional edges. | `python session-06_workflow_graph.py` |
| [`session-06_multi_agent_crew.py`](session-06_multi_agent_crew.py) | A CrewAI/AutoGen-style multi-agent team: researcher, writer and reviewer. | `python session-06_multi_agent_crew.py` |
| [`session-06_project_expense_agent.py`](session-06_project_expense_agent.py) | Mini project (full solution) — An expense-claim agent with tools, memory, guardrails and a human in the loop. | `python session-06_project_expense_agent.py` |
| [`session-06_expense_decisions.png`](session-06_expense_decisions.png) | Claims and amounts by agent decision | created by `python session-06_project_expense_agent.py` |

### [Session 7 · Building AI-Powered Apps: Local LLMs, Summariser, Chatbot and RAG](../session-07-building-ai-powered-applications.md)

| File | What it does | How to run |
|---|---|---|
| [`session-07-building-ai-powered-applications.ipynb`](session-07-building-ai-powered-applications.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-07-building-ai-powered-applications.ipynb` |
| [`session-07_local_llm_client.py`](session-07_local_llm_client.py) | Talking to a local LLM through Ollama's REST API, and sizing models for your laptop. | `python session-07_local_llm_client.py` |
| [`session-07_summarizer.py`](session-07_summarizer.py) | A text summariser: offline extractive engine + LLM (DeepSeek-R1 / Qwen) prompt via Ollama. | `python session-07_summarizer.py` |
| [`session-07_rag_search.py`](session-07_rag_search.py) | Retrieval-Augmented Generation (RAG): retrieve, then build a grounded prompt. | `python session-07_rag_search.py` |
| [`session-07_project_chatbot.py`](session-07_project_chatbot.py) | Mini project (full solution) — "CampusBot": a RAG chatbot on Qwen 2.5 via Ollama, with an offline fallback. | `python session-07_project_chatbot.py` |
| [`session-07_rag_scores.png`](session-07_rag_scores.png) | Retrieval similarity scores for three questions | created by `python session-07_rag_search.py` |

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer</sub>
