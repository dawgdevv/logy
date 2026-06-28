from litellm import acompletion

from packages.shared.config import settings


async def complete(
    messages: list[dict[str, str]],
    model: str | None = None,
    temperature: float = 0.3,
) -> str:
    """Send a completion request to the configured LLM via LiteLLM."""
    model = model or settings.litellm_model

    kwargs: dict = {"model": model, "messages": messages, "temperature": temperature}

    if settings.litellm_api_key:
        kwargs["api_key"] = settings.litellm_api_key
    if settings.litellm_api_base:
        kwargs["api_base"] = settings.litellm_api_base

    response = await acompletion(**kwargs)
    return response.choices[0].message.content or ""
