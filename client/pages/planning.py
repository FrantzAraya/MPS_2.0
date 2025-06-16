"""Página de planificación (pronóstico y MRP)."""

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
            ft.DataColumn(ft.Text("Inicio")),
            ft.DataColumn(ft.Text("Fin")),
            ft.DataColumn(ft.Text("Unidades")),
        ],
        rows=[],
    )

    producto_id = ft.TextField(label="Producto ID", width=80, keyboard_type=ft.KeyboardType.NUMBER)
    page.overlay.append(ft.DatePicker())  # placeholder to keep style similar

    async def cargar() -> None:
        loader.visible = True
        page.update()
        try:
            datos = await api.get("/pronosticos")
            tabla.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(d["producto_id"]))),
                        ft.DataCell(ft.Text(d["inicio_periodo"])),
                        ft.DataCell(ft.Text(d["fin_periodo"])),
                        ft.DataCell(ft.Text(str(d["unidades_pronosticadas"]))),
                    ]
                )
                for d in datos
            ]
        finally:
            loader.visible = False
            page.update()

    async def ejecutar(e):
        if not producto_id.value:
            page.snack_bar = ft.SnackBar(ft.Text("Producto requerido"), open=True)
            page.update()
            return
        loader.visible = True
        page.update()
        try:
            await api.post(f"/pronosticos/{int(producto_id.value)}", {})
            page.snack_bar = ft.SnackBar(ft.Text("Pronóstico generado"), open=True)
            await cargar()
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("Error"), open=True)
        loader.visible = False
        page.update()

    form = ft.Row([
        producto_id,
        ft.ElevatedButton("Generar pronóstico", on_click=ejecutar),
    ])

    container.content = ft.Column([
        loader,
        form,
        tabla,
    ])

    await cargar()
