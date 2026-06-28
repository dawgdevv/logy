from packages.ai.client import complete

GRAMMAR_SYSTEM = """You are a writing assistant. Fix grammar and clarity in the user's text.
Rules:
- Preserve the original meaning and tone.
- Fix spelling, grammar, and punctuation.
- Improve clarity without changing the message.
- Return ONLY the corrected text, no explanations."""


async def correct_grammar(text: str) -> str:
    """Return a grammar-corrected version of the input text."""
    messages = [
        {"role": "system", "content": GRAMMAR_SYSTEM},
        {"role": "user", "content": text},
    ]
    return await complete(messages)
