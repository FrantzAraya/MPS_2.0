"""Planificador de tareas semanales."""

from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import select

from .forecasting.prophet_service import generar_pronostico
from . import models
from .database import obtener_engine
from sqlmodel.ext.asyncio.session import AsyncSession


scheduler = BackgroundScheduler(timezone="UTC")


def iniciar_scheduler() -> None:
    scheduler.start()


async def tarea_semanal() -> None:
    """Ejecuta el pronóstico semanal para todos los productos."""
    engine = obtener_engine()
    async with AsyncSession(engine) as session:
        productos = await session.exec(select(models.Producto))
        for producto in productos:
            await generar_pronostico(session, producto.id)


scheduler.add_job(tarea_semanal, "cron", day_of_week="sun", hour=23, minute=55)
