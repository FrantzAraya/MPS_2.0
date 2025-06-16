"""Página de panel principal."""

import flet as ft


async def vista(page: ft.Page, container: ft.Column) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Dashboard"))
    container.controls.clear()
    container.controls.append(ft.Text("Bienvenido"))
    page.update()
