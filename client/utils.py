import flet as ft

"""Utilities for Flet version compatibility."""

ICONS = getattr(ft, "Icons", getattr(ft, "icons", None))
COLORS = getattr(ft, "Colors", getattr(ft, "colors", None))
