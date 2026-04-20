from flask import request
from flask_restx import Namespace, Resource, fields
from datetime import datetime

from app import db
from app.manto.models import (
    TarjetaPrestamo,
    TarjetaMaterial,
    Inventario,
    BitacoraManto
)

ns = Namespace(
    'manto/tarjeta-material',
    description='Material dentro de tarjeta'
)

material_model = ns.model('TarjetaMaterial', {
    'inventario_id': fields.Integer(required=True),
    'cantidad': fields.Integer(required=True),
    'estado_salida': fields.String(
        enum=['bueno', 'regular', 'malo'],
        required=True
    )
})



# POST

@ns.route('/<int:tarjeta_id>')
class AgregarMaterial(Resource):

    @ns.expect(material_model)
    def post(self, tarjeta_id):
        data = request.json

        tarjeta = TarjetaPrestamo.query.get_or_404(tarjeta_id)
        inventario = Inventario.query.get_or_404(data['inventario_id'])

        if inventario.cantidad_disponible < data['cantidad']:
            return {'error': 'Inventario insuficiente'}, 400

        # Descontar inventario
        inventario.cantidad_disponible -= data['cantidad']

        material = TarjetaMaterial(
            tarjeta_id=tarjeta.id,
            inventario_id=inventario.id,
            cantidad=data['cantidad'],
            estado_salida=data['estado_salida']
        )

        db.session.add(material)
        db.session.commit()

        db.session.add(BitacoraManto(
            tabla='tarjeta_material',
            registro_id=material.id,
            accion='INSERT',
            descripcion=f'Salida de {data["cantidad"]} {inventario.nombre}'
        ))
        db.session.commit()

        return {'mensaje': 'Material agregado a tarjeta'}, 201


# PUT

@ns.route('/<int:id>/devolver')
class DevolverMaterial(Resource):

    @ns.expect(ns.model('Devolucion', {
        'estado_entrada': fields.String(
            enum=['bueno', 'regular', 'malo'],
            required=True
        )
    }))
    def put(self, id):
        material = TarjetaMaterial.query.get_or_404(id)
        inventario = material.inventario

        if material.devuelto:
            return {'error': 'Ya fue devuelto'}, 400

        data = request.json

        material.devuelto = True
        material.estado_entrada = data['estado_entrada']
        material.fecha_entrada = datetime.utcnow()

        # Sumar inventario
        inventario.cantidad_disponible += material.cantidad

        # Registrar anomalía
        if material.estado_salida != material.estado_entrada:
            db.session.add(BitacoraManto(
                tabla='tarjeta_material',
                registro_id=material.id,
                accion='UPDATE',
                descripcion=(
                    f'Daño detectado: '
                    f'{material.estado_salida} → {material.estado_entrada}'
                )
            ))

        db.session.commit()
        return {'mensaje': 'Material devuelto'}, 200


# GET

@ns.route('/tarjeta/<int:tarjeta_id>')
class MaterialesPorTarjeta(Resource):

    def get(self, tarjeta_id):
        materiales = TarjetaMaterial.query.filter_by(
            tarjeta_id=tarjeta_id
        ).all()

        return [{
            'id': m.id,
            'material': m.inventario.nombre,
            'cantidad': m.cantidad,
            'estado_salida': m.estado_salida,
            'estado_entrada': m.estado_entrada,
            'devuelto': m.devuelto
        } for m in materiales], 200




