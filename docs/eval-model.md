# `eval_model` Fixture

Session-scoped pytest fixture defined in `conftest.py`. Constructs the DeepEval LLM judge once per session and shares it across all 20 parametrized test items.

---

## Construction Flow

```mermaid
flowchart TD
    A([session start]) --> B[eval_model fixture]
    B --> C["os.getenv('EVAL_MODEL_PROVIDER', 'anthropic')"]

    C --> D{provider?}

    D -- anthropic\ndefault --> E["return None\nDeepEval reads\nANTHROPIC_API_KEY automatically"]

    D -- bedrock --> F["AmazonBedrockModel\nmodel = AWS_BEDROCK_MODEL_ID\nregion = AWS_REGION"]

    D -- gemini --> G["GeminiModel\nmodel = GEMINI_MODEL_ID\napi_key = GOOGLE_API_KEY"]

    E & F & G --> H([eval_model injected\ninto all 20 tests])
```

---

## Provider Reference

| `EVAL_MODEL_PROVIDER` | Wrapper returned | Required env vars |
|----------------------|-----------------|-------------------|
| `anthropic` (default) | `None` | `ANTHROPIC_API_KEY` |
| `bedrock` | `AmazonBedrockModel` | `AWS_BEDROCK_MODEL_ID`, `AWS_REGION` |
| `gemini` | `GeminiModel` | `GEMINI_MODEL_ID`, `GOOGLE_API_KEY` |

---

## Why a Fixture Instead of a Module-Level Constant?

```mermaid
flowchart LR
    subgraph BAD ["❌ Module-level constant"]
        direction TB
        B1["_EVAL_MODEL = _build_eval_model()\n(runs at import time)"]
        B2["conftest.py load_dotenv()\nhasn't fired yet"]
        B3["env vars missing\nor wrong values"]
        B1 --> B2 --> B3
    end

    subgraph GOOD ["✅ Session-scoped fixture"]
        direction TB
        G1["conftest.py load_dotenv()\nfires first"]
        G2["eval_model fixture\nruns after env is ready"]
        G3["correct provider\ncorrect credentials"]
        G1 --> G2 --> G3
    end
```

The fixture is lazy — it only runs when the first test requests it — and it participates in pytest's dependency injection, making it easy to override in tests with a different model.

---

## Related Files

| File | Role |
|------|------|
| `conftest.py` | `eval_model` fixture definition |
| `tests/test_smoke.py` | Consumes `eval_model` via parameter injection |
| `.env` | `EVAL_MODEL_PROVIDER` and model credentials |
