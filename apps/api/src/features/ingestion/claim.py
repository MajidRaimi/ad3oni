from typing import Any

from src.shared.pocketbase.filters import quote
from src.shared.queue.context import WorkerContext

PENDING = "pending"
PROCESSING = "processing"
_CLAIMABLE = {PENDING, PROCESSING}


async def claim_prayer(context: WorkerContext, prayer_id: str) -> dict[str, Any] | None:
    record = await context.pocketbase.get_first("prayers", f"id = {quote(prayer_id)}")
    if record is None or record.get("status") not in _CLAIMABLE:
        return None
    if record.get("status") == PROCESSING:
        return record
    return await context.pocketbase.update_record("prayers", prayer_id, {"status": PROCESSING})
