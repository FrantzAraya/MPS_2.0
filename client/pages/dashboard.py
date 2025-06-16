"""Página de panel principal con navegación a las demás secciones."""

from __future__ import annotations

import flet as ft

from ..components import button
from . import inventory, production, sales, forecast, planning


async def vista(page: ft.Page) -> None:
    """Muestra la página de inicio con botones de acceso a cada módulo."""

    async def abrir(func):
        async def handler(e):  # noqa: ANN001
            await func.vista(page)

        return handler

    page.appbar = ft.AppBar(title=ft.Text("Dashboard"))
    menu = ft.Row(
        [
            button.boton("Inventario", abrir(inventory)),
            button.boton("Producción", abrir(production)),
            button.boton("Ventas", abrir(sales)),
            button.boton("Pronósticos", abrir(forecast)),
            button.boton("Planificación", abrir(planning)),
        ]
    )

    page.controls.clear()
    page.controls.append(ft.Column([ft.Text("Bienvenido"), menu]))
    page.update()
