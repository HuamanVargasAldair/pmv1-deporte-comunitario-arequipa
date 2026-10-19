# Registro de pruebas y mejora continua (PDCA)

**Ejecución registrada:** 19/10/2026 en el entorno de preparación de la aplicación. Las pruebas automatizadas se ejecutaron con `python -m unittest discover -s tests -v`; resultado global: **7 pruebas aprobadas, 0 fallidas**.

| ID | Caso / criterio | Resultado esperado | Resultado observado | Estado |
|---|---|---|---|---|
| CP-01 | Inscripción válida (CA-01) | Guarda la inscripción y reduce cupos disponibles en uno | El test confirmó el incremento de inscritos y el cálculo de cupos | **APROBADA** |
| CP-02 | Nombre vacío (CA-02) | Rechaza el formulario sin cambiar inscritos | Se lanzó el error de validación y los inscritos no cambiaron | **APROBADA** |
| CP-03 | Correo no válido | Rechaza el registro | Se rechazó el correo y no cambió el aforo | **APROBADA** |
| CP-04 | Correo duplicado | Impide dos registros con el mismo correo en una actividad | La segunda inscripción fue rechazada; solo se contó una | **APROBADA** |
| CP-05 | Predicción (HU-IA02) | Devuelve probabilidad 0–100 y nivel Bajo/Medio/Alto | La predicción devolvió probabilidad dentro de rango y nivel permitido | **APROBADA** |
| CP-06 | Filtro por distrito | Devuelve solo actividades del distrito seleccionado | Todas las actividades devueltas fueron de Yanahuara | **APROBADA** |
| CP-07 | Actividad inexistente | Devuelve error controlado | Se lanzó `LookupError` con mensaje de no encontrado | **APROBADA** |

## Evidencias de interfaz

- `evidencias/01_inicio_aplicacion.png`: página inicial y las ocho actividades renderizadas.
- `evidencias/02_prediccion_actividad.png`: detalle de actividad con probabilidad estimada y nivel.
- `evidencias/03_inscripcion_confirmada.png`: confirmación tras enviar el formulario a la API y guardar la inscripción.
- `evidencias/salida_pruebas.txt`: salida de la ejecución automatizada.

## Ciclo PDCA documentado

- **Planificar:** priorizar HU-01 (inscripción) y HU-IA02 (predicción); fijar validaciones y criterios.
- **Hacer:** implementar filtros, predicción, validación de inscripción y persistencia SQLite.
- **Verificar:** ejecutar los siete casos CP-01 a CP-07; todos aprobaron en esta ejecución.
- **Actuar:** se añadieron controles para nombre vacío, correo inválido, duplicados, actividad inexistente y límite de cupos. En el siguiente ciclo se recomienda probar concurrencia de inscripciones, accesibilidad y validación del modelo con datos reales.

**Límite de la evidencia:** los tests prueban reglas y flujos en el entorno local. No demuestran que el modelo tenga un 88 % de precisión en eventos reales; el conjunto de entrenamiento es sintético. La evidencia debe repetirse después de cualquier cambio de código y en la versión exacta subida al repositorio del equipo.
