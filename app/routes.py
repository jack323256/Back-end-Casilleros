# routes.py
from flask import request, jsonify, send_from_directory, current_app
from flask_restx import Namespace, Resource, fields
from .models import Assignment
from . import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('')
class AssignmentList(Resource):
    @bp.marshal_list_with(assignment_model)
    def get(self):
        assignments = Assignment.query.all()
        return [a.to_dict() for a in assignments]

    @bp.expect(assignment_input_model, validate=False)
    def post(self):
        data = request.form
        required_fields = ['alumno', 'cuatrimestre', 'grupo', 'tutor', 'celular', 'matricula', 'numero_casillero', 'periodo']
        for field in required_fields:
            if field not in data or not data[field].strip():
                bp.abort(400, f'El campo {field} es obligatorio')

        try:
            cuatrimestre = int(data['cuatrimestre'])
            if not (1 <= cuatrimestre <= 11):
                bp.abort(400, 'El cuatrimestre debe estar entre 1 y 11')
        except ValueError:
            bp.abort(400, 'El cuatrimestre debe ser un número entero')

        grupo = data['grupo'].strip().upper()
        if grupo not in ['A', 'B', 'C', 'D', 'E']:
            bp.abort(400, 'El grupo debe ser A, B, C, D o E')

        try:
            numero_casillero = int(data['numero_casillero'])
        except ValueError:
            bp.abort(400, 'El número de casillero debe ser un número entero')

        pagado = data.get('pagado', '').strip()
        en_uso = data.get('en_uso', '').strip()

        fecha_prestamo = None
        if data.get('fecha_prestamo'):
            try:
                fecha_prestamo = datetime.strptime(data['fecha_prestamo'], '%Y-%m-%d').date()
            except ValueError:
                bp.abort(400, 'Formato de fecha inválido (debe ser YYYY-MM-DD)')

        # Creación del nuevo registro con el campo periodo incluido
        assignment = Assignment(
            alumno=data['alumno'].strip(),
            cuatrimestre=cuatrimestre,
            grupo=grupo,
            tutor=data['tutor'].strip(),
            celular=data['celular'].strip(),
            matricula=data['matricula'].strip(),
            numero_casillero=numero_casillero,
            periodo=data['periodo'].strip(),  # ← AÑADIDO
            pagado=pagado,
            en_uso=en_uso,
            fecha_prestamo=fecha_prestamo,
            notas=data.get('notas', '').strip()
        )

        # Manejo de fotos
        for field in ['foto_credencial', 'foto_casillero']:
            if field in request.files:
                file = request.files[field]
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    setattr(assignment, field, filename)

        db.session.add(assignment)
        db.session.commit()
        return assignment.to_dict(), 201


@bp.route('/<int:id>')
@bp.param('id', 'ID de la asignación')
class AssignmentResource(Resource):
    @bp.marshal_with(assignment_model)
    def get(self, id):
        assignment = Assignment.query.get_or_404(id)
        return assignment.to_dict()

    @bp.expect(assignment_input_model, validate=False)
    @bp.marshal_with(assignment_model)
    def put(self, id):
        assignment = Assignment.query.get_or_404(id)
        data = request.form

        if 'alumno' in data:
            assignment.alumno = data['alumno'].strip()
        if 'cuatrimestre' in data:
            try:
                cuatrimestre = int(data['cuatrimestre'])
                if not (1 <= cuatrimestre <= 11):
                    bp.abort(400, 'El cuatrimestre debe estar entre 1 y 11')
                assignment.cuatrimestre = cuatrimestre
            except ValueError:
                bp.abort(400, 'El cuatrimestre debe ser un número entero')
        if 'grupo' in data:
            grupo = data['grupo'].strip().upper()
            if grupo not in ['A', 'B', 'C', 'D', 'E']:
                bp.abort(400, 'El grupo debe ser A, B, C, D o E')
            assignment.grupo = grupo
        if 'tutor' in data:
            assignment.tutor = data['tutor'].strip()
        if 'celular' in data:
            assignment.celular = data['celular'].strip()
        if 'matricula' in data:
            assignment.matricula = data['matricula'].strip()
        if 'numero_casillero' in data:
            try:
                assignment.numero_casillero = int(data['numero_casillero'])
            except ValueError:
                bp.abort(400, 'El número de casillero debe ser un número entero')
        if 'periodo' in data:
            assignment.periodo = data['periodo'].strip()  # ← AÑADIDO: actualización del periodo
        if 'pagado' in data:
            assignment.pagado = data['pagado'].strip()
        if 'en_uso' in data:
            assignment.en_uso = data['en_uso'].strip()
        if 'fecha_prestamo' in data:
            if data['fecha_prestamo'].strip() == '':
                assignment.fecha_prestamo = None
            else:
                try:
                    assignment.fecha_prestamo = datetime.strptime(data['fecha_prestamo'], '%Y-%m-%d').date()
                except ValueError:
                    bp.abort(400, 'Formato de fecha inválido (YYYY-MM-DD)')
        if 'notas' in data:
            assignment.notas = data['notas'].strip()

        # Manejo de nuevas fotos (solo si se sube una)
        for field in ['foto_credencial', 'foto_casillero']:
            if field in request.files:
                file = request.files[field]
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    setattr(assignment, field, filename)

        db.session.commit()
        return assignment.to_dict()

    def delete(self, id):
        assignment = Assignment.query.get_or_404(id)
        db.session.delete(assignment)
        db.session.commit()
        return '', 204