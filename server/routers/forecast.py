"""Rutas para pronósticos."""

from __future__ import annotations


from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import crud, models
from ..database import get_session
from ..forecasting.prophet_service import generar_pronostico

router = APIRouter(prefix="/pronosticos", tags=["Pronósticos"])


@router.post("/{producto_id}", response_model=list[models.Pronostico])
async def ejecutar_pronostico(
    producto_id: int, session: AsyncSession = Depends(get_session)
):
    return await generar_pronostico(session, producto_id)


@router.get("/", response_model=list[models.Pronostico])
async def listar(session: AsyncSession = Depends(get_session)):
    return await crud.listar(session, models.Pronostico)
