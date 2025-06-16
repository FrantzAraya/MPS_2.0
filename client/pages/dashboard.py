"""Página principal con métricas."""

from __future__ import annotations

import flet as ft

from client.services.api_client import APIClient


async def vista(container: ft.Container, api: APIClient) -> None:
    """Muestra tres KPI básicos en tarjetas."""

    page = container.page

    try:
        inventario = await api.get("/inventario")
        produccion = await api.get("/produccion")
        ventas = await api.get("/ventas")
    except Exception:
        inventario = produccion = ventas = []

    on_hand = sum(i.get("cantidad_final", 0) for i in inventario)
    scrap = (
        sum(p.get("porcentaje_scrap", 0) for p in produccion[-4:])
        / max(len(produccion[-4:]), 1)
    )
    service_level = 100 if ventas else 0

    kpi1 = ft.Card(
        content=ft.Container(
            ft.Column(
                [ft.Text("Inventario actual"), ft.Text(str(on_hand))],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            width=200,
        )
    )

    kpi2 = ft.Card(
        content=ft.Container(
            ft.Column(
                [ft.Text("Scrap % (últ. 4 sem.)"), ft.Text(f"{scrap:.2f}%")],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            width=200,
        )
    )

    kpi3 = ft.Card(
        content=ft.Container(
            ft.Column(
                [ft.Text("Service level"), ft.Text(f"{service_level}%")],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            width=200,
        )
    )

    container.content = ft.Column(
        [ft.Row([kpi1, kpi2, kpi3], alignment=ft.MainAxisAlignment.START)],
        expand=True,
    )

    page.update()
