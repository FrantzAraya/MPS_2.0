import pandas as pd
import pytest
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from server import crud, models
from server.database import obtener_engine
from server.forecasting.prophet_service import generar_pronostico


@pytest.mark.asyncio
async def test_generar_pronostico():
    engine = obtener_engine(echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine) as session:
        await session.commit()
        venta = models.Venta(
            producto_id=1, fecha_venta=pd.Timestamp("2023-01-01"), unidades_vendidas=10
        )
        await crud.crear(session, venta)
        pronosticos = await generar_pronostico(session, 1)
        assert isinstance(pronosticos, list)
