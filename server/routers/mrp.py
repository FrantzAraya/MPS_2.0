"""Rutas para MRP."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import crud, models
from ..database import get_session

router = APIRouter(prefix="/mrp", tags=["MRP"])


@router.get("/", response_model=list[models.LineaMRP])
async def listar_mrp(session: AsyncSession = Depends(get_session)):
    return await crud.listar(session, models.LineaMRP)
