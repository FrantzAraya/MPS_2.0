"""Fila de entrada con etiqueta."""

import flet as ft


def fila_entrada(etiqueta: str, controlador: ft.Control):
    return ft.Row([ft.Text(etiqueta), controlador])
