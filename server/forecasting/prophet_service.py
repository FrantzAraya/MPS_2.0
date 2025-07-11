"""Servicio de pronóstico usando Prophet."""

from __future__ import annotations

from datetime import timedelta

from prophet import Prophet
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import crud, models


async def generar_pronostico(session: AsyncSession, producto_id: int):
    ventas = await session.exec(
        select(models.Venta).where(models.Venta.producto_id == producto_id)
    )
    df = ventas.to_pandas()
    if df.empty:
        return []
    df = df.rename(columns={"fecha_venta": "ds", "unidades_vendidas": "y"})
    modelo = Prophet(seasonality_mode="multiplicative", weekly_seasonality=3)
    modelo.fit(df)
    futuro = df[["ds"]].copy()
    max_fecha = futuro["ds"].max()
    for i in range(12):
        futuro.loc[len(futuro)] = max_fecha + timedelta(weeks=i + 1)
    forecast = modelo.predict(futuro)
    pronosticos = []
    for _, row in forecast.tail(12).iterrows():
        p = models.Pronostico(
            producto_id=producto_id,
            inicio_periodo=row["ds"].date(),
            fin_periodo=(row["ds"] + timedelta(days=6)).date(),
            unidades_pronosticadas=int(row["yhat"]),
        )
        pronosticos.append(p)
        await crud.crear(session, p)
    return pronosticos
