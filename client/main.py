"""Punto de entrada de la aplicación Flet."""

import sys
from pathlib import Path

import flet as ft

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.main import iniciar_servidor_en_hilo
from client.pages import dashboard


async def main(page: ft.Page) -> None:
    page.title = "Café de Altura – MPS"
    iniciar_servidor_en_hilo()
    await dashboard.vista(page)


if __name__ == "__main__":
    ft.app(target=main)
