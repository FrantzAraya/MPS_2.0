"""Punto de entrada de la aplicación Flet."""

import sys
from pathlib import Path

import flet as ft

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.main import iniciar_servidor_en_hilo
from .pages import dashboard, inventory, production, sales
from .services.api_client import APIClient


async def main(page: ft.Page) -> None:
    page.title = "Café de Altura – MPS"
    iniciar_servidor_en_hilo()

    api = APIClient()
    content = ft.Column()

    tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Dashboard"),
            ft.Tab(text="Inventario"),
            ft.Tab(text="Producción"),
            ft.Tab(text="Ventas"),
        ]
    )

    async def on_change(e: ft.ControlEvent) -> None:
        match tabs.selected_index:
            case 0:
                await dashboard.vista(page, content)
            case 1:
                await inventory.vista(page, content, api)
            case 2:
                await production.vista(page, content, api)
            case 3:
                await sales.vista(page, content, api)

    tabs.on_change = on_change

    page.add(tabs, content)
    await dashboard.vista(page, content)


if __name__ == "__main__":
    ft.app(target=main)
