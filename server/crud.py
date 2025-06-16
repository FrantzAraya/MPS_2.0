"""Funciones CRUD de utilidad."""

from __future__ import annotations

from typing import Iterable, Type, TypeVar

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T", bound=SQLModel)


async def crear(session: AsyncSession, modelo: T) -> T:
    session.add(modelo)
    await session.commit()
    await session.refresh(modelo)
    return modelo


async def obtener(session: AsyncSession, modelo: Type[T], objeto_id: int) -> T | None:
    return await session.get(modelo, objeto_id)


async def listar(session: AsyncSession, modelo: Type[T]) -> Iterable[T]:
    resultado = await session.exec(select(modelo))
    return resultado.all()


async def actualizar(session: AsyncSession, modelo: T) -> T:
    session.add(modelo)
    await session.commit()
    await session.refresh(modelo)
    return modelo


async def borrar(session: AsyncSession, modelo: Type[T], objeto_id: int) -> None:
    obj = await session.get(modelo, objeto_id)
    if obj:
        await session.delete(obj)
        await session.commit()
