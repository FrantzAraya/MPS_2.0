import pytest
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from server import mrp
from server.database import obtener_engine


@pytest.mark.asyncio
async def test_generar_mrp():
    engine = obtener_engine(echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine) as session:
        lineas = await mrp.generar_mrp(session, material_id=1, semanas=2)
        assert len(lineas) == 2
