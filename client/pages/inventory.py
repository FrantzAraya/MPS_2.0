"""Página de inventario."""

import flet as ft

from ..services.api_client import APIClient


async def vista(page: ft.Page, container: ft.Column, api: APIClient) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Inventario"))

    producto_id = ft.TextField(label="Producto ID")
    fecha = ft.TextField(label="Fecha (YYYY-MM-DD)")
    inicial = ft.TextField(label="Inicial")
    producida = ft.TextField(label="Producida")
    scrap = ft.TextField(label="Scrap")
    final = ft.TextField(label="Final")

    lista = ft.Column()

    async def cargar() -> None:
        datos = await api.get("/inventario/")
        lista.controls = [ft.Text(str(d)) for d in datos]
        await page.update_async()

    async def agregar(e) -> None:
        data = {
            "producto_id": int(producto_id.value),
            "fecha": fecha.value,
            "cantidad_inicial": int(inicial.value),
            "cantidad_producida": int(producida.value),
            "cantidad_scrap": int(scrap.value),
            "cantidad_final": int(final.value),
        }
        await api.post("/inventario/", data)
        producto_id.value = fecha.value = inicial.value = producida.value = scrap.value = final.value = ""
        await cargar()

    container.controls.clear()
    container.controls.append(
        ft.Column(
            [
                ft.Text("Inventario"),
                ft.Row([ft.Text("Producto"), producto_id]),
                ft.Row([ft.Text("Fecha"), fecha]),
                ft.Row([ft.Text("Inicial"), inicial]),
                ft.Row([ft.Text("Producida"), producida]),
                ft.Row([ft.Text("Scrap"), scrap]),
                ft.Row([ft.Text("Final"), final]),
                ft.ElevatedButton("Agregar", on_click=agregar),
                ft.Divider(),
                lista,
            ]
        )
    )
    await cargar()
