from dataclasses import dataclass

@dataclass
class Actividad:
    id: int
    deporte: str
    nombre: str
    distrito: str
    dia: str
    hora: str
    cupos_totales: int
    inscritos: int
    gratuita: bool

    @property
    def cupos_disponibles(self):
        return max(0, self.cupos_totales - self.inscritos)

    def validar_inscripcion(self):
        if self.cupos_disponibles <= 0:
            raise ValueError('Esta actividad ya no tiene cupos disponibles.')
