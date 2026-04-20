from flask import request
from flask_restx import Namespace, Resource, fields
from app.manto.models import BitacoraManto


ns = Namespace(
    'manto/bitacora',
    description='Consulta de bitácora MANTO (solo lectura)'
)

# =========================
# Swagger Model
# =========================
bitacora_model = ns.model('BitacoraManto', {
    'id': fields.Integer,
    'tabla': fields.String,
    'registro_id': fields.Integer,
    'accion': fields.String,
    'usuario': fields.String,
    'fecha': fields.DateTime,
    'descripcion': fields.String
})


# =========================
# /manto/bitacora
# =========================
@ns.route('')
class BitacoraList(Resource):

    @ns.marshal_list_with(bitacora_model)
    def get(self):
        """
        Consulta de bitácora
        Filtros opcionales:
        - tabla
        - registro_id
        - accion
        - usuario
        """
        query = BitacoraManto.query

        tabla = request.args.get('tabla')
        registro_id = request.args.get('registro_id')
        accion = request.args.get('accion')
        usuario = request.args.get('usuario')

        if tabla:
            query = query.filter(BitacoraManto.tabla == tabla)

        if registro_id:
            query = query.filter(BitacoraManto.registro_id == registro_id)

        if accion:
            query = query.filter(BitacoraManto.accion == accion)

        if usuario:
            query = query.filter(BitacoraManto.usuario == usuario)

        return query.order_by(BitacoraManto.fecha.desc()).all(), 200
