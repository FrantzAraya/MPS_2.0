"""Página de planificación.

Muestra las líneas de MRP obtenidas desde la API.
"""

from __future__ import annotations

import flet as ft

from ..services.api_client import APIClient
from ..components import button
from . import dashboard


async def vista(page: ft.Page) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Planificación"))

    api = APIClient()
    lista = ft.Column()

    async def cargar() -> None:
        registros = await api.get("/mrp/")
        lista.controls.clear()
        for r in registros:
            texto = (
                f"{r['id']} mat {r['material_id']} -> {r['orden_planificada']}"
            )
            lista.controls.append(ft.Text(texto))
        page.update()

    async def volver(e):  # noqa: ANN001
        await dashboard.vista(page)

    page.controls.clear()
    page.controls.append(ft.Column([button.boton("Volver", volver), lista]))
    await cargar()
