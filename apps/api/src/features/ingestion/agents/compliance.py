from src.features.ingestion.prompts import COMPLIANCE_SYSTEM, compliance_user
from src.features.ingestion.schema import ComplianceResult
from src.shared.ai.structured import complete_json
from src.shared.queue.context import WorkerContext


async def review_compliance(context: WorkerContext, text: str) -> ComplianceResult:
    return await complete_json(
        context.ai,
        context.settings.ai_model,
        COMPLIANCE_SYSTEM,
        compliance_user(text),
        ComplianceResult,
        reasoning_effort=context.settings.compliance_effort,
    )
