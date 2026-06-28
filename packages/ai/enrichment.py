import asyncio

from pydantic import BaseModel

from packages.ai.extraction import extract_entities, summarize
from packages.ai.grammar import correct_grammar


class EnrichedEntry(BaseModel):
    corrected_content: str
    summary: str
    people: list[str]
    technologies: list[str]
    entities: list[str]


async def enrich_entry(content: str) -> EnrichedEntry:
    """Run the full enrichment pipeline on an entry.

    Pipeline:
    1. Grammar correction
    2. Entity / technology extraction
    3. Summary generation
    """
    corrected = await correct_grammar(content)

    extracted, summary = await asyncio.gather(
        extract_entities(corrected),
        summarize(corrected),
    )

    return EnrichedEntry(
        corrected_content=corrected,
        summary=summary,
        people=extracted["people"],
        technologies=extracted["technologies"],
        entities=extracted["entities"],
    )
