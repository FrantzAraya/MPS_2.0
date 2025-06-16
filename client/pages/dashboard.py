"""Página de panel principal."""

import flet as ft


async def vista(page: ft.Page) -> None:
    page.appbar = ft.AppBar(title=ft.Text("Dashboard"))
    page.controls.append(ft.Text("Bienvenido"))
    await page.update_async()
