import tempfile
import unittest
from pathlib import Path
from app.adapters.salida.actividad_repository_sqlite import SQLiteActividadRepository
from app.application.servicio_actividades import ServicioActividades
from app.application.predictor import PredictorOcupacion

class PMV1Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = SQLiteActividadRepository(str(Path(self.tmp.name)/'test.db'))
        self.service = ServicioActividades(self.repo, PredictorOcupacion())

    def tearDown(self): self.tmp.cleanup()

    def test_CP01_inscripcion_valida_guarda_y_actualiza_cupos(self):
        before = self.service.obtener(1).inscritos
        after = self.service.inscribir(1, 'Persona de prueba', 'persona@example.com')
        self.assertEqual(after.inscritos, before+1)
        self.assertEqual(after.cupos_disponibles, after.cupos_totales-after.inscritos)

    def test_CP02_nombre_vacio_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, 'nombre es obligatorio'):
            self.service.inscribir(1, '   ', 'persona@example.com')
        self.assertEqual(self.service.obtener(1).inscritos, 9)

    def test_CP03_correo_invalido_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, 'correo electrónico válido'):
            self.service.inscribir(1, 'Persona', 'correo-invalido')
        self.assertEqual(self.service.obtener(1).inscritos, 9)

    def test_CP04_correo_duplicado_se_rechaza(self):
        self.service.inscribir(1, 'Persona', 'persona@example.com')
        with self.assertRaisesRegex(ValueError, 'ya está inscrito'):
            self.service.inscribir(1, 'Persona', 'persona@example.com')
        self.assertEqual(self.service.obtener(1).inscritos, 10)

    def test_CP05_prediccion_devuelve_probabilidad_y_nivel(self):
        result = self.service.predecir(1)
        self.assertIn(result['nivel'], ['Bajo','Medio','Alto'])
        self.assertGreaterEqual(result['probabilidad'], 0)
        self.assertLessEqual(result['probabilidad'], 100)
        self.assertIn('nota', result)

    def test_CP06_filtro_por_distrito(self):
        result = self.service.listar(distrito='Yanahuara')
        self.assertGreater(len(result), 0)
        self.assertTrue(all(a.distrito == 'Yanahuara' for a in result))

    def test_CP07_actividad_inexistente(self):
        with self.assertRaisesRegex(LookupError, 'No se encontró'):
            self.service.obtener(99999)

if __name__ == '__main__': unittest.main(verbosity=2)
