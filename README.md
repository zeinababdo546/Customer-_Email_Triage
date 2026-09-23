# Prompt-Powered Microservice: Customer Email Triage

A lightweight Python microservice that ingests unorganized customer emails and extracts clean, validated JSON using Structured Outputs and Pydantic schemas.

## Key Features
- **Deterministic Schema Enforcement:** Guarantees LLM output strictly matches specified types and Enum values.
- **Zero Hallucination Routing:** Eliminates malformed JSON responses or extra conversational text.
- **Robust Field Validation:** Powered by `Pydantic` to guard down-stream backend logic against bad data.
- **Comprehensive Unit Testing:** Includes 5 isolated test cases covering all triage edge scenarios using Pytest mocks.

## Why Pydantic Validation Matters (Anti-Hallucination Layer)
LLMs in raw text mode suffer from unpredictability: missing fields, altered JSON keys, or conversational bloat (e.g., `"Here is your JSON:"`).

By combining **Structured Outputs API** with **Pydantic Validation**:
1. **Type Safety:** Ensures `urgency` is strictly restricted to valid Enum choices (`Critical`, `High`, `Medium`, `Low`).
2. **Crash Prevention:** Missing required attributes trigger deterministic exceptions before invalid data enters core backend systems.
3. **Production Readiness:** Translates loose natural language into reliable API contract data.

## Getting Started

### 1. Prerequisites & Installation
Clone the repository and install dependencies using Python virtual environment:

```bash
python -m venv microservice
source microservice/Scripts/activate  # On Windows (Git Bash)
pip install -r requirements.txt

```

### 2. Configure Environment Variable

Set your OpenRouter or OpenAI API Key in your terminal session:

```bash
export OPENROUTER_API_KEY="your-api-key-here"

```

### 3. Execution & Testing

* **Run the Microservice:**
```bash
python main.py

```
<img width="936" height="267" alt="image" src="https://github.com/user-attachments/assets/8dcc27e7-88d4-4891-8799-f670e6afe106" />



* **Run Unit Test Suite (100% Offline & Free via Mocks):**
```bash
pytest test_main.py

```

<img width="968" height="267" alt="WhatsApp Image 2026-09-23 at 6 13 50 PM" src="https://github.com/user-attachments/assets/2039a714-1d6e-4f1e-9bfa-52294c6975d5" />

## Test Results

All 5 unit test cases pass deterministically in under 3 seconds:

* `Test 1:` High-urgency billing dispute extraction.
* `Test 2:` Technical account issue handling.
* `Test 3:` General feedback / positive review filtering.
* `Test 4:` Critical security threat routing.
* `Test 5:` Empty prompt error validation (`ValueError`).

