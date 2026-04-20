from flask import request
from flask_restx import Namespace, Resource, fields
from datetime import datetime

from app import db
from app.manto.models import SesionClase, BitacoraManto


ns = Namespace(
    'manto/sesiones',
    description='Gestión de sesiones de clase'
)

# =========================
# Swagger Model
# =========================
sesion_model = ns.model('SesionClase', {
    'docente': fields.String(required=True),
    'materia': fields.String,
    'laboratorio': fields.String,
    'grupo': fields.String
})


# =========================
# /manto/sesiones
# =========================
@ns.route('')
class SesionList(Resource):

    def get(self):
        """Listar sesiones activas"""
        sesiones = SesionClase.query.filter_by(estatus='activa').all()
        # ← CAMBIO AQUÍ: usar to_dict() en lugar de __dict__
        return [s.to_dict() for s in sesiones], 200

    @ns.expect(sesion_model)
    def post(self):
        """Abrir nueva sesión"""
        data = request.json

        sesion = SesionClase(
            docente=data['docente'],
            materia=data.get('materia'),
            laboratorio=data.get('laboratorio'),
            grupo=data.get('grupo')
        )

        db.session.add(sesion)
        db.session.commit()

        # Bitácora
        log = BitacoraManto(
            tabla='sesiones_clase',
            registro_id=sesion.id,
            accion='INSERT',
            descripcion=f'Sesión iniciada por {sesion.docente}'
        )
        db.session.add(log)
        db.session.commit()

        # ← Mejor devolver to_dict() para consistencia
        return sesion.to_dict(), 201

# =========================
# /manto/sesiones/<id>/cerrar
# =========================
@ns.route('/<int:id>/cerrar')
class SesionCerrar(Resource):

    def put(self, id):
        """Cerrar sesión"""
        sesion = SesionClase.query.get_or_404(id)

        if sesion.estatus == 'cerrada':
            return {'error': 'La sesión ya está cerrada'}, 400

        sesion.estatus = 'cerrada'
        sesion.fecha_fin = datetime.utcnow()

        db.session.commit()

        # Bitácora
        log = BitacoraManto(
            tabla='sesiones_clase',
            registro_id=sesion.id,
            accion='UPDATE',
            descripcion='Sesión cerrada'
        )
        db.session.add(log)
        db.session.commit()

        return {'mensaje': 'Sesión cerrada correctamente'}, 200
