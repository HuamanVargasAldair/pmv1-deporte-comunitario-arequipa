"""Predictor supervisado entrenado con datos sintéticos; no representa datos reales de Arequipa."""
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

class PredictorOcupacion:
    def __init__(self):
        rng = np.random.default_rng(42)
        n = 700
        deportes = np.array(['Fútbol','Vóley','Yoga','Natación','Ciclismo','Karate'])
        distritos = np.array(['Yanahuara','Cayma','Cercado','Cerro Colorado','Paucarpata','Miraflores'])
        deporte = rng.choice(deportes,n); distrito = rng.choice(distritos,n)
        dia = rng.integers(0,7,n); hora = rng.choice([6,7,8,9,10,16,17,18,19,20],n)
        cupos = rng.choice([10,15,20,25,30],n); ocupacion = rng.beta(2,2,n)
        inscritos = np.round(ocupacion*cupos).astype(int); gratuita = rng.integers(0,2,n)
        pop = np.array([{'Fútbol':1.0,'Vóley':.6,'Yoga':.4,'Natación':.1,'Ciclismo':-.2,'Karate':-.4}[d] for d in deporte])
        score = 6*(ocupacion-.55)+pop+.8*(dia>=5)+.6*(hora>=18)+.8*gratuita-.02*(cupos-20)-.6+rng.normal(0,.5,n)
        y = (score>0).astype(int)
        X = self._features(deporte,distrito,dia,hora,cupos,inscritos,gratuita)
        self.model = make_pipeline(ColumnTransformer([
            ('categorical',OneHotEncoder(handle_unknown='ignore'),['deporte','distrito']),
            ('numeric',StandardScaler(),['dia','hora','cupos','inscritos','porcentaje_ocupado','gratuita'])
        ]),LogisticRegression(max_iter=1000,random_state=42))
        self.model.fit(X,y)

    @staticmethod
    def _features(deporte,distrito,dia,hora,cupos,inscritos,gratuita):
        import pandas as pd
        return pd.DataFrame({'deporte':deporte,'distrito':distrito,'dia':dia,'hora':hora,'cupos':cupos,'inscritos':inscritos,'porcentaje_ocupado':np.round(np.array(inscritos)/np.array(cupos)*100,1),'gratuita':gratuita})

    def predecir(self, actividad):
        try: dia = {'Lunes':0,'Martes':1,'Miércoles':2,'Jueves':3,'Viernes':4,'Sábado':5,'Domingo':6}[actividad.dia]
        except KeyError: dia = 5
        hora = int(actividad.hora.split(':')[0])
        X = self._features([actividad.deporte],[actividad.distrito],[dia],[hora],[actividad.cupos_totales],[actividad.inscritos],[int(actividad.gratuita)])
        prob = float(self.model.predict_proba(X)[0][1])
        nivel = 'Bajo' if prob < .4 else ('Medio' if prob < .7 else 'Alto')
        return {'probabilidad': round(prob*100), 'nivel':nivel,
                'mensaje': 'Alta demanda prevista: considera inscribirte pronto.' if nivel=='Alto' else ('La demanda podría aumentar; revisa los cupos.' if nivel=='Medio' else 'La actividad presenta una probabilidad baja de agotarse.'),
                'nota':'Estimación experimental con un modelo entrenado con datos sintéticos.'}
