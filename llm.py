"""Creates the Groq LLM shared by all agents."""
from crewai import LLM


def get_llm(model_id: str, api_key: str) -> LLM:
    return LLM(model=model_id, api_key=api_key, temperature=0.3, max_tokens=4000)
