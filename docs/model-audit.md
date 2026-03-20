# Model Audit

pyntrace can scan saved ML model files for security vulnerabilities — malicious pickle payloads, embedded secrets, unsafe deserialization patterns, and format anomalies — before you load them into memory.

```python
from pyntrace import audit_model

report = audit_model("./models/classifier.pkl")
report.summary()        # coloured terminal output
print(report.safe)      # False if CRITICAL or HIGH findings
```

---

## Supported Formats

| Format | Extensions | What's checked |
|--------|-----------|----------------|
| **Pickle** | `.pkl`, `.pickle`, `.joblib` | Dangerous global references (`os.system`, `subprocess`, `eval`, `exec`, `ctypes`, etc.) |
| **PyTorch** | `.pt`, `.pth`, `.bin` | ZIP-embedded pickle payloads, malicious checkpoint data |
| **safetensors** | `.safetensors` | Header size anomalies, suspicious metadata keys, invalid JSON |
| **HDF5 / Keras** | `.h5`, `.hdf5`, `.keras` | Lambda layers, embedded pickle markers |
| **ONNX** | `.onnx` | Custom Python ops (`PythonOp`) that execute arbitrary code |
| **NumPy** | `.npy`, `.npz` | Object-dtype arrays (require `allow_pickle=True`) |
| **Joblib** | `.joblib` | Same as pickle — joblib is pickle under the hood |

---

## Severity Levels

| Level | Meaning | Example |
|-------|---------|---------|
| `CRITICAL` | Confirmed code execution vector | `os.system` in pickle stream |
| `HIGH` | Very likely dangerous | Lambda layer in Keras model |
| `MEDIUM` | Potentially unsafe | PyTorch checkpoint contains pickle |
| `LOW` | Informational risk | Plain pickle without dangerous globals |
| `INFO` | Clean — no issues found | Valid safetensors with normal metadata |

A report is considered **safe** only when it contains no `CRITICAL` or `HIGH` findings.

---

## Python API

### `audit_model(path)`

Scan a single model file:

```python
from pyntrace import audit_model, ModelAuditReport

report: ModelAuditReport = audit_model("./model.safetensors")

# Check safety
if not report.safe:
    print(f"Unsafe model: {len(report.findings)} finding(s)")
    for f in report.findings:
        print(f"  [{f.severity}] {f.rule_id}: {f.title}")

# Export to JSON
data = report.to_json()

# Export SARIF (for GitHub Advanced Security / IDE integration)
report.save_sarif("./model-scan.sarif")
```

### `audit_models(directory, recursive=True)`

Scan an entire directory:

```python
from pyntrace import audit_models

reports = audit_models("./checkpoints/", recursive=True)
unsafe = [r for r in reports if not r.safe]
print(f"{len(unsafe)} of {len(reports)} models are unsafe")
```

### `ModelAuditReport` fields

| Field | Type | Description |
|-------|------|-------------|
| `path` | `str` | Absolute path to the scanned file |
| `format` | `str` | Detected format: `pickle`, `pytorch`, `safetensors`, etc. |
| `file_size_bytes` | `int` | File size |
| `sha256` | `str` | SHA-256 hex digest of the file |
| `findings` | `list[ModelFinding]` | All findings, sorted by severity |
| `safe` | `bool` | `True` if no CRITICAL or HIGH findings |
| `scan_duration_s` | `float` | Scan time in seconds |
| `scanned_at` | `str` | ISO 8601 timestamp |

### `ModelFinding` fields

| Field | Type | Description |
|-------|------|-------------|
| `severity` | `str` | `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` / `INFO` |
| `rule_id` | `str` | Rule identifier (e.g. `PICKLE001`, `ST004`) |
| `title` | `str` | Short human-readable title |
| `description` | `str` | Full explanation |
| `file_path` | `str` | File where the finding was detected |
| `offset` | `int` | Byte offset in the file (if applicable) |
| `evidence` | `str` | Raw matched bytes or pattern |

---

## CLI

```bash
# Scan a single file
pyntrace audit-model ./model.pkl

# Scan a directory recursively
pyntrace audit-model ./checkpoints/

# JSON output
pyntrace audit-model ./model.pkl --format json

# SARIF output (GitHub Advanced Security)
pyntrace audit-model ./model.pkl --sarif report.sarif

# Exit with non-zero code if CRITICAL findings found (useful in CI)
pyntrace audit-model ./model.pkl --fail-on-critical

# Non-recursive directory scan
pyntrace audit-model ./checkpoints/ --no-recursive
```

---

## CI Integration

Add a model audit step to your GitHub Actions workflow:

```yaml
- name: Audit ML models
  run: |
    pip install pyntrace
    pyntrace audit-model ./models/ --fail-on-critical --format json --output model-audit.json

- name: Upload model audit report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: model-audit
    path: model-audit.json
```

Or with SARIF upload for GitHub Advanced Security:

```yaml
- name: Audit ML models (SARIF)
  run: pyntrace audit-model ./models/ --sarif model-audit.sarif

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: model-audit.sarif
```

---

## Secret Detection

pyntrace also scans model weight files for accidentally embedded secrets. The following patterns are detected:

| Rule | Pattern | Severity |
|------|---------|---------|
| `SEC001` | OpenAI API key (`sk-...`) | HIGH |
| `SEC002` | Anthropic key (`sk-ant-...`) | HIGH |
| `SEC003` | AWS access key (`AKIA...`) | HIGH |
| `SEC004` | PEM private key header | CRITICAL |
| `SEC005` | GitHub token (`ghp_...`) | HIGH |
| `SEC006`–`SEC015` | Generic tokens, passwords, bearer headers, etc. | MEDIUM–HIGH |

This catches cases where training data, config dicts, or environment state was accidentally serialized into model checkpoints.
