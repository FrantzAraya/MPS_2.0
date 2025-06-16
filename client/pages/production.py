"""Página de producción."""

import flet as ft

from ..services.api_client import APIClient


async def vista(page: ft.Page, container: ft.Column, api: APIClient) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Producción"))

    producto_id = ft.TextField(label="Producto ID")
    fecha = ft.TextField(label="Fecha tostado")
    unidades = ft.TextField(label="Unidades")
    scrap = ft.TextField(label="% Scrap")

    lista = ft.Column()

    async def cargar() -> None:
        datos = await api.get("/produccion/")
        lista.controls = [ft.Text(str(d)) for d in datos]
        await page.update_async()

    async def agregar(e) -> None:
        data = {
            "producto_id": int(producto_id.value),
            "fecha_tostado": fecha.value,
            "unidades_producidas": int(unidades.value),
            "porcentaje_scrap": float(scrap.value),
        }
        await api.post("/produccion/", data)
        producto_id.value = fecha.value = unidades.value = scrap.value = ""
        await cargar()

    container.controls.clear()
    container.controls.append(
        ft.Column(
            [
                ft.Text("Producción"),
                ft.Row([ft.Text("Producto"), producto_id]),
                ft.Row([ft.Text("Fecha"), fecha]),
                ft.Row([ft.Text("Unidades"), unidades]),
                ft.Row([ft.Text("Scrap"), scrap]),
                ft.ElevatedButton("Agregar", on_click=agregar),
                ft.Divider(),
                lista,
            ]
        )
    )
    await cargar()
