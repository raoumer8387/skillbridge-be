from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


def get_llm(temperature: float) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=temperature,
    )
