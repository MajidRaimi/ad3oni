from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.shared.errors.exceptions import AppError
from src.shared.logging.setup import get_logger

logger = get_logger("api.errors")


def _error_body(code: str, message: str) -> dict[str, dict[str, str]]:
    return {"error": {"code": code, "message": message}}


async def _handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    if exc.status_code >= 500:
        logger.error("app_error path=%s code=%s", request.url.path, exc.code)
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(exc.code, exc.message),
    )


async def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_error path=%s", request.url.path)
    return JSONResponse(
        status_code=500,
        content=_error_body("internal_error", "An unexpected error occurred."),
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _handle_app_error)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, _handle_unexpected_error)
