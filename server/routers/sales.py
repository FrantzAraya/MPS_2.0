"""Rutas para ventas."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import crud, models
from ..database import get_session

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.post("/", response_model=models.Venta)
async def crear_venta(
    venta: models.Venta, session: AsyncSession = Depends(get_session)
):
    return await crud.crear(session, venta)


@router.get("/", response_model=list[models.Venta])
async def listar_ventas(session: AsyncSession = Depends(get_session)):
    return await crud.listar(session, models.Venta)
