"""Botón personalizado."""

import flet as ft


def boton(texto: str, on_click):
    return ft.ElevatedButton(texto, on_click=on_click)
