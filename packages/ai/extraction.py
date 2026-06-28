import json

from packages.ai.client import complete

EXTRACT_SYSTEM = """You are an entity and technology extractor.
Given a daily work entry, extract:
- people: list of people mentioned
- technologies: list of technologies, tools, languages, frameworks used
- entities: list of important entities (projects, services, systems)

Return ONLY valid JSON with keys "people", "technologies", "entities",
each mapping to a list of strings.
If none found, return empty lists."""


async def extract_entities(text: str) -> dict[str, list[str]]:
    """Extract people, technologies, and entities from text."""
    messages = [
        {"role": "system", "content": EXTRACT_SYSTEM},
        {"role": "user", "content": text},
    ]
    raw = await complete(messages)
    try:
        data = json.loads(raw)
        return {
            "people": data.get("people", []),
            "technologies": data.get("technologies", []),
            "entities": data.get("entities", []),
        }
    except (json.JSONDecodeError, AttributeError):
        return {"people": [], "technologies": [], "entities": []}


SUMMARY_SYSTEM = """You are a concise summarizer. Summarize the user's work entry in one sentence.
Rules:
- Be concise and factual.
- Capture the main action and outcome.
- Return ONLY the summary text."""


async def summarize(text: str) -> str:
    """Generate a one-sentence summary of the entry."""
    messages = [
        {"role": "system", "content": SUMMARY_SYSTEM},
        {"role": "user", "content": text},
    ]
    return await complete(messages)
