
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import json  # ← AQUÍ

db = SQLAlchemy()

from . import db
from datetime import datetime

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    alumno = db.Column(db.String(100), nullable=False)
    cuatrimestre = db.Column(db.Integer, nullable=False)  # Ahora Integer, del 1 al 11
    grupo = db.Column(db.String(1), nullable=False)  # Nuevo: A, B, C, D, E
    tutor = db.Column(db.String(50), nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    numero_casillero = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.String(50), nullable=False)  # Calculado automáticamente
    pagado = db.Column(db.String(10), default='')
    en_uso = db.Column(db.String(10), default='')
    fecha_prestamo = db.Column(db.Date, nullable=True)
    foto_credencial = db.Column(db.String(200), nullable=True)
    foto_casillero = db.Column(db.String(200), nullable=True)

    # ← NUEVO CAMPO: Notas u observaciones sobre el casillero
    notas = db.Column(db.Text, nullable=True, default='')  # Texto largo, opcional

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Calcular periodo automáticamente si no se proporciona
        if not self.periodo:
            self.periodo = self._calcular_periodo()
        # Setear fecha_prestamo a hoy si no se proporciona
        if not self.fecha_prestamo:
            self.fecha_prestamo = datetime.now().date()

    def _calcular_periodo(self):
        hoy = datetime.now()
        year = hoy.year
        month = hoy.month
        if 1 <= month <= 4:
            return f"Enero - Abril {year}"
        elif 5 <= month <= 8:
            return f"Mayo - Agosto {year}"
        else:
            return f"Septiembre - Diciembre {year}"

    def to_dict(self):
        # Lógica para mostrar "Estadia" si cuatrimestre es 6 o 11
        cuatrimestre_display = "Estadia" if self.cuatrimestre in [6, 11] else str(self.cuatrimestre)
        
        return {
            'id': self.id,
            'alumno': self.alumno,
            'cuatrimestre': self.cuatrimestre,
            'cuatrimestre_display': cuatrimestre_display,  # Nuevo: para frontend
            'grupo': self.grupo,
            'tutor': self.tutor,
            'celular': self.celular,
            'matricula': self.matricula,
            'numero_casillero': self.numero_casillero,
            'periodo': self.periodo,
            'pagado': self.pagado,
            'en_uso': self.en_uso,
            'fecha_prestamo': self.fecha_prestamo.isoformat() if self.fecha_prestamo else None,
            'foto_credencial': self.foto_credencial,
            'foto_casillero': self.foto_casillero,
            'notas': self.notas  # ← Incluido en la respuesta JSON
        }


# Modelo de bitacora

class Bitacora(db.Model):
    __tablename__ = 'bitacora'

    id_bitacora = db.Column(db.Integer, primary_key=True)
    operacion = db.Column(db.Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_registro = db.Column(db.Integer)

    # Valores antiguos (para UPDATE y DELETE)
    alumno_antiguo = db.Column(db.String(100))
    cuatrimestre_antiguo = db.Column(db.Integer)
    grupo_antiguo = db.Column(db.String(1))
    tutor_antiguo = db.Column(db.String(50))
    celular_antiguo = db.Column(db.String(20))
    matricula_antigua = db.Column(db.String(20))
    numero_casillero_antiguo = db.Column(db.Integer)
    pagado_antiguo = db.Column(db.String(10))
    en_uso_antiguo = db.Column(db.String(10))
    fecha_prestamo_antigua = db.Column(db.Date)

    # Valores nuevos (para INSERT y UPDATE)
    alumno_nuevo = db.Column(db.String(100))
    cuatrimestre_nuevo = db.Column(db.Integer)
    grupo_nuevo = db.Column(db.String(1))
    tutor_nuevo = db.Column(db.String(50))
    celular_nuevo = db.Column(db.String(20))
    matricula_nueva = db.Column(db.String(20))
    numero_casillero_nuevo = db.Column(db.Integer)
    pagado_nuevo = db.Column(db.String(10))
    en_uso_nuevo = db.Column(db.String(10))
    fecha_prestamo_nueva = db.Column(db.Date)

    def to_dict(self):
        return {
            'id_bitacora': self.id_bitacora,
            'operacion': self.operacion,
            'usuario': self.usuario,
            'fecha_hora': self.fecha_hora.isoformat(),
            'id_registro': self.id_registro,
            'alumno_antiguo': self.alumno_antiguo,
            'cuatrimestre_antiguo': self.cuatrimestre_antiguo,
            'grupo_antiguo': self.grupo_antiguo,
            'alumno_nuevo': self.alumno_nuevo,
            'cuatrimestre_nuevo': self.cuatrimestre_nuevo,
            'grupo_nuevo': self.grupo_nuevo,
            # ... (puedes agregar los demás campos si quieres verlos en JSON)
        }
    


# app/models.py (agregar al final)
class Horario(db.Model):
    __tablename__ = 'horarios'

    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(20), nullable=False)  # Lunes, Martes, etc.
    materia = db.Column(db.String(100), nullable=False)
    docente = db.Column(db.String(100), nullable=False)
    grupo = db.Column(db.String(20), nullable=False)
    laboratorio = db.Column(db.String(50), nullable=False)
    duracion = db.Column(db.String(20))
    horaInicio = db.Column(db.String(10), nullable=False)  # "13:30"
    horaFin = db.Column(db.String(10), nullable=False)     # "15:30"
    responsable_cierre = db.Column(db.String(100))
    programas = db.Column(db.Text)  # JSON string: '["Clase Teórica"]'

    # NUEVOS CAMPOS
    logo_carrera = db.Column(db.String(255))  # ej: "/logos/mi.png"
    logo_area = db.Column(db.String(255))     # ej: "/logos/automatizacion.png"

    def to_dict(self):
        return {
            'id': self.id,
            'dia': self.dia,
            'materia': self.materia,
            'docente': self.docente,
            'grupo': self.grupo,
            'laboratorio': self.laboratorio,
            'duracion': self.duracion,
            'horaInicio': self.horaInicio,
            'horaFin': self.horaFin,
            'responsableCierre': self.responsable_cierre,
            'programas': json.loads(self.programas) if self.programas else [],
            'logo_carrera': self.logo_carrera,
            'logo_area': self.logo_area
        }