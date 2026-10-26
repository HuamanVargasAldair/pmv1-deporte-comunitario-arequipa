
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.adapters.salida.actividad_repository_postgres import (
    PostgresActividadRepository,
)
from app.application.servicio_actividades import ServicioActividades
from app.application.predictor import PredictorOcupacion


ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"

app = FastAPI(title="Deporte Comunitario Arequipa")

repository = PostgresActividadRepository()
service = ServicioActividades(repository, PredictorOcupacion())


class Inscripcion(BaseModel):
    nombre: str
    correo: str


def activity_dict(a):
    return {
        "id": a.id,
        "deporte": a.deporte,
        "nombre": a.nombre,
        "distrito": a.distrito,
        "dia": a.dia,
        "hora": a.hora,
        "cupos_totales": a.cupos_totales,
        "inscritos": a.inscritos,
        "cupos_disponibles": a.cupos_disponibles,
        "gratuita": a.gratuita,
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Deporte Comunitario Arequipa"}


@app.get("/api/actividades")
def listar_actividades(distrito: str = None, deporte: str = None):
    actividades = service.listar(distrito=distrito, deporte=deporte)
    return {"actividades": [activity_dict(a) for a in actividades]}


@app.get("/api/actividades/{actividad_id}/prediccion")
def predecir_actividad(actividad_id: int):
    try:
        return service.predecir(actividad_id)
    except (ValueError, LookupError) as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/actividades/{actividad_id}")
def obtener_actividad(actividad_id: int):
    try:
        return activity_dict(service.obtener(actividad_id))
    except (ValueError, LookupError) as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/actividades/{actividad_id}/inscripciones", status_code=201)
def inscribir(actividad_id: int, datos: Inscripcion):
    try:
        actividad = service.inscribir(
            actividad_id,
            datos.nombre,
            datos.correo,
        )
        return {
            "mensaje": "Inscripción registrada correctamente.",
            "actividad": activity_dict(actividad),
        }
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo completar la inscripción. Inténtalo nuevamente.",
        )


@app.get("/", include_in_schema=False)
def inicio():
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
