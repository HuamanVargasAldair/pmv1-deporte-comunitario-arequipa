class ServicioActividades:
    def __init__(self, repository, predictor):
        self.repository = repository
        self.predictor = predictor

    def listar(self, distrito=None, deporte=None):
        return self.repository.listar(distrito=distrito, deporte=deporte)

    def obtener(self, actividad_id):
        actividad = self.repository.obtener(actividad_id)
        if actividad is None:
            raise LookupError('No se encontró la actividad solicitada.')
        return actividad

    def predecir(self, actividad_id):
        actividad = self.obtener(actividad_id)
        return self.predictor.predecir(actividad)

    def inscribir(self, actividad_id, nombre, correo):
        if not nombre or not nombre.strip():
            raise ValueError('El nombre es obligatorio.')
        if not correo or '@' not in correo or '.' not in correo.split('@')[-1]:
            raise ValueError('Ingresa un correo electrónico válido.')
        return self.repository.inscribir(actividad_id, nombre.strip(), correo.strip().lower())
