from fastapi import FastAPI

from src.features.health.router import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="Ad3oni API")
    app.include_router(health_router)
    return app


app = create_app()
