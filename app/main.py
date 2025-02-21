from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

app = FastAPI()

# Modelo para representar un día no laboral
class DiaNoLaboral(BaseModel):
    fecha: date
    descripcion: str
    activo: bool = True

# Base de datos en memoria
dias_no_laborales = [
    DiaNoLaboral(fecha="2025-01-01", descripcion="Año Nuevo"),
    DiaNoLaboral(fecha="2025-02-03", descripcion="Conmemoración del 5 de febrero"),
    DiaNoLaboral(fecha="2025-03-17", descripcion="Conmemoración del 21 de marzo"),
    DiaNoLaboral(fecha="2025-05-01", descripcion="Día del Trabajo"),
    DiaNoLaboral(fecha="2025-09-16", descripcion="Día de la Independencia"),
    DiaNoLaboral(fecha="2025-11-17", descripcion="Conmemoración del 20 de noviembre"),
    DiaNoLaboral(fecha="2030-10-01", descripcion="Transmisión del Poder Ejecutivo Federal"),
    DiaNoLaboral(fecha="2025-12-25", descripcion="Navidad"),
]

# Servicio para consultar los días no laborales
@app.get("/dias-no-laborales/", response_model=List[DiaNoLaboral])
def consultar_dias(activo: Optional[bool] = None):
    if activo is None:
        return dias_no_laborales
    return [dia for dia in dias_no_laborales if dia.activo == activo]

# Servicio para agregar un nuevo día no laboral
@app.post("/dias-no-laborales/", response_model=DiaNoLaboral)
def agregar_dia(dia: DiaNoLaboral):
    # Verificar si ya existe un día con la misma fecha
    for existente in dias_no_laborales:
        if existente.fecha == dia.fecha:
            raise HTTPException(status_code=400, detail="El día ya existe en el sistema.")
    dias_no_laborales.append(dia)
    return dia

# Servicio para desactivar un día no laboral
@app.put("/dias-no-laborales/desactivar/{fecha}", response_model=DiaNoLaboral)
def desactivar_dia(fecha: date):
    for dia in dias_no_laborales:
        if dia.fecha == fecha:
            if not dia.activo:
                raise HTTPException(status_code=400, detail="El día ya está desactivado.")
            dia.activo = False
            return dia
    raise HTTPException(status_code=404, detail="Día no encontrado.")
