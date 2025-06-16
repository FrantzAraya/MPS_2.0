"""Servicio de pronóstico usando Prophet."""

from __future__ import annotations

from datetime import timedelta, date

from prophet import Prophet
from sqlmodel import select
import pandas as pd
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import crud, models


async def generar_pronostico(session: AsyncSession, producto_id: int):
    ventas = await session.exec(
        select(models.Venta).where(models.Venta.producto_id == producto_id)
    )
    rows = ventas.all()
    df = pd.DataFrame([row.model_dump() for row in rows])
    if df.empty:
        return []

    if len(df) < 2:
        ultima = df.iloc[-1]
        base_fecha = ultima["fecha_venta"]
        pronosticos = []
        for i in range(12):
            inicio = base_fecha + timedelta(weeks=i + 1)
            p = models.Pronostico(
                producto_id=producto_id,
                inicio_periodo=inicio if isinstance(inicio, date) else inicio.date(),
                fin_periodo=(inicio + timedelta(days=6)) if isinstance(inicio, date) else (inicio + timedelta(days=6)).date(),
                unidades_pronosticadas=int(ultima["unidades_vendidas"]),
            )
            pronosticos.append(p)
            await crud.crear(session, p)
        return pronosticos

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
