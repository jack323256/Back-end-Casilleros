from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from datetime import datetime

from app import db
from app.manto.models import Inventario, BitacoraManto
from werkzeug.utils import secure_filename
import os

ns = Namespace(
    'manto/inventario',
    description='Gestión de inventario MANTO'
)

# =========================
# Swagger Model (agregamos imagen_url de solo lectura)
# =========================
inventario_model = ns.model('Inventario', {
    'codigo': fields.String(required=True, description='Código único del material'),
    'nombre': fields.String(required=True),
    'descripcion': fields.String,
    'categoria': fields.String,
    'cantidad_total': fields.Integer(required=True),
    'ubicacion': fields.String,
    'activo': fields.Boolean,
    'imagen_url': fields.String(readonly=True, description='URL de la foto del item')
})

# Función para validar extensiones (reutilizamos la de config)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# =========================
# /manto/inventario
# =========================
@ns.route('')
class InventarioList(Resource):

    def get(self):
        """Listar inventario"""
        inventario = Inventario.query.all()
        return [i.to_dict() for i in inventario], 200

    @ns.expect(inventario_model)
    def post(self):
        """Crear nuevo item de inventario"""
        data = request.form  # Para manejar multipart (texto + archivo)
        file = request.files.get('imagen')  # El frontend envía el archivo con name="imagen"

        # ---------- Validaciones ----------
        if Inventario.query.filter_by(codigo=data['codigo']).first():
            return {'error': 'El código ya existe'}, 409

        if int(data['cantidad_total']) < 0:
            return {'error': 'La cantidad no puede ser negativa'}, 400

        # ---------- Crear item ----------
        item = Inventario(
            codigo=data['codigo'],
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            categoria=data.get('categoria'),
            cantidad_total=int(data['cantidad_total']),
            cantidad_disponible=int(data['cantidad_total']),
            ubicacion=data.get('ubicacion'),
            activo=data.get('activo', True) in ['true', True, 'True']
        )

        # ---------- Manejo de imagen ----------
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            item.imagen = filename

        db.session.add(item)
        db.session.commit()

        # ---------- Bitácora ----------
        db.session.add(BitacoraManto(
            tabla='inventario',
            registro_id=item.id,
            accion='INSERT',
            descripcion=f'Alta de inventario: {item.nombre}'
        ))
        db.session.commit()

        return item.to_dict(), 201


# =========================
# /manto/inventario/<id>
# =========================
@ns.route('/<int:id>')
class InventarioResource(Resource):

    def get(self, id):
        """Obtener item por ID"""
        item = Inventario.query.get_or_404(id)
        return item.to_dict(), 200

    @ns.expect(inventario_model)
    def put(self, id):
        """Actualizar item de inventario"""
        item = Inventario.query.get_or_404(id)
        data = request.form
        file = request.files.get('imagen')

        old_activo = item.activo  # Guardamos el estado anterior

        # ---------- Campos simples ----------
        if 'codigo' in data:
            item.codigo = data['codigo']
        if 'nombre' in data:
            item.nombre = data['nombre']
        if 'descripcion' in data:
            item.descripcion = data['descripcion']
        if 'categoria' in data:
            item.categoria = data['categoria']
        if 'ubicacion' in data:
            item.ubicacion = data['ubicacion']

        # ---------- Estado activo ----------
        if 'activo' in data:
            nuevo_activo = data['activo'] in ['true', True, 'True']
            if nuevo_activo != old_activo:
                # Si pasa de Inactivo a Activo → sumar al disponible
                if nuevo_activo:
                    item.cantidad_disponible += item.cantidad_total
                # Si pasa de Activo a Inactivo → restar del disponible
                else:
                    item.cantidad_disponible -= item.cantidad_total

                # Evitar números negativos
                if item.cantidad_disponible < 0:
                    item.cantidad_disponible = 0

                item.activo = nuevo_activo

        # ---------- Cantidades ----------
        if 'cantidad_total' in data:
            nueva_total = int(data['cantidad_total'])
            if nueva_total < 0:
                return {'error': 'Cantidad inválida'}, 400

            diferencia = nueva_total - item.cantidad_total
            # Solo ajustamos disponible si el item está activo
            if item.activo:
                item.cantidad_disponible += diferencia
                if item.cantidad_disponible < 0:
                    item.cantidad_disponible = 0

            item.cantidad_total = nueva_total

        # ---------- Manejo de nueva imagen ----------
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            item.imagen = filename

        db.session.commit()

        # ---------- Bitácora ----------
        descripcion = f'Actualización de inventario: {item.nombre}'
        if 'activo' in data and nuevo_activo != old_activo:
            descripcion += f' | Estado cambiado a {"Activo" if nuevo_activo else "Inactivo"}'

        db.session.add(BitacoraManto(
            tabla='inventario',
            registro_id=item.id,
            accion='UPDATE',
            descripcion=descripcion
        ))
        db.session.commit()

        return item.to_dict(), 200

    def delete(self, id):
        """Borrado lógico del inventario"""
        item = Inventario.query.get_or_404(id)
        item.activo = False
        db.session.commit()

        db.session.add(BitacoraManto(
            tabla='inventario',
            registro_id=item.id,
            accion='DELETE',
            descripcion=f'Baja lógica de inventario: {item.nombre}'
        ))
        db.session.commit()

        return {'message': 'Item desactivado'}, 200