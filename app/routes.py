# routes.py
from flask import request, jsonify, send_from_directory, current_app
from flask_restx import Namespace, Resource, fields
from .models import Assignment
from . import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import traceback  # <- NUEVO: Para rastrear errores ocultos

# Importación para el controlador API de Imágenes 
import cloudinary
import cloudinary.uploader
#-----------------------------

# === CONFIGURACIÓN DE CLOUDINARY ===
cloudinary.config( 
  cloud_name = "jack32", 
  api_key = "921913451556512", 
  api_secret = "QOteKxbVL_vtEzdimM1QSy8zUp0",
  secure = True
)

def subir_a_nube(file):
    try:
        print(f"Subiendo {file.filename} a Cloudinary...", flush=True)
        # Cloudinary hace toda la magia con esta simple línea
        respuesta = cloudinary.uploader.upload(file)
        
        print("¡Éxito! Cloudinary aceptó la foto.", flush=True)
        return respuesta['secure_url'] # Nos devuelve el link seguro (https)
        
    except Exception as e:
        print(f"🚨 ERROR EN CLOUDINARY: {str(e)}", flush=True)
        return None
# ==============================


# Namespace para las operaciones REST
bp = Namespace('assignments', description='Operaciones sobre asignaciones de casilleros')

# Modelos para Swagger
assignment_model = bp.model('Assignment', {
    'id': fields.Integer(readonly=True),
    'alumno': fields.String(required=True),
    'cuatrimestre': fields.Integer(required=True, min=1, max=11),
    'cuatrimestre_display': fields.String(),
    'grupo': fields.String(required=True, enum=['A', 'B', 'C', 'D', 'E']),
    'tutor': fields.String(required=True),
    'celular': fields.String(required=True),
    'matricula': fields.String(required=True),
    'numero_casillero': fields.Integer(required=True),
    'periodo': fields.String(description='Periodo académico, ej: Enero - Abril 2026'),
    'pagado': fields.String(),
    'en_uso': fields.String(),
    'fecha_prestamo': fields.Date(),
    'foto_credencial': fields.String(),
    'foto_casillero': fields.String(),
    'notas': fields.String(description='Observaciones o detalles del casillero (daños, comentarios, etc.)'),
})

assignment_input_model = bp.model('AssignmentInput', {
    'alumno': fields.String(required=True),
    'cuatrimestre': fields.Integer(required=True, min=1, max=11),
    'grupo': fields.String(required=True, enum=['A', 'B', 'C', 'D', 'E']),
    'tutor': fields.String(required=True),
    'celular': fields.String(required=True),
    'matricula': fields.String(required=True),
    'numero_casillero': fields.Integer(required=True),
    'periodo': fields.String(description='Periodo académico (obligatorio en el frontend)'),
    'pagado': fields.String(),
    'en_uso': fields.String(),
    'fecha_prestamo': fields.Date(required=False),
    'notas': fields.String(description='Observaciones o detalles del casillero'),
})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', set())

@bp.route('')
class AssignmentList(Resource):
    @bp.marshal_list_with(assignment_model)
    def get(self):
        assignments = Assignment.query.all()
        return [a.to_dict() for a in assignments]

    @bp.expect(assignment_input_model, validate=False)
    def post(self):
        try:
            data = request.form
            required_fields = ['alumno', 'cuatrimestre', 'grupo', 'tutor', 'celular', 'matricula', 'numero_casillero', 'periodo']
            for field in required_fields:
                if field not in data or not data[field].strip():
                    bp.abort(400, f'El campo {field} es obligatorio')

            cuatrimestre = int(data['cuatrimestre'])
            grupo = data['grupo'].strip().upper()
            numero_casillero = int(data['numero_casillero'])
            pagado = data.get('pagado', '').strip()
            en_uso = data.get('en_uso', '').strip()

            fecha_prestamo = None
            if data.get('fecha_prestamo'):
                fecha_prestamo = datetime.strptime(data['fecha_prestamo'], '%Y-%m-%d').date()

            assignment = Assignment(
                alumno=data['alumno'].strip(),
                cuatrimestre=cuatrimestre,
                grupo=grupo,
                tutor=data['tutor'].strip(),
                celular=data['celular'].strip(),
                matricula=data['matricula'].strip(),
                numero_casillero=numero_casillero,
                periodo=data['periodo'].strip(),
                pagado=pagado,
                en_uso=en_uso,
                fecha_prestamo=fecha_prestamo,
                notas=data.get('notas', '').strip()
            )

            for field in ['foto_credencial', 'foto_casillero']:
                if field in request.files:
                    file = request.files[field]
                    if file and file.filename != '' and allowed_file(file.filename):
                        link_imagen = subir_a_nube(file)
                        if link_imagen:
                            setattr(assignment, field, link_imagen)
                        else:
                            bp.abort(500, f'Error al subir la imagen {field} a ImgBB.')

            db.session.add(assignment)
            db.session.commit()
            return assignment.to_dict(), 201
            
        except Exception as e:
            print("🚨 ERROR FATAL EN POST 🚨", flush=True)
            traceback.print_exc()
            return {'message': f'Error interno: {str(e)}'}, 500


@bp.route('/<int:id>')
@bp.param('id', 'ID de la asignación')
class AssignmentResource(Resource):
    @bp.marshal_with(assignment_model)
    def get(self, id):
        assignment = Assignment.query.get_or_404(id)
        return assignment.to_dict()

    @bp.expect(assignment_input_model, validate=False)
    def put(self, id):
        try:
            print(f"--- INICIANDO PUT PARA ID {id} ---", flush=True)
            assignment = Assignment.query.get_or_404(id)
            data = request.form
            
            print(f"Archivos recibidos: {request.files}", flush=True)

            if 'alumno' in data: assignment.alumno = data['alumno'].strip()
            if 'cuatrimestre' in data: assignment.cuatrimestre = int(data['cuatrimestre'])
            if 'grupo' in data: assignment.grupo = data['grupo'].strip().upper()
            if 'tutor' in data: assignment.tutor = data['tutor'].strip()
            if 'celular' in data: assignment.celular = data['celular'].strip()
            if 'matricula' in data: assignment.matricula = data['matricula'].strip()
            if 'numero_casillero' in data: assignment.numero_casillero = int(data['numero_casillero'])
            if 'periodo' in data: assignment.periodo = data['periodo'].strip()
            if 'pagado' in data: assignment.pagado = data['pagado'].strip()
            if 'en_uso' in data: assignment.en_uso = data['en_uso'].strip()
            if 'fecha_prestamo' in data:
                if data['fecha_prestamo'].strip() == '':
                    assignment.fecha_prestamo = None
                else:
                    assignment.fecha_prestamo = datetime.strptime(data['fecha_prestamo'], '%Y-%m-%d').date()
            if 'notas' in data: assignment.notas = data['notas'].strip()

            for field in ['foto_credencial', 'foto_casillero']:
                if field in request.files:
                    file = request.files[field]
                    if file and file.filename != '':
                        print(f"Procesando {field}: {file.filename}", flush=True)
                        if allowed_file(file.filename):
                            link_imagen = subir_a_nube(file)
                            if link_imagen:
                                setattr(assignment, field, link_imagen)
                            else:
                                return {'message': f'Error al subir la imagen {field} a ImgBB.'}, 500
                        else:
                            return {'message': 'Extensión no permitida.'}, 400

            db.session.commit()
            print("--- PUT EXITOSO ---", flush=True)
            return assignment.to_dict(), 200

        except Exception as e:
            print("🚨 ERROR FATAL EN PUT 🚨", flush=True)
            traceback.print_exc()
            return {'message': f'Error interno: {str(e)}'}, 500

    def delete(self, id):
        assignment = Assignment.query.get_or_404(id)
        db.session.delete(assignment)
        db.session.commit()
        return '', 204
