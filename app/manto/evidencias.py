import os
import uuid
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from .models import db, Mantenimiento
from datetime import datetime

ns = Namespace(
    'manto/evidencias',
    description='Gestión de evidencias de mantenimiento industrial'
)

# Ya tenemos los nombres exactos, así que el modelo es mucho más simple y seguro
evidencia_model = ns.model('EvidenciaMantenimiento', {
    'id': fields.Integer,
    'titulo': fields.String,
    'laboratorio': fields.String,
    'especialista': fields.String,
    'area': fields.String,
    'notas': fields.String, # <--- NUEVO
    'fecha': fields.String(attribute=lambda x: x.fecha_registro.strftime('%d/%m/%Y %H:%M') if x.fecha_registro else 'Sin fecha'),
    'fotos': fields.Raw(attribute=lambda x: {
        'actual': x.foto_actual,
        'proceso': x.foto_proceso,
        'completado': x.foto_completado
    })
})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@ns.route('')
class EvidenciasList(Resource):
    @ns.marshal_list_with(evidencia_model)
    def get(self):
        """Lista todas las evidencias"""
        return Mantenimiento.query.order_by(Mantenimiento.id.desc()).all()

    def post(self):
        """Crea una nueva evidencia"""
        try:
            # Creación con los nombres EXACTOS de tu base de datos
            nuevo = Mantenimiento(
                titulo=request.form.get('titulo'),
                laboratorio=request.form.get('laboratorio'),
                especialista=request.form.get('especialista', 'Carlos Iván Crespo Alvarado'),
                area=request.form.get('area', 'Mantenimiento Industrial'),
                notas=request.form.get('notas', ''), # <--- NUEVO
                fecha_registro=datetime.now()
            )

            # Mapeo exacto para las fotos
            mapping = {
                'actual': 'foto_actual',
                'proceso': 'foto_proceso',
                'completado': 'foto_completado'
            }

            for key_vue, col_db in mapping.items():
                file = request.files.get(key_vue)
                if file and file.filename != '' and allowed_file(file.filename):
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    nombre = f"manto_{uuid.uuid4().hex[:8]}_{key_vue}.{ext}"
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nombre))
                    setattr(nuevo, col_db, nombre)

            db.session.add(nuevo)
            db.session.commit()
            return {"message": "Guardado con éxito"}, 201

        except Exception as e:
            db.session.rollback()
            print(f"ERROR EN POST: {str(e)}")
            return {"error": str(e)}, 500

@ns.route('/<int:id>')
class EvidenciaItem(Resource):
    def delete(self, id):
        """Borra registro y archivos físicos"""
        try:
            ev = Mantenimiento.query.get_or_404(id)
            
            # Borrar las fotos físicas de la carpeta uploads
            for col in ['foto_actual', 'foto_proceso', 'foto_completado']:
                archivo = getattr(ev, col)
                if archivo:
                    ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], archivo)
                    if os.path.exists(ruta): 
                        os.remove(ruta)
            
            db.session.delete(ev)
            db.session.commit()
            return {"message": "Eliminado correctamente"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def put(self, id):
        """Actualiza un registro"""
        try:
            ev = Mantenimiento.query.get_or_404(id)
            ev.titulo = request.form.get('titulo', ev.titulo)
            ev.laboratorio = request.form.get('laboratorio', ev.laboratorio)
            ev.especialista = request.form.get('especialista', ev.especialista)
            ev.area = request.form.get('area', ev.area)
            ev.notas = request.form.get('notas', ev.notas) # <--- NUEVO

            mapping = {
                'actual': 'foto_actual',
                'proceso': 'foto_proceso',
                'completado': 'foto_completado'
            }

            for key_vue, col_db in mapping.items():
                file = request.files.get(key_vue)
                if file and file.filename != '' and allowed_file(file.filename):
                    # Borrar archivo viejo
                    viejo = getattr(ev, col_db)
                    if viejo:
                        ruta_vieja = os.path.join(current_app.config['UPLOAD_FOLDER'], viejo)
                        if os.path.exists(ruta_vieja): 
                            os.remove(ruta_vieja)
                    
                    # Guardar nuevo
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    nombre = f"upd_{uuid.uuid4().hex[:8]}_{key_vue}.{ext}"
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nombre))
                    setattr(ev, col_db, nombre)

            db.session.commit()
            return {"message": "Actualizado correctamente"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500