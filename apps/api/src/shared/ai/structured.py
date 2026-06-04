import json
from copy import deepcopy
from typing import Any

from openai import AsyncOpenAI, BadRequestError
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic import BaseModel, ValidationError

from src.shared.errors.exceptions import UpstreamError


def _to_strict_schema(node: Any) -> Any:
    if isinstance(node, dict):
        if node.get("type") == "object" and "properties" in node:
            node["additionalProperties"] = False
            node["required"] = list(node["properties"].keys())
        for value in node.values():
            _to_strict_schema(value)
    elif isinstance(node, list):
        for item in node:
            _to_strict_schema(item)
    return node


def _strict_schema_for(schema: type[BaseModel]) -> dict[str, Any]:
    schema_dict: dict[str, Any] = deepcopy(schema.model_json_schema())
    _to_strict_schema(schema_dict)
    return schema_dict


def _messages(system: str, user: str) -> list[ChatCompletionMessageParam]:
    return [
        ChatCompletionSystemMessageParam(role="system", content=system),
        ChatCompletionUserMessageParam(role="user", content=user),
    ]


async def _complete(
    client: AsyncOpenAI,
    model: str,
    system: str,
    user: str,
    body: dict[str, Any],
) -> str:
    response = await client.chat.completions.create(
        model=model,
        messages=_messages(system, user),
        extra_body=body,
    )
    content = response.choices[0].message.content
    if content is None:
        raise UpstreamError("ai_empty_response")
    return content


async def complete_json[T: BaseModel](
    client: AsyncOpenAI,
    model: str,
    system: str,
    user: str,
    schema: type[T],
    reasoning_effort: str = "medium",
    max_retries: int = 1,
) -> T:
    strict = _strict_schema_for(schema)
    schema_format = {
        "type": "json_schema",
        "json_schema": {"name": schema.__name__, "strict": True, "schema": strict},
    }
    try:
        content = await _complete(
            client,
            model,
            system,
            user,
            {"response_format": schema_format, "reasoning_effort": reasoning_effort},
        )
        return schema.model_validate_json(content)
    except (BadRequestError, ValidationError, UpstreamError):
        pass

    fallback_system = (
        f"{system}\n\nReturn ONLY a JSON object matching this schema:\n"
        f"{json.dumps(strict, ensure_ascii=False)}"
    )
    last_error: Exception | None = None
    for _ in range(max_retries):
        try:
            content = await _complete(
                client,
                model,
                fallback_system,
                user,
                {
                    "response_format": {"type": "json_object"},
                    "reasoning_effort": reasoning_effort,
                },
            )
            return schema.model_validate_json(content)
        except (BadRequestError, ValidationError, UpstreamError) as exc:
            last_error = exc

    raise UpstreamError(f"ai_structured_output_failed:{schema.__name__}") from last_error
