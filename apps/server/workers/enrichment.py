import asyncio
import logging
from typing import Any

from packages.ai.enrichment import EnrichedEntry, enrich_entry
from packages.database.repository import Repository
from packages.shared.config import settings

logger = logging.getLogger(__name__)

_enrichment_queue: asyncio.Queue[int] = asyncio.Queue()
_worker_task: asyncio.Task[Any] | None = None


async def enqueue_entry(entry_id: int) -> None:
    """Add an entry ID to the enrichment queue."""
    await _enrichment_queue.put(entry_id)
    logger.info("Entry %d queued for enrichment", entry_id)


async def _worker(repo: Repository) -> None:
    """Background worker that processes entries from the queue."""
    while True:
        entry_id = await _enrichment_queue.get()
        try:
            entry = repo.get_entry(entry_id)
            if not entry:
                logger.warning("Entry %d not found, skipping", entry_id)
                continue

            logger.info("Enriching entry %d", entry_id)
            enriched: EnrichedEntry = await enrich_entry(entry.content)

            repo.update_entry(
                entry_id=entry_id,
                content=enriched.corrected_content,
            )

            logger.info("Entry %d enriched successfully", entry_id)
        except Exception:
            logger.exception("Failed to enrich entry %d", entry_id)
        finally:
            _enrichment_queue.task_done()


def start_worker() -> None:
    """Start the background enrichment worker."""
    global _worker_task
    repo = Repository(settings.db_path)
    _worker_task = asyncio.create_task(_worker(repo))
    logger.info("Enrichment worker started")
