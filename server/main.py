"""Punto de entrada del servidor FastAPI."""

from __future__ import annotations

import threading

import uvicorn
from fastapi import FastAPI

from .database import crear_db_y_tablas
from .routers import inventory, production, sales, forecast, mrp
from .scheduler import iniciar_scheduler
from .database import settings

app = FastAPI(title="Café de Altura MPS")

app.include_router(inventory.router)
app.include_router(production.router)
app.include_router(sales.router)
app.include_router(forecast.router)
app.include_router(mrp.router)


@app.on_event("startup")
async def startup() -> None:
    await crear_db_y_tablas()
    iniciar_scheduler()


def iniciar_servidor_en_hilo() -> None:
    thread = threading.Thread(
        target=uvicorn.run,
        args=("server.main:app",),
        kwargs={"port": settings.api_port, "host": "127.0.0.1", "log_level": "info"},
        daemon=True,
    )
    thread.start()
