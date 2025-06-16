"""Rutas para inventario."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import crud, models
from ..database import get_session

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.post("/", response_model=models.Inventario)
async def crear_inventario(
    inventario: models.Inventario, session: AsyncSession = Depends(get_session)
):
    return await crud.crear(session, inventario)


@router.get("/", response_model=list[models.Inventario])
async def listar_inventario(session: AsyncSession = Depends(get_session)):
    return await crud.listar(session, models.Inventario)
