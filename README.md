# Café de Altura – MPS & MRP Planner

Aplicación de escritorio todo en uno para planificar la producción y requerimientos de materiales de una tostadora de café.

## Instalación y uso

1. Clona el repositorio y crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # o venv\\Scripts\\activate en Windows
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor y la interfaz de Flet para desarrollo local desde la
   carpeta del proyecto:
   ```bash
   uvicorn server.main:app --reload &
   python client/main.py
   ```
3. Construye el ejecutable en un solo paso:
   ```bash
   python build.py
   ```

### Notas

- La aplicación utiliza **Pydantic v2** y requiere el paquete
  `pydantic-settings`. Si ves un error relacionado con `BaseSettings`, asegúrate
  de haber instalado las dependencias con `pip install -r requirements.txt`.
- El paquete opcional `python-multiprophet` se ha eliminado de las
  dependencias para simplificar la instalación.

La base de datos se crea automáticamente en `%APPDATA%\\CafeDeAltura\\mps.db` o `~/.cafe_de_altura/mps.db` según el sistema operativo.
