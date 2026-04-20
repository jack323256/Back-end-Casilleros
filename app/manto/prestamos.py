from flask import request
from flask_restx import Namespace, Resource, fields
from datetime import datetime

from app import db
from app.manto.models import Prestamo, Inventario, BitacoraManto

ns = Namespace(
    'manto/prestamos',
    description='Gestión de préstamos de inventario MANTO'
)

# =========================
# Modelo Swagger (adaptado a tu modelo real de Prestamo)
# =========================
prestamo_model = ns.model('Prestamo', {
    'inventario_id': fields.Integer(required=True, description='ID del item de inventario'),
    'tipo_prestamo': fields.String(required=True, enum=['docente', 'alumno', 'externo'], default='alumno'),
    'solicitante': fields.String(required=True, description='Nombre del alumno o docente'),
    'referencia': fields.String(description='Matrícula, motivo o referencia (ej: práctica remedial)'),
    'observaciones': fields.String(description='Notas adicionales'),
})

# =========================
# /manto/prestamos
# =========================
@ns.route('')
class PrestamoList(Resource):

    def get(self):
        """Listar préstamos (opcional: ?estatus=activo)"""
        estatus = request.args.get('estatus')
        query = Prestamo.query
        if estatus == 'activo':
            query = query.filter_by(estatus='activo')
        prestamos = query.all()
        return [p.to_dict() for p in prestamos], 200

    @ns.expect(prestamo_model)
    def post(self):
        """Crear un nuevo préstamo"""
        data = request.json

        required_fields = ['inventario_id', 'solicitante', 'laboratorio']
        for field in required_fields:
            if field not in data:
                return {'error': f'El campo {field} es obligatorio'}, 400

        inventario = Inventario.query.get_or_404(data['inventario_id'])

        if not inventario.activo:
            return {'error': 'El item está dado de baja'}, 400

        if inventario.cantidad_disponible <= 0:
            return {'error': 'No hay unidades disponibles de este item'}, 400

        # Restar del stock
        inventario.cantidad_disponible -= 1

        prestamo = Prestamo(
            inventario_id=inventario.id,
            tipo_prestamo=data.get('tipo_prestamo', 'alumno'),
            solicitante=data['solicitante'],
            referencia=data.get('referencia', 'Práctica remedial'),
            observaciones=f"Lab: {data['laboratorio']} | {data.get('observaciones', '')}".strip(' | '),
            fecha_prestamo=datetime.utcnow(),
            estatus='activo'
        )

        try:
            db.session.add(prestamo)
            db.session.commit()

            log = BitacoraManto(
                tabla='prestamos',
                registro_id=prestamo.id,
                accion='INSERT',
                descripcion=f'Préstamo en {data["laboratorio"]} a {prestamo.solicitante}: {inventario.nombre}',
                fecha=datetime.utcnow()
            )
            db.session.add(log)
            db.session.commit()

            return prestamo.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            inventario.cantidad_disponible += 1  # Revertir si falla
            return {'error': f'Error al crear préstamo: {str(e)}'}, 500


@ns.route('/<int:id>/devolver')
class PrestamoDevolucion(Resource):
    def put(self, id):
        """Registrar devolución de préstamo"""
        prestamo = Prestamo.query.get_or_404(id)

        if prestamo.estatus != 'activo':
            return {'error': 'El préstamo ya fue devuelto o cancelado'}, 400

        prestamo.estatus = 'devuelto'
        prestamo.fecha_devolucion = datetime.utcnow()

        # Sumar al inventario
        inventario = prestamo.inventario
        if inventario:
            inventario.cantidad_disponible += 1

        try:
            db.session.commit()

            log = BitacoraManto(
                tabla='prestamos',
                registro_id=prestamo.id,
                accion='UPDATE',
                descripcion=f'Devolución de préstamo ID {prestamo.id} - {inventario.nombre}',
                fecha=datetime.utcnow()
            )
            db.session.add(log)
            db.session.commit()

            return {'message': 'Préstamo devuelto correctamente'}, 200
        except Exception as e:
            db.session.rollback()
            if inventario:
                inventario.cantidad_disponible -= 1  # Revertir si falla
            return {'error': str(e)}, 500

# =========================
# (Opcional) Transferencia - solo si usas matrícula
# =========================
# Si no usas el campo alumno_matricula, puedes eliminar esta parte
transferencia_model = ns.model('TransferenciaPrestamo', {
    'nuevo_alumno_matricula': fields.Integer(required=True),
    'observaciones': fields.String
})

@ns.route('/<int:id>/transferir')
class PrestamoTransferencia(Resource):
    @ns.expect(transferencia_model)
    def put(self, id):
        prestamo = Prestamo.query.get_or_404(id)
        data = request.json

        if prestamo.estatus != 'activo':
            return {'error': 'Solo se pueden transferir préstamos activos'}, 400

        # Aquí ajusta según tu modelo real
        # Ejemplo si tuvieras un campo alumno_matricula:
        # prestamo.alumno_matricula = data['nuevo_alumno_matricula']

        prestamo.observaciones = data.get('observaciones', prestamo.observaciones)

        try:
            db.session.commit()
            return {'message': 'Préstamo transferido correctamente'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500