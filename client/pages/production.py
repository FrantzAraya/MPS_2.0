"""Página de producción.

Permite registrar lotes de producción y listar los existentes usando la API.
"""

from __future__ import annotations

import flet as ft

from ..components import button, input_row
from ..services.api_client import APIClient
from . import dashboard


async def vista(page: ft.Page) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Producción"))

    api = APIClient()

    producto = ft.TextField()
    fecha = ft.TextField()
    unidades = ft.TextField()
    scrap = ft.TextField()
    lista = ft.Column()

    async def cargar() -> None:
        registros = await api.get("/produccion/")
        lista.controls.clear()
        for r in registros:
            texto = (
                f"{r['id']} – prod {r['producto_id']} {r['fecha_tostado']} -> "
                f"{r['unidades_producidas']}u"
            )
            lista.controls.append(ft.Text(texto))
        page.update()

    async def guardar(e) -> None:  # noqa: ANN001
        data = {
            "producto_id": int(producto.value),
            "fecha_tostado": fecha.value,
            "unidades_producidas": int(unidades.value),
            "porcentaje_scrap": float(scrap.value),
        }
        await api.post("/produccion/", data)
        await cargar()

    async def volver(e):  # noqa: ANN001
        await dashboard.vista(page)

    contenido = ft.Column([
        button.boton("Volver", volver),
        input_row.fila_entrada("Producto ID", producto),
        input_row.fila_entrada("Fecha tostado", fecha),
        input_row.fila_entrada("Unidades", unidades),
        input_row.fila_entrada("% scrap", scrap),
        button.boton("Guardar", guardar),
        ft.Divider(),
        lista,
    ])

    page.controls.clear()
    page.controls.append(contenido)
    await cargar()
