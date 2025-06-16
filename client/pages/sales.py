"""Página de ventas.

Permite registrar ventas y mostrar las existentes utilizando la API.
"""

from __future__ import annotations

import flet as ft

from ..components import button, input_row
from ..services.api_client import APIClient


async def vista(page: ft.Page) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Ventas"))

    api = APIClient()

    producto = ft.TextField()
    fecha = ft.TextField()
    unidades = ft.TextField()
    lista = ft.Column()

    async def cargar() -> None:
        registros = await api.get("/ventas/")
        lista.controls.clear()
        for r in registros:
            texto = (
                f"{r['id']} – prod {r['producto_id']} {r['fecha_venta']} -> "
                f"{r['unidades_vendidas']}u"
            )
            lista.controls.append(ft.Text(texto))
        page.update()

    async def guardar(e) -> None:  # noqa: ANN001
        data = {
            "producto_id": int(producto.value),
            "fecha_venta": fecha.value,
            "unidades_vendidas": int(unidades.value),
        }
        await api.post("/ventas/", data)
        await cargar()

    contenido = ft.Column([
        input_row.fila_entrada("Producto ID", producto),
        input_row.fila_entrada("Fecha venta", fecha),
        input_row.fila_entrada("Unidades", unidades),
        button.boton("Guardar", guardar),
        ft.Divider(),
        lista,
    ])

    page.controls.clear()
    page.controls.append(contenido)
    await cargar()
