# Changelog

All notable changes to pyntrace are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.6.0] — 2026-03-20

### Added

#### Security — Model Audit
- `pyntrace.guard.model_audit`: New ML model file scanner (`audit_model()`, `audit_models()`)
- Detects malicious pickle payloads, unsafe deserialization, embedded secrets, and format anomalies
- Supports 7 formats: pickle, PyTorch checkpoint, HDF5/Keras, ONNX, safetensors, NumPy, joblib
- SARIF export (`report.save_sarif()`), JSON export (`report.to_json()`), coloured terminal summary
- 15 secret patterns detected inside model weights (API keys, private keys, AWS tokens, etc.)
- CLI: `pyntrace audit-model ./model.pkl` with `--format`, `--output`, `--sarif`, `--fail-on-critical`

#### Security — Custom Attack Plugins
- `@pyntrace.attack_plugin("name")` decorator to register custom attack generators
- `register_plugin(name, fn)` programmatic API
- Auto-discovery from `~/.pyntrace/plugins/*.py` files
- Entry-point discovery via `pyntrace.attack_plugins` group in `pyproject.toml`
- `load_all_plugins()` to activate all external plugins at once

#### Security — Threat Intelligence Feed
- `pyntrace.guard.threats`: OWASP LLM Top 10 (LLM01–LLM10) + pyntrace extras (PYN01–PYN04) catalog
- `GET /api/threats/feed?limit=N` — sorted by severity
- `POST /api/threats/test` — queue a targeted red-team scan against a specific threat
- `/api/v1/threats/feed` — available under versioned prefix too

#### Providers — 6 New LLM Backends
- **Azure OpenAI**: `azure:gpt-4o`, `azure:gpt-4o-mini` — requires `AZURE_OPENAI_ENDPOINT` + `AZURE_OPENAI_API_KEY`
- **AWS Bedrock**: `bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0` — requires boto3 + AWS credentials
- **Groq**: `groq:llama-3.1-70b-versatile` — requires `GROQ_API_KEY`
- **Mistral**: `mistral:mistral-large-latest` — requires `MISTRAL_API_KEY`
- **Cohere**: `cohere:command-r-plus` — requires `COHERE_API_KEY`
- **Together AI**: `together:meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo` — requires `TOGETHER_API_KEY`
- Install extras: `pip install pyntrace[azure]`, `pyntrace[bedrock]`, `pyntrace[groq]`, `pyntrace[mistral]`, `pyntrace[cohere]`, `pyntrace[together]`
- `_with_retry()`: automatic exponential backoff on HTTP 429 / 5xx / network errors

#### Server
- `GET /health` — `{"status":"ok","version":"0.6.0","db":"ok"}` for load balancer checks
- `?page=&size=` pagination on all list endpoints (security reports, traces, MCP scans, etc.)
- `?model=&from_ts=&to_ts=` time/model filtering on security and monitor endpoints
- `/api/v1/` versioned router — all `/api/` routes mirrored under `/api/v1/` (backward compatible)
- WebSocket `/ws` now validates `PYNTRACE_API_KEY` token query param when auth is enabled

#### Infrastructure
- `Dockerfile`: multi-stage build, non-root user `pyntrace`, `VOLUME /data`, `HEALTHCHECK`
- `docker-compose.yml`: one-command self-hosted deploy
- DB migration system: `PRAGMA user_version`-based migration runner, 5 initial migrations
- `PRAGMA foreign_keys=ON` enforced on every connection
- 28 SQLite performance indexes across all frequently-queried columns

#### Developer Experience
- `.pre-commit-config.yaml`: ruff + bandit hooks
- `.github/workflows/security.yml`: Bandit SAST + pip-audit CVE scan + Ruff S-series CI
- `[dev]` extra in `pyproject.toml`: `pip install pyntrace[dev]`
- PII detector expanded from 5 → 18 patterns (AWS keys, GH tokens, IBAN, MAC, IPv6, etc.)

### Changed
- `pyproject.toml`: Development status `3 - Alpha` → `4 - Beta`
- Provider `call()` now retries automatically — `call_llm` alias preserved for backward compat

---

## [0.5.1] — 2026-01-15

### Added
- MCP tool risk scoring (`analyze_mcp_tools`, `ToolRiskReport`)
- Conversation scan (`scan_conversation`, `ConversationScanReport`)
- 9-tab dashboard with demo video embed
- Scan comparison modal (side-by-side diff of up to 4 scans)

---

## [0.5.0] — 2025-12-01

### Added
- OAuth 2.0 login (GitHub, Google) for dashboard
- Audit log for all API actions
- Compliance report generator (OWASP LLM Top 10, NIST AI RMF, EU AI Act)
- Review & annotation UI for red team results

---

## [0.4.0] — 2025-10-15

### Added
- Cross-language jailbreak scanner (`scan_multilingual`)
- System prompt leakage scoring (`prompt_leakage_score`)
- MCP server scanner (`scan_mcp`)
- Prometheus metrics exporter

---

## [0.3.0] — 2025-09-01

### Added
- Multi-agent swarm exploitation (`scan_swarm`)
- Toolchain privilege escalation scanner (`scan_toolchain`)
- Latency profiling with p50/p95/p99 (`benchmark_latency`)

---

## [0.2.0] — 2025-07-15

### Added
- Attack heatmap / model fingerprinting (`fingerprint`, `ModelFingerprint`)
- Auto test-case generation (`auto_dataset`)
- Drift detection (`DriftDetector`, `DriftReport`)
- Git-aware regression tracking

---

## [0.1.0] — 2025-06-01

### Added
- Initial release: `red_team()`, `Dataset`, `Experiment`, `trace()`/`span()`
- SQLite persistence, FastAPI dashboard
- OpenAI, Anthropic, Google, Ollama providers
- SARIF + JUnit export
