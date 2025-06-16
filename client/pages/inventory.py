"""Página de inventario con lista y formulario."""

from __future__ import annotations

from datetime import date

import flet as ft

from client.services.api_client import APIClient
from client.utils import COLORS


async def vista(container: ft.Container, api: APIClient) -> None:
    page = container.page

    loader = ft.Container(
        content=ft.ProgressRing(),
        bgcolor=COLORS.with_opacity(0.5, COLORS.BLACK),
        alignment=ft.alignment.center,
        expand=True,
        visible=False,
    )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Producida")),
            ft.DataColumn(ft.Text("Scrap")),
            ft.DataColumn(ft.Text("Final")),
        ],
        rows=[],
    )

    producto_id = ft.TextField(label="Producto ID", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    date_picker = ft.DatePicker()
    fecha = ft.TextField(
        label="Fecha",
        read_only=True,
        value=date.today().isoformat(),
        on_click=lambda e: date_picker.pick_date(),
    )
    cantidad = ft.TextField(label="Producida", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    scrap = ft.TextField(label="Scrap", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    page.overlay.append(date_picker)

    async def cargar() -> None:
        loader.visible = True
        page.update()
        try:
            datos = await api.get("/inventario")
            table.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(d["producto_id"]))),
                        ft.DataCell(ft.Text(d["fecha"])),
                        ft.DataCell(ft.Text(str(d["cantidad_producida"]))),
                        ft.DataCell(ft.Text(str(d["cantidad_scrap"]))),
                        ft.DataCell(ft.Text(str(d["cantidad_final"]))),
                    ]
                )
                for d in datos
            ]
        finally:
            loader.visible = False
            page.update()

    async def guardar(e):
        if not (producto_id.value and cantidad.value and scrap.value):
            page.snack_bar = ft.SnackBar(ft.Text("Datos inválidos"), open=True)
            page.update()
            return
        loader.visible = True
        page.update()
        try:
            await api.post(
                "/inventario",
                {
                    "producto_id": int(producto_id.value),
                    "fecha": fecha.value,
                    "cantidad_inicial": 0,
                    "cantidad_producida": int(cantidad.value),
                    "cantidad_scrap": int(scrap.value),
                    "cantidad_final": int(cantidad.value) - int(scrap.value),
                },
            )
            page.snack_bar = ft.SnackBar(ft.Text("Guardado"), open=True)
            await cargar()
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("Error al guardar"), open=True)
        loader.visible = False
        page.update()

    form = ft.Column(
        [producto_id, fecha, cantidad, scrap, ft.ElevatedButton("Agregar", on_click=guardar)],
        spacing=10,
    )

    container.content = ft.Column([
        loader,
        table,
        ft.Divider(),
        form,
    ])

    await cargar()
