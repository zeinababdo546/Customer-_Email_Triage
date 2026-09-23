import os
from openai import OpenAI
from schema import EmailAnalysis

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


def analyze_customer_email(raw_email: str) -> EmailAnalysis:
    if not raw_email or not raw_email.strip():
        raise ValueError("Input email text cannot be empty.")

    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    response = client.beta.chat.completions.parse(
        model="google/gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_email},
        ],
        response_format=EmailAnalysis,
        temperature=0.0,
        max_tokens=1000,  
    )

    parsed_result = response.choices[0].message.parsed
    if parsed_result is None:
        raise RuntimeError("Failed to parse structured output from LLM.")

    return parsed_result


if __name__ == "__main__":
    sample_email = (
        "Hi Team, I was charged $99 twice on my credit card this morning! "
        "Please refund the duplicate transaction immediately as this is very urgent."
    )
    result = analyze_customer_email(sample_email)
    print("--- Execution Test Output ---")
    print(result.model_dump_json(indent=2))