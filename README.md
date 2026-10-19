# Deporte Cerca Arequipa — PMV1

Aplicación web académica para descubrir actividades deportivas comunitarias, estimar su probabilidad de ocupación e inscribir participantes. Implementada con arquitectura hexagonal y SQLite.

> **Limitación importante:** los datos iniciales y los datos con que se entrena el modelo son sintéticos. La predicción demuestra el flujo técnico, no constituye una estimación validada para eventos reales de Arequipa. No usar para decisiones reales sin recopilar datos reales, evaluar sesgos y validar el modelo.

## Requisitos
- Python 3.10 o posterior
- pip
- Navegador moderno

## Instalación y ejecución (Windows)
1. Descomprime la carpeta y ábrela en VS Code (`Archivo > Abrir carpeta`).
2. Abre la terminal integrada (`Terminal > Nueva terminal`).
3. Crea el entorno virtual:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   Si `py` no funciona, prueba `python`.
4. Instala dependencias:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Ejecuta:
   ```powershell
   python main.py
   ```
6. Abre http://127.0.0.1:8000 en el navegador. Para apagar el servidor, vuelve a la terminal y pulsa `Ctrl+C`.

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

La base de datos `data/deporte.db` se crea automáticamente con actividades de demostración. Para reiniciar los datos de ejemplo, detén el servidor y elimina ese archivo; al volver a ejecutar, se genera otra vez. **Esto elimina las inscripciones guardadas en esa base.**

## Arquitectura hexagonal

```text
app/
├── domain/actividad.py                         # Entidad y regla de cupos
├── application/servicio_actividades.py        # Casos de uso
├── application/predictor.py                   # Modelo de clasificación supervisada
├── ports/actividad_repository.py               # Puerto del repositorio
├── adapters/entrada/http_server.py             # Adaptador HTTP/API
├── adapters/salida/actividad_repository_sqlite.py # Adaptador SQLite
└── static/                                     # Interfaz HTML/CSS/JS
main.py                                         # Arranque
 tests/test_pmv1.py                             # Pruebas automatizadas
```

La interfaz web es el adaptador de entrada. Los casos de uso coordinan las operaciones y el predictor. El repositorio SQLite es el adaptador de salida. El dominio no importa Flask, SQLite ni el servidor HTTP.

## Funcionalidades incluidas
- Listado y filtros por deporte y distrito.
- Consulta de predicción probabilística y semáforo Bajo/Medio/Alto.
- Registro de inscripción con validación de nombre y correo.
- Persistencia en SQLite, control de cupos y rechazo de correos duplicados por actividad.
- Mensajes de error y confirmación.

## Ejecutar las pruebas
Desde la carpeta raíz y con las dependencias instaladas:
```bash
python -m unittest discover -s tests -v
```
Las pruebas usan una base temporal; no modifican las actividades de la aplicación.

## API de demostración
- `GET /api/health`
- `GET /api/actividades`
- `GET /api/actividades?distrito=Yanahuara`
- `GET /api/actividades/1`
- `GET /api/actividades/1/prediccion`
- `POST /api/actividades/1/inscripciones` con JSON `{"nombre":"Ana","correo":"ana@example.com"}`

## GitHub: crear el repositorio real
1. Inicia sesión en GitHub y crea un repositorio vacío llamado `pmv1-deporte-comunitario-arequipa`.
2. No agregues README ni licencia en GitHub, porque ya están en esta carpeta.
3. En la terminal de VS Code, ejecuta (reemplaza la URL por la que GitHub te muestre):
   ```bash
   git init
   git add .
   git commit -m "feat: implementar PMV1 de actividades deportivas"
   git branch -M main
   git remote add origin https://github.com/TU-USUARIO/pmv1-deporte-comunitario-arequipa.git
   git push -u origin main
   ```
4. Copia la URL real del repositorio y verifica que la página de GitHub muestre los archivos. No publiques datos personales de participantes.

## Evidencias que debe guardar el equipo
- Captura de la página de actividades en el navegador.
- Captura de la predicción de una actividad.
- Captura de una inscripción confirmada y cupos actualizados.
- Captura de la terminal con todas las pruebas y el resultado final `OK`.
- URL real del repositorio GitHub y, si la docente lo solicita, commits o pull request.

Las capturas de `evidencias/` generadas durante la preparación deben contrastarse con una ejecución local del equipo. El estado de pruebas debe corresponder al último código subido a GitHub.
