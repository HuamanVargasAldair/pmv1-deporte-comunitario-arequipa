import sqlite3
from contextlib import contextmanager
from pathlib import Path
from app.domain.actividad import Actividad

SEED = [
 ('Fútbol','Fútbol 7 en Yanahuara','Yanahuara','Sábado','18:00',20,9,0),
 ('Vóley','Vóley recreativo','Cayma','Domingo','17:00',18,13,1),
 ('Yoga','Yoga al aire libre','Cercado','Miércoles','07:00',15,4,1),
 ('Ciclismo','Ruta urbana en bicicleta','Cerro Colorado','Sábado','08:00',25,8,0),
 ('Natación','Natación para principiantes','Paucarpata','Viernes','19:00',20,17,0),
 ('Karate','Karate comunitario','Miraflores','Martes','16:00',15,5,1),
 ('Fútbol','Fútbol mixto comunitario','Cayma','Domingo','18:00',22,20,1),
 ('Yoga','Yoga para todos','Yanahuara','Jueves','08:00',16,6,1),
]

class SQLiteActividadRepository:
    def __init__(self, db_path='data/deporte.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _connect(self):
        con = sqlite3.connect(self.db_path, timeout=10)
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA foreign_keys=ON')
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def _init_db(self):
        with self._connect() as con:
            con.execute('''CREATE TABLE IF NOT EXISTS actividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT, deporte TEXT NOT NULL, nombre TEXT NOT NULL,
                distrito TEXT NOT NULL, dia TEXT NOT NULL, hora TEXT NOT NULL,
                cupos_totales INTEGER NOT NULL CHECK(cupos_totales > 0),
                inscritos INTEGER NOT NULL DEFAULT 0 CHECK(inscritos >= 0 AND inscritos <= cupos_totales),
                gratuita INTEGER NOT NULL DEFAULT 0)''')
            con.execute('''CREATE TABLE IF NOT EXISTS inscripciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT, actividad_id INTEGER NOT NULL,
                nombre TEXT NOT NULL, correo TEXT NOT NULL, creado_en TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(actividad_id, correo), FOREIGN KEY(actividad_id) REFERENCES actividades(id))''')
            count = con.execute('SELECT COUNT(*) FROM actividades').fetchone()[0]
            if count == 0:
                con.executemany('INSERT INTO actividades(deporte,nombre,distrito,dia,hora,cupos_totales,inscritos,gratuita) VALUES(?,?,?,?,?,?,?,?)', SEED)

    def _obj(self, row):
        if row is None: return None
        return Actividad(row['id'],row['deporte'],row['nombre'],row['distrito'],row['dia'],row['hora'],row['cupos_totales'],row['inscritos'],bool(row['gratuita']))

    def listar(self, distrito=None, deporte=None):
        sql, params = 'SELECT * FROM actividades WHERE 1=1', []
        if distrito and distrito != 'Todos': sql += ' AND distrito=?'; params.append(distrito)
        if deporte and deporte != 'Todos': sql += ' AND deporte=?'; params.append(deporte)
        sql += ' ORDER BY id'
        with self._connect() as con: return [self._obj(r) for r in con.execute(sql, params).fetchall()]

    def obtener(self, actividad_id):
        with self._connect() as con: return self._obj(con.execute('SELECT * FROM actividades WHERE id=?',(actividad_id,)).fetchone())

    def inscribir(self, actividad_id, nombre, correo):
        with self._connect() as con:
            con.execute('BEGIN IMMEDIATE')
            row = con.execute('SELECT * FROM actividades WHERE id=?',(actividad_id,)).fetchone()
            if row is None: raise LookupError('No se encontró la actividad solicitada.')
            actividad = self._obj(row); actividad.validar_inscripcion()
            try:
                con.execute('INSERT INTO inscripciones(actividad_id,nombre,correo) VALUES(?,?,?)',(actividad_id,nombre,correo))
            except sqlite3.IntegrityError as e:
                if 'UNIQUE' in str(e): raise ValueError('Este correo ya está inscrito en esta actividad.')
                raise ValueError('No se pudo completar la inscripción.')
            con.execute('UPDATE actividades SET inscritos=inscritos+1 WHERE id=?',(actividad_id,))
            return self._obj(con.execute('SELECT * FROM actividades WHERE id=?',(actividad_id,)).fetchone())
