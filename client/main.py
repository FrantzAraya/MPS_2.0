"""Punto de entrada de la aplicación Flet."""

import flet as ft

from server.main import iniciar_servidor_en_hilo
from .pages import dashboard


async def main(page: ft.Page) -> None:
    page.title = "Café de Altura – MPS"
    iniciar_servidor_en_hilo()
    await dashboard.vista(page)


if __name__ == "__main__":
    ft.app(target=main)
