"""Creates the Groq LLM shared by all agents."""
from crewai import LLM


def get_llm(model_id: str, api_key: str) -> LLM:
    return LLM(
        model=model_id,
        api_key=api_key,
        temperature=0.3,
        max_tokens=2000,   # smaller reply budget = fewer tokens per request
        num_retries=5,     # auto-retry when Groq says "rate limit"
    )
