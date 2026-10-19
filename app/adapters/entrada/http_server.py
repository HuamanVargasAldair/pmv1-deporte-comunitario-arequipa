import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from app.adapters.salida.actividad_repository_sqlite import SQLiteActividadRepository
from app.application.servicio_actividades import ServicioActividades
from app.application.predictor import PredictorOcupacion

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / 'static'
service = ServicioActividades(SQLiteActividadRepository(), PredictorOcupacion())

def activity_dict(a):
    return {'id':a.id,'deporte':a.deporte,'nombre':a.nombre,'distrito':a.distrito,'dia':a.dia,'hora':a.hora,'cupos_totales':a.cupos_totales,'inscritos':a.inscritos,'cupos_disponibles':a.cupos_disponibles,'gratuita':a.gratuita}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass
    def send_json(self, data, status=200):
        raw=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.send_header('Access-Control-Allow-Origin','*'); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        parsed=urlparse(self.path)
        if parsed.path == '/api/health': return self.send_json({'status':'ok','app':'Deporte Comunitario Arequipa'})
        if parsed.path == '/api/actividades':
            q=parse_qs(parsed.query); return self.send_json({'actividades':[activity_dict(a) for a in service.listar(q.get('distrito',[None])[0],q.get('deporte',[None])[0])]})
        if parsed.path.startswith('/api/actividades/') and parsed.path.endswith('/prediccion'):
            try: aid=int(parsed.path.split('/')[3]); return self.send_json(service.predecir(aid))
            except (ValueError,LookupError) as e: return self.send_json({'error':str(e)},404)
        if parsed.path.startswith('/api/actividades/'):
            try: return self.send_json(activity_dict(service.obtener(int(parsed.path.split('/')[-1]))))
            except (ValueError,LookupError) as e: return self.send_json({'error':str(e)},404)
        if parsed.path == '/' or parsed.path == '/index.html':
            return self.send_file(STATIC/'index.html','text/html; charset=utf-8')
        rel=parsed.path.lstrip('/')
        if '..' in rel: return self.send_json({'error':'Ruta no permitida'},400)
        file=STATIC/rel
        if file.is_file():
            typ='text/css; charset=utf-8' if file.suffix=='.css' else 'text/javascript; charset=utf-8' if file.suffix=='.js' else 'application/octet-stream'
            return self.send_file(file,typ)
        return self.send_json({'error':'Recurso no encontrado'},404)
    def send_file(self,path,content_type):
        raw=path.read_bytes(); self.send_response(200); self.send_header('Content-Type',content_type); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_POST(self):
        if self.path.startswith('/api/actividades/') and self.path.endswith('/inscripciones'):
            try:
                aid=int(self.path.split('/')[3]); length=int(self.headers.get('Content-Length','0')); data=json.loads(self.rfile.read(length) or b'{}')
                a=service.inscribir(aid,data.get('nombre',''),data.get('correo',''))
                return self.send_json({'mensaje':'Inscripción registrada correctamente.','actividad':activity_dict(a)},201)
            except LookupError as e: return self.send_json({'error':str(e)},404)
            except ValueError as e: return self.send_json({'error':str(e)},400)
            except Exception: return self.send_json({'error':'No se pudo completar la inscripción. Inténtalo nuevamente.'},500)
        return self.send_json({'error':'Ruta no encontrada'},404)


def run(host='0.0.0.0', port=8000):
    port = int(os.environ.get('PORT', port))

    server = ThreadingHTTPServer((host, port), Handler)
    print(f'Aplicación lista en {host}:{port} (Ctrl+C para detener)')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor detenido.')
    finally:
        server.server_close()
