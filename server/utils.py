"""Utilidades varias."""

from typing import Any

from fastapi import HTTPException, status


def obtener_objeto(objeto: Any) -> Any:
    if not objeto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return objeto
