"""Cálculo simplificado de MRP."""

from __future__ import annotations

from datetime import date

from sqlmodel.ext.asyncio.session import AsyncSession

from . import crud, models


async def generar_mrp(session: AsyncSession, material_id: int, semanas: int = 12):
    lineas: list[models.LineaMRP] = []
    for i in range(semanas):
        linea = models.LineaMRP(
            material_id=material_id,
            periodo=date.today(),
            requerimiento_bruto=0,
            recibo_programado=0,
            orden_planificada=0,
        )
        lineas.append(linea)
        await crud.crear(session, linea)
    return lineas
