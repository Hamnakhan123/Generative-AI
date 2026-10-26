"""
Session 7 · Example 1 — Talking to a local LLM through Ollama's REST API, and sizing models for your laptop.

Ollama serves open models (Qwen 2.5, Llama 3, Mistral, DeepSeek-R1) at localhost:11434.
We size models for your RAM, build the /api/chat body and call it if Ollama is running.

Setup (your own machine):  install Ollama from ollama.com, then
    ollama pull qwen2.5:7b      # or qwen2.5:1.5b on a small laptop
Run:  python session-07_local_llm_client.py
"""
import json
import urllib.request

OLLAMA = "http://localhost:11434"

# 1) Memory estimate: parameters x bytes per weight x ~1.2 overhead (KV cache, runtime)
MODELS = {"qwen2.5:1.5b": 1.5, "mistral:7b": 7.2, "qwen2.5:7b": 7.6, "llama3:8b": 8.0,
          "qwen2.5:14b": 14.7, "qwen2.5:72b": 72.7}
BITS = {"FP16": 16, "Q8": 8, "Q4": 4.5}       # Q4 formats store ~4.5 bits/weight incl. scales
print(f"{'model':14s} {'params':>7s}  " + "  ".join(f"{k:>6s}" for k in BITS) + "   (GB of RAM/VRAM)")
for name, b in MODELS.items():
    gbs = [b * 1e9 * bits / 8 * 1.2 / 1e9 for bits in BITS.values()]
    print(f"{name:14s} {b:6.1f}B  " + "  ".join(f"{g:6.1f}" for g in gbs))

# 2) The request body for a chat call
body = {
    "model": "qwen2.5:7b",
    "messages": [
        {"role": "system", "content": "You are a concise teaching assistant. Answer in 2 sentences."},
        {"role": "user", "content": "What does a transformer's attention layer do?"},
    ],
    "stream": False,
    "options": {"temperature": 0.2, "num_ctx": 4096},
}
print("\nPOST /api/chat body:\n{\n" + ",\n".join(f'  "{k}": {json.dumps(v)}' for k, v in body.items()) + "\n}")


def chat(payload, timeout=60):
    req = urllib.request.Request(OLLAMA + "/api/chat", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())["message"]["content"]


def ollama_running():
    try:
        urllib.request.urlopen(OLLAMA + "/api/tags", timeout=1)
        return True
    except Exception:
        return False

# 3) Call it if available
if ollama_running():
    print("\nModel reply:\n" + chat(body))
else:
    print("\nOllama is not running on this machine, so no reply was generated.")
    print("Start it with:  ollama serve   then   ollama pull qwen2.5:7b   and run this script again.")
