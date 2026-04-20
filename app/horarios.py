# app/routes/horarios.py
from flask_restx import Namespace, Resource, fields
from flask import request
from .models import Horario, db
import json

horarios_namespace = Namespace('horarios', description='Operaciones de horarios de laboratorios')

# Modelo para Swagger
horario_model = horarios_namespace.model('Horario', {
    'dia': fields.String(required=True, description='Día de la semana'),
    'materia': fields.String(required=True),
    'docente': fields.String(required=True),
    'grupo': fields.String(required=True),
    'laboratorio': fields.String(required=True),
    'duracion': fields.String(),
    'horaInicio': fields.String(required=True, example="13:30"),
    'horaFin': fields.String(required=True, example="15:30"),
    'responsable_cierre': fields.String(),
    'programas': fields.List(fields.String, description='Ej: ["Clase Teórica"]'),
    'logo_carrera': fields.String(description='Ruta al logo de la carrera'),
    'logo_area': fields.String(description='Ruta al logo del área/laboratorio')
})

@horarios_namespace.route('')
class HorariosList(Resource):
    @horarios_namespace.doc('list_horarios')
    def get(self):
        """Lista todos los horarios"""
        horarios = Horario.query.all()
        return [h.to_dict() for h in horarios], 200

    @horarios_namespace.doc('create_horario')
    @horarios_namespace.expect(horario_model)
    def post(self):
        """Crear un nuevo horario"""
        data = request.json
        try:
            nuevo = Horario(
                dia=data['dia'],
                materia=data['materia'],
                docente=data['docente'],
                grupo=data['grupo'],
                laboratorio=data['laboratorio'],
                duracion=data.get('duracion'),
                horaInicio=data['horaInicio'],
                horaFin=data['horaFin'],
                responsable_cierre=data.get('responsable_cierre'),
                programas=json.dumps(data.get('programas', [])),
                logo_carrera=data.get('logo_carrera'),
                logo_area=data.get('logo_area')
            )
            db.session.add(nuevo)
            db.session.commit()
            return nuevo.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

@horarios_namespace.route('/<int:id>')
class HorarioResource(Resource):
    @horarios_namespace.doc('get_horario')
    def get(self, id):
        """Obtener un horario por ID"""
        horario = Horario.query.get_or_404(id)
        return horario.to_dict(), 200

    @horarios_namespace.doc('update_horario')
    @horarios_namespace.expect(horario_model)
    def put(self, id):
        """Actualizar un horario"""
        horario = Horario.query.get_or_404(id)
        data = request.json
        try:
            horario.dia = data['dia']
            horario.materia = data['materia']
            horario.docente = data['docente']
            horario.grupo = data['grupo']
            horario.laboratorio = data['laboratorio']
            horario.duracion = data.get('duracion')
            horario.horaInicio = data['horaInicio']
            horario.horaFin = data['horaFin']
            horario.responsable_cierre = data.get('responsable_cierre')
            horario.programas = json.dumps(data.get('programas', []))
            horario.logo_carrera = data.get('logo_carrera')
            horario.logo_area = data.get('logo_area')

            db.session.commit()
            return horario.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @horarios_namespace.doc('delete_horario')
    def delete(self, id):
        """Eliminar un horario"""
        horario = Horario.query.get_or_404(id)
        db.session.delete(horario)
        db.session.commit()
        return {'message': 'Horario eliminado'}, 200