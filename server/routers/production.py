"""Rutas para producción."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import crud, models
from ..database import get_session

router = APIRouter(prefix="/produccion", tags=["Producción"])


@router.post("/", response_model=models.LoteProduccion)
async def crear_lote(
    lote: models.LoteProduccion, session: AsyncSession = Depends(get_session)
):
    return await crud.crear(session, lote)


@router.get("/", response_model=list[models.LoteProduccion])
async def listar_lotes(session: AsyncSession = Depends(get_session)):
    return await crud.listar(session, models.LoteProduccion)
