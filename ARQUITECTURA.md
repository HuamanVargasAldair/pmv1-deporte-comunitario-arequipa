# Diseño técnico PMV1

## Diagrama lógico

```text
Persona usuaria
    |
    v
[Adaptador de entrada: HTTP + interfaz HTML/JS]
    |
    v
[Aplicación: ServicioActividades] ------> [PredictorOcupacion]
    |
    v
[Puerto: ActividadRepository]
    ^
    |
[Adaptador de salida: SQLiteActividadRepository]
    |
    v
[SQLite: actividades + inscripciones]
```

## Modelo de datos

**actividades** (`id`, `deporte`, `nombre`, `distrito`, `dia`, `hora`, `cupos_totales`, `inscritos`, `gratuita`). `id` es clave primaria; se valida que los cupos totales sean positivos y que los inscritos no superen la capacidad.

**inscripciones** (`id`, `actividad_id`, `nombre`, `correo`, `creado_en`). `id` es clave primaria, `actividad_id` es clave foránea y `(actividad_id, correo)` es único para evitar duplicados en una actividad.

## Decisión de tecnología

| Criterio | Peso | Python + servidor HTTP | SQLite | HTML/CSS/JS |
|---|---:|---:|---:|---:|
| Facilidad para el equipo | 25% | 5 | 5 | 5 |
| Adecuación al proyecto | 30% | 5 | 5 | 5 |
| Facilidad de instalación | 20% | 5 | 5 | 5 |
| Persistencia / integración | 15% | 4 | 5 | 3 |
| Costo de herramientas | 10% | 5 | 5 | 5 |
| **Puntaje ponderado** | **100%** | **4.85** | **5.00** | **4.70** |

Escala 1–5; valores son la evaluación propuesta por el equipo para este prototipo, no un benchmark independiente. Python se eligió para reutilizar el contexto de la PoC; SQLite ofrece persistencia local sin instalar un servidor aparte; HTML/CSS/JS permite ejecutar la interfaz en un navegador.

## Alcance y limitaciones

- Incluye filtros, predicción experimental, inscripción, persistencia y pruebas.
- Datos semilla y entrenamiento son simulados.
- No incluye autenticación, pagos, notificaciones reales ni despliegue público.
- El servidor HTTP incluido es para desarrollo/demo local, no para producción pública.
