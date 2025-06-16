"""Módulo de base de datos."""

from __future__ import annotations

from pathlib import Path
from typing import AsyncGenerator

from pydantic import BaseSettings
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class Settings(BaseSettings):
    api_port: int = 8000
    debug: bool = False
    db_url: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def obtener_ruta_db() -> str:
    """Obtiene la ruta de la base de datos dependiendo del SO."""
    if settings.db_url:
        return settings.db_url
    home = Path.home()
    if Path.home().drive:
        base = Path.home() / "AppData" / "Roaming" / "CafeDeAltura"
    else:
        base = home / ".cafe_de_altura"
    base.mkdir(parents=True, exist_ok=True)
    return str(base / "mps.db")


def obtener_engine(echo: bool | None = None):
    url = f"sqlite+aiosqlite:///{obtener_ruta_db()}"
    engine = create_engine(
        url, echo=echo if echo is not None else settings.debug, future=True
    )
    return engine


async def crear_db_y_tablas() -> None:
    engine = obtener_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    engine = obtener_engine()
    async_session = AsyncSession(engine)
    async with async_session as session:
        yield session
