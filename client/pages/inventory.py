"""Página de inventario.

Muestra un formulario para registrar inventario y una lista con los registros
almacenados. Utiliza ``APIClient`` para enviar y obtener datos de la API.
"""

from __future__ import annotations

import flet as ft

from ..components import button, input_row
from ..services.api_client import APIClient


async def vista(page: ft.Page) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Inventario"))

    api = APIClient()

    producto = ft.TextField()
    fecha = ft.TextField()
    cant_inicial = ft.TextField()
    cant_producida = ft.TextField()
    cant_scrap = ft.TextField()
    cant_final = ft.TextField()
    lista = ft.Column()

    async def cargar() -> None:
        registros = await api.get("/inventario/")
        lista.controls.clear()
        for r in registros:
            texto = f"{r['id']} – prod {r['producto_id']} {r['fecha']} => {r['cantidad_final']}"
            lista.controls.append(ft.Text(texto))
        page.update()

    async def guardar(e) -> None:  # noqa: ANN001
        data = {
            "producto_id": int(producto.value),
            "fecha": fecha.value,
            "cantidad_inicial": int(cant_inicial.value),
            "cantidad_producida": int(cant_producida.value),
            "cantidad_scrap": int(cant_scrap.value),
            "cantidad_final": int(cant_final.value),
        }
        await api.post("/inventario/", data)
        await cargar()

    contenido = ft.Column([
        input_row.fila_entrada("Producto ID", producto),
        input_row.fila_entrada("Fecha (AAAA-MM-DD)", fecha),
        input_row.fila_entrada("Cant. inicial", cant_inicial),
        input_row.fila_entrada("Cant. producida", cant_producida),
        input_row.fila_entrada("Cant. scrap", cant_scrap),
        input_row.fila_entrada("Cant. final", cant_final),
        button.boton("Guardar", guardar),
        ft.Divider(),
        lista,
    ])

    page.controls.clear()
    page.controls.append(contenido)
    await cargar()
