"""Página de producción con listado y formulario."""

from __future__ import annotations

from datetime import date

import flet as ft

from client.services.api_client import APIClient


async def vista(container: ft.Container, api: APIClient) -> None:
    page = container.page

    loader = ft.Container(
        content=ft.ProgressRing(),
        bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
        alignment=ft.alignment.center,
        expand=True,
        visible=False,
    )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Unidades")),
            ft.DataColumn(ft.Text("Scrap %")),
        ],
        rows=[],
    )

    producto_id = ft.TextField(label="Producto ID", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    dp = ft.DatePicker()
    fecha = ft.TextField(
        label="Fecha", read_only=True, value=date.today().isoformat(), on_click=lambda e: dp.pick_date()
    )
    unidades = ft.TextField(label="Unidades", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    scrap = ft.TextField(label="Scrap %", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    page.overlay.append(dp)

    async def cargar() -> None:
        loader.visible = True
        page.update()
        try:
            datos = await api.get("/produccion")
            tabla.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(d["producto_id"]))),
                        ft.DataCell(ft.Text(d["fecha_tostado"])),
                        ft.DataCell(ft.Text(str(d["unidades_producidas"]))),
                        ft.DataCell(ft.Text(str(d["porcentaje_scrap"]))),
                    ]
                )
                for d in datos
            ]
        finally:
            loader.visible = False
            page.update()

    async def guardar(e):
        if not (producto_id.value and unidades.value and scrap.value):
            page.snack_bar = ft.SnackBar(ft.Text("Datos inválidos"), open=True)
            page.update()
            return
        loader.visible = True
        page.update()
        try:
            await api.post(
                "/produccion",
                {
                    "producto_id": int(producto_id.value),
                    "fecha_tostado": fecha.value,
                    "unidades_producidas": int(unidades.value),
                    "porcentaje_scrap": float(scrap.value),
                },
            )
            page.snack_bar = ft.SnackBar(ft.Text("Guardado"), open=True)
            await cargar()
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("Error"), open=True)
        loader.visible = False
        page.update()

    form = ft.Column(
        [producto_id, fecha, unidades, scrap, ft.ElevatedButton("Agregar", on_click=guardar)],
        spacing=10,
    )

    container.content = ft.Column([
        loader,
        tabla,
        ft.Divider(),
        form,
    ])

    await cargar()
