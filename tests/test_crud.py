import pytest
import pytest_asyncio
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from server import crud, models
from server.database import obtener_engine


@pytest_asyncio.fixture()
async def session():
    engine = obtener_engine(echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_crear_listar(session):
    producto = await crud.crear(session, models.Producto(nombre="Café", unidad="kg"))
    productos = await crud.listar(session, models.Producto)
    assert producto in productos
