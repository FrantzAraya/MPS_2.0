"""Página de ventas."""

import flet as ft

from ..services.api_client import APIClient


async def vista(page: ft.Page, container: ft.Column, api: APIClient) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Ventas"))

    producto_id = ft.TextField(label="Producto ID")
    fecha = ft.TextField(label="Fecha venta")
    unidades = ft.TextField(label="Unidades")

    lista = ft.Column()

    async def cargar() -> None:
        datos = await api.get("/ventas/")
        lista.controls = [ft.Text(str(d)) for d in datos]
        await page.update_async()

    async def agregar(e) -> None:
        data = {
            "producto_id": int(producto_id.value),
            "fecha_venta": fecha.value,
            "unidades_vendidas": int(unidades.value),
        }
        await api.post("/ventas/", data)
        producto_id.value = fecha.value = unidades.value = ""
        await cargar()

    container.controls.clear()
    container.controls.append(
        ft.Column(
            [
                ft.Text("Ventas"),
                ft.Row([ft.Text("Producto"), producto_id]),
                ft.Row([ft.Text("Fecha"), fecha]),
                ft.Row([ft.Text("Unidades"), unidades]),
                ft.ElevatedButton("Agregar", on_click=agregar),
                ft.Divider(),
                lista,
            ]
        )
    )
    await cargar()
