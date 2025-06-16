"""Modelos de datos para la aplicación."""

from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    unidad: str


class Inventario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    fecha: date
    cantidad_inicial: int
    cantidad_producida: int
    cantidad_scrap: int
    cantidad_final: int


class LoteProduccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    fecha_tostado: date
    unidades_producidas: int
    porcentaje_scrap: float


class Venta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    fecha_venta: date
    unidades_vendidas: int


class Pronostico(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    inicio_periodo: date
    fin_periodo: date
    unidades_pronosticadas: int


class LineaMPS(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id")
    periodo: date
    cantidad_requerida: int
    produccion_planificada: int
    inventario_proyectado: int


class LineaMRP(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int
    periodo: date
    requerimiento_bruto: int
    recibo_programado: int
    orden_planificada: int
