from typing import Any, cast

import pytest
from src.features.ingestion import agents
from src.features.ingestion.agents.diacritize import diacritize
from src.features.ingestion.schema import DiacritizationResult
from src.shared.config.settings import Settings
from src.shared.errors.exceptions import UpstreamError
from src.shared.queue.context import WorkerContext

_SOURCE = "اللهم اغفر لي وارحمني"
_VOCALIZED = "اللَّهُمَّ اغْفِرْ لِي وَارْحَمْنِي"


def _context() -> WorkerContext:
    settings = Settings(ai_model="test-model", diacritization_verify_enabled=False)
    return WorkerContext(
        settings=settings,
        pocketbase=cast(Any, None),
        ai=cast(Any, None),
        http=cast(Any, None),
    )


@pytest.mark.asyncio
async def test_diacritize_falls_back_to_plain_when_ai_errors(monkeypatch: Any) -> None:
    async def boom(*args: Any, **kwargs: Any) -> DiacritizationResult:
        raise UpstreamError("ai_structured_output_failed:DiacritizationResult")

    monkeypatch.setattr(agents.diacritize, "complete_json", boom)

    result = await diacritize(_context(), _SOURCE)

    assert result == _SOURCE


@pytest.mark.asyncio
async def test_diacritize_returns_harakat_when_ai_succeeds(monkeypatch: Any) -> None:
    async def ok(*args: Any, **kwargs: Any) -> DiacritizationResult:
        return DiacritizationResult(diacritized_text=_VOCALIZED)

    monkeypatch.setattr(agents.diacritize, "complete_json", ok)

    result = await diacritize(_context(), _SOURCE)

    assert result == _VOCALIZED


@pytest.mark.asyncio
async def test_diacritize_rejects_word_altering_output(monkeypatch: Any) -> None:
    async def altered(*args: Any, **kwargs: Any) -> DiacritizationResult:
        return DiacritizationResult(diacritized_text="اللهم اغفر لي فقط")

    monkeypatch.setattr(agents.diacritize, "complete_json", altered)

    result = await diacritize(_context(), _SOURCE)

    assert result == _SOURCE
