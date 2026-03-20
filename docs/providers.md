# Provider Reference

pyntrace supports 9 LLM providers out of the box. All providers share the same `call()` interface — just change the model string prefix.

```python
from pyntrace.providers import call

# OpenAI
response = call("gpt-4o", [{"role": "user", "content": "Hello"}])

# Azure OpenAI
response = call("azure:gpt-4o", [{"role": "user", "content": "Hello"}])

# AWS Bedrock
response = call("bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0", [...])

# Groq
response = call("groq:llama-3.1-70b-versatile", [...])
```

---

## Provider Quick Reference

| Provider | Prefix | Install extra | Required env vars |
|----------|--------|---------------|-------------------|
| OpenAI | `gpt-*` / no prefix | `pyntrace[providers]` | `OPENAI_API_KEY` |
| Anthropic | `claude-*` | `pyntrace[providers]` | `ANTHROPIC_API_KEY` |
| Google (Gemini) | `gemini-*` | `pyntrace[providers]` | `GOOGLE_API_KEY` |
| Ollama (local) | `ollama:` or configured | — (zero deps) | — |
| **Azure OpenAI** | `azure:` | `pyntrace[azure]` | `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY` |
| **AWS Bedrock** | `bedrock:` | `pyntrace[bedrock]` | AWS credentials (any method) |
| **Groq** | `groq:` | `pyntrace[groq]` | `GROQ_API_KEY` |
| **Mistral** | `mistral:` | `pyntrace[mistral]` | `MISTRAL_API_KEY` |
| **Cohere** | `cohere:` | `pyntrace[cohere]` | `COHERE_API_KEY` |
| **Together AI** | `together:` | `pyntrace[together]` | `TOGETHER_API_KEY` |

Bold = added in v0.6.0.

---

## OpenAI

```bash
export OPENAI_API_KEY=sk-...
pip install pyntrace[providers]
```

```python
call("gpt-4o", messages)
call("gpt-4o-mini", messages)
call("o1-preview", messages)
```

---

## Anthropic Claude

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

```python
call("claude-3-5-sonnet-20241022", messages)
call("claude-3-haiku-20240307", messages)
```

---

## Google Gemini

```bash
export GOOGLE_API_KEY=AIza...
```

```python
call("gemini-1.5-pro", messages)
call("gemini-1.5-flash", messages)
```

---

## Azure OpenAI

```bash
pip install pyntrace[azure]
export AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com/
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_API_VERSION=2024-10-21  # optional, defaults to latest
```

```python
call("azure:gpt-4o", messages)              # uses gpt-4o deployment
call("azure:my-custom-deployment", messages) # custom deployment name
```

---

## AWS Bedrock

```bash
pip install pyntrace[bedrock]
# Configure AWS credentials via any standard method:
# - AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY + AWS_DEFAULT_REGION
# - IAM role (EC2/Lambda/ECS)
# - AWS CLI profile
```

```python
# Anthropic Claude on Bedrock
call("bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0", messages)
call("bedrock:anthropic.claude-3-haiku-20240307-v1:0", messages)

# Amazon Titan
call("bedrock:amazon.titan-text-express-v1", messages)

# Meta Llama
call("bedrock:meta.llama3-70b-instruct-v1:0", messages)
```

pyntrace auto-selects the correct Bedrock request format based on model family (Anthropic Messages API, Llama prompt format, or Converse API for others).

---

## Groq

```bash
pip install pyntrace[groq]
export GROQ_API_KEY=gsk_...
```

```python
call("groq:llama-3.1-70b-versatile", messages)
call("groq:llama-3.1-8b-instant", messages)
call("groq:mixtral-8x7b-32768", messages)
call("groq:gemma2-9b-it", messages)
```

---

## Mistral

```bash
pip install pyntrace[mistral]
export MISTRAL_API_KEY=...
```

```python
call("mistral:mistral-large-latest", messages)
call("mistral:mistral-small-latest", messages)
call("mistral:codestral-latest", messages)
```

---

## Cohere

```bash
pip install pyntrace[cohere]
export COHERE_API_KEY=...
```

```python
call("cohere:command-r-plus", messages)
call("cohere:command-r", messages)
call("cohere:command", messages)
```

---

## Together AI

```bash
pip install pyntrace[together]
export TOGETHER_API_KEY=...
```

```python
call("together:meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", messages)
call("together:mistralai/Mixtral-8x7B-Instruct-v0.1", messages)
call("together:Qwen/Qwen2-72B-Instruct", messages)
```

---

## Ollama (Local)

No API key needed. Requires [Ollama](https://ollama.com) running locally.

```python
pyntrace.init(offline=True, local_judge_model="llama3")

call("ollama:llama3", messages)
call("llama3", messages)  # also works
```

---

## Install All Providers

```bash
pip install "pyntrace[providers]"   # OpenAI, Anthropic, Google, Mistral, Cohere, Bedrock
pip install "pyntrace[azure]"       # + Azure OpenAI
pip install "pyntrace[groq]"        # + Groq
pip install "pyntrace[together]"    # + Together AI
pip install "pyntrace[full]"        # everything
```

---

## Retry Behaviour

All providers use automatic exponential backoff:

- **Retries on**: HTTP 429 (rate limit), HTTP 5xx (server errors), network timeouts
- **Default**: 3 retries, 1s base delay, up to 10s max delay
- **Override**:

```python
from pyntrace import providers
providers._MAX_RETRIES = 5
providers._RETRY_BASE_DELAY_S = 2.0
providers._RETRY_MAX_DELAY_S = 30.0
```

---

## Using Providers in Red Team Scans

```python
report = pyntrace.red_team(
    my_fn,
    plugins=["jailbreak"],
    judge_model="groq:llama-3.1-70b-versatile",   # fast + cheap judge
    n_attacks=20,
)
```

---

## Multi-Provider Fingerprinting

```python
fp = pyntrace.fingerprint({
    "gpt-4o":             gpt4o_fn,
    "claude-3-5-sonnet":  claude_fn,
    "groq:llama-3.1-70b": groq_fn,
    "mistral:large":      mistral_fn,
})
fp.heatmap()
```
