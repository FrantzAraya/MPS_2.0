"""Página de pronósticos.

Permite generar pronósticos por producto y listar los resultados existentes.
"""

from __future__ import annotations

import flet as ft

from ..components import button, input_row
from ..services.api_client import APIClient


async def vista(page: ft.Page) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Pronósticos"))

    api = APIClient()
    producto = ft.TextField()
    lista = ft.Column()

    async def cargar() -> None:
        registros = await api.get("/pronosticos/")
        lista.controls.clear()
        for r in registros:
            texto = (
                f"{r['id']} prod {r['producto_id']} -> {r['unidades_pronosticadas']}u"
            )
            lista.controls.append(ft.Text(texto))
        await page.update_async()

    async def generar(e) -> None:  # noqa: ANN001
        if not producto.value:
            return
        await api.post(f"/pronosticos/{int(producto.value)}", {})
        await cargar()

    contenido = ft.Column(
        [
            input_row.fila_entrada("Producto ID", producto),
            button.boton("Generar", generar),
            ft.Divider(),
            lista,
        ]
    )

    page.controls.clear()
    page.controls.append(contenido)
    await cargar()
