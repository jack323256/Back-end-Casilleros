from flask import request
from flask_restx import Namespace, Resource, fields
from datetime import datetime

from app import db
from app.manto.models import (
    TarjetaPrestamo,
    TarjetaMaterial,
    SesionClase,
    Inventario,
    BitacoraManto
)

ns = Namespace(
    'manto/tarjetas',
    description='Tarjetas dinámicas de préstamo'
)

tarjeta_model = ns.model('Tarjeta', {
    'sesion_id': fields.Integer(description='ID de la sesión de clase (opcional para tarjetas remediales, enviar null o omitir)'),
    'responsable_actual': fields.String(required=True, description='Nombre completo del alumno'),
    'ubicacion_trabajo': fields.String(required=True, description='Nombre del laboratorio o ubicación (ej: "Lab de Automatización")')
})

cambio_responsable_model = ns.model('CambioResponsable', {
    'responsable_actual': fields.String(required=True)
})


# =========================
# CREAR TARJETA (clase o remedial)
# =========================
@ns.route('')
class TarjetaList(Resource):

    @ns.expect(tarjeta_model)
    def post(self):
        """Crear tarjeta de préstamo (para clase activa o remedial)"""
        data = request.json

        if not data.get('responsable_actual') or not data.get('ubicacion_trabajo'):
            return {'error': 'responsable_actual y ubicacion_trabajo son obligatorios'}, 400

        sesion_id = data.get('sesion_id')

        # Validar sesión solo si se proporciona sesion_id
        if sesion_id is not None:
            sesion = SesionClase.query.get_or_404(sesion_id)
            if sesion.estatus != 'activa':
                return {'error': 'La sesión no está activa'}, 400

        tarjeta = TarjetaPrestamo(
            sesion_id=sesion_id,  # Puede ser None para remediales
            responsable_actual=data['responsable_actual'],
            ubicacion_trabajo=data['ubicacion_trabajo']
        )

        db.session.add(tarjeta)
        db.session.commit()

        tipo = 'de clase' if sesion_id else 'remedial'
        db.session.add(BitacoraManto(
            tabla='tarjetas_prestamo',
            registro_id=tarjeta.id,
            accion='INSERT',
            descripcion=f'Tarjeta {tipo} creada para {data["responsable_actual"]}'
        ))
        db.session.commit()

        return {
            'id': tarjeta.id,
            'mensaje': f'Tarjeta {tipo} creada exitosamente'
        }, 201

    def get(self):
        """Listar todas las tarjetas activas (para frontend unificado)"""
        tarjetas = TarjetaPrestamo.query.filter_by(estatus='activa').all()

        return [{
            'id': t.id,
            'responsable_actual': t.responsable_actual,
            'ubicacion_trabajo': t.ubicacion_trabajo,
            'sesion_id': t.sesion_id,
            'materiales': len(t.materiales)
        } for t in tarjetas], 200


# =========================
# LISTAR TARJETAS POR SESIÓN (mantener para compatibilidad)
# =========================
@ns.route('/sesion/<int:sesion_id>')
class TarjetasPorSesion(Resource):
    def get(self, sesion_id):
        tarjetas = TarjetaPrestamo.query.filter_by(
            sesion_id=sesion_id,
            estatus='activa'
        ).all()

        return [{
            'id': t.id,
            'responsable_actual': t.responsable_actual,
            'ubicacion_trabajo': t.ubicacion_trabajo,
            'materiales': len(t.materiales)
        } for t in tarjetas], 200


# =========================
# CAMBIAR RESPONSABLE
# =========================
@ns.route('/<int:id>/responsable')
class CambioResponsable(Resource):
    @ns.expect(cambio_responsable_model)
    def put(self, id):
        tarjeta = TarjetaPrestamo.query.get_or_404(id)
        data = request.json

        tarjeta.responsable_actual = data['responsable_actual']
        db.session.commit()

        db.session.add(BitacoraManto(
            tabla='tarjetas_prestamo',
            registro_id=tarjeta.id,
            accion='UPDATE',
            descripcion=f'Cambio de responsable a {data["responsable_actual"]}'
        ))
        db.session.commit()

        return {'mensaje': 'Responsable actualizado'}, 200


# =========================
# CERRAR TARJETA
# =========================
@ns.route('/<int:id>/cerrar')
class CerrarTarjeta(Resource):
    def put(self, id):
        tarjeta = TarjetaPrestamo.query.get_or_404(id)

        pendientes = TarjetaMaterial.query.filter_by(
            tarjeta_id=id,
            devuelto=False
        ).count()

        if pendientes > 0:
            return {'error': 'Hay material pendiente de devolución'}, 400

        tarjeta.estatus = 'completa'
        db.session.commit()

        db.session.add(BitacoraManto(
            tabla='tarjetas_prestamo',
            registro_id=tarjeta.id,
            accion='UPDATE',
            descripcion='Tarjeta cerrada (todos los materiales devueltos)'
        ))
        db.session.commit()

        return {'mensaje': 'Tarjeta cerrada correctamente'}, 200