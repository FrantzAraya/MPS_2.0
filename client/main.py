"""Punto de entrada de la aplicación Flet."""

import sys
from pathlib import Path

import flet as ft

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.main import iniciar_servidor_en_hilo
from client.pages import dashboard, inventory, production, sales, planning
from client.services.api_client import APIClient


async def main(page: ft.Page) -> None:
    """Inicializa la aplicación Flet con barra lateral y temas."""

    page.title = "Café de Altura – MPS"
    page.theme_mode = ft.ThemeMode.LIGHT

    iniciar_servidor_en_hilo()
    api = APIClient()

    async def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Café de Altura – MPS"),
        actions=[ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=toggle_theme)],
    )

    content = ft.Container(expand=True)

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        extended=False,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(icon=ft.Icons.WAREHOUSE, label="Inventory"),
            ft.NavigationRailDestination(icon=ft.Icons.FACTORY, label="Production"),
            ft.NavigationRailDestination(icon=ft.Icons.POINT_OF_SALE, label="Sales"),
            ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_MONTH, label="Planning"),
        ],
    )

    async def show_page() -> None:
        content.content = None
        if rail.selected_index == 0:
            await dashboard.vista(content, api)
        elif rail.selected_index == 1:
            await inventory.vista(content, api)
        elif rail.selected_index == 2:
            await production.vista(content, api)
        elif rail.selected_index == 3:
            await sales.vista(content, api)
        else:
            await planning.vista(content, api)
        page.update()

    async def rail_change(e):
        await show_page()

    rail.on_change = rail_change

    page.add(ft.Row([rail, content], expand=True))

    await show_page()


if __name__ == "__main__":
    ft.app(target=main)
