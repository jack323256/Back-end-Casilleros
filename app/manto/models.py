from datetime import datetime
from app import db

# =========================
# INVENTARIO
# =========================
class Inventario(db.Model):
    __bind_key__ = 'manto'
    __tablename__ = 'inventario'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(100))
    cantidad_total = db.Column(db.Integer, nullable=False, default=0)
    cantidad_disponible = db.Column(db.Integer, nullable=False, default=0)
    ubicacion = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    imagen = db.Column(db.String(255), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'cantidad_total': self.cantidad_total,
            'cantidad_disponible': self.cantidad_disponible,
            'ubicacion': self.ubicacion,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'imagen_url': f"/uploads/{self.imagen}" if self.imagen else None
        }

# =========================
# PRÉSTAMOS
# =========================
class Prestamo(db.Model):
    __bind_key__ = 'manto'
    __tablename__ = 'prestamos'

    id = db.Column(db.Integer, primary_key=True)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'), nullable=False)
    
    # Agregado name para Postgres
    tipo_prestamo = db.Column(
        db.Enum('docente', 'alumno', 'externo', name='tipo_prestamo_enum'), 
        nullable=False
    )

    solicitante = db.Column(db.String(150), nullable=False)
    referencia = db.Column(db.String(50))
    fecha_prestamo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion = db.Column(db.DateTime)

    # Agregado name para Postgres
    estatus = db.Column(
        db.Enum('activo', 'devuelto', 'cancelado', name='estatus_prestamo_enum'), 
        default='activo'
    )

    observaciones = db.Column(db.Text)
    inventario = db.relationship('Inventario')

    def to_dict(self):
        return {
            'id': self.id,
            'inventario_id': self.inventario_id,
            'inventario': self.inventario.nombre if self.inventario else None,
            'tipo_prestamo': self.tipo_prestamo,
            'solicitante': self.solicitante,
            'referencia': self.referencia,
            'fecha_prestamo': self.fecha_prestamo.isoformat(),
            'fecha_devolucion': self.fecha_devolucion.isoformat() if self.fecha_devolucion else None,
            'estatus': self.estatus,
            'observaciones': self.observaciones
        }

# =========================
# SESIONES DE CLASE
# =========================
class SesionClase(db.Model):
    __bind_key__ = 'manto'
    __tablename__ = 'sesiones_clase'

    id = db.Column(db.Integer, primary_key=True)
    docente = db.Column(db.String(150), nullable=False)
    materia = db.Column(db.String(150))
    laboratorio = db.Column(db.String(100))
    grupo = db.Column(db.String(50))
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime)

    # Agregado name para Postgres
    estatus = db.Column(
        db.Enum('activa', 'cerrada', name='estatus_sesion_enum'), 
        default='activa'
    )

    tarjetas = db.relationship('TarjetaPrestamo', backref='sesion')

    def to_dict(self):
        return {
            'id': self.id,
            'docente': self.docente,
            'materia': self.materia,
            'laboratorio': self.laboratorio,
            'grupo': self.grupo,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'estatus': self.estatus,
            'tarjetas_activas': len([t for t in self.tarjetas if t.estatus == 'activa'])
        }

# =========================
# TARJETAS DE PRÉSTAMO
# =========================
class TarjetaPrestamo(db.Model):
    __bind_key__ = 'manto'
    __tablename__ = 'tarjetas_prestamo'

    id = db.Column(db.Integer, primary_key=True)
    sesion_id = db.Column(db.Integer, db.ForeignKey('sesiones_clase.id'), nullable=True)
    responsable_actual = db.Column(db.String(150), nullable=False)
    ubicacion_trabajo = db.Column(db.String(100))

    # Agregado name para Postgres
    estatus = db.Column(
        db.Enum('activa', 'completa', name='estatus_tarjeta_enum'), 
        default='activa'
    )

    creada_en = db.Column(db.DateTime, default=datetime.utcnow)
    materiales = db.relationship('TarjetaMaterial', backref='tarjeta', cascade='all, delete-orphan')

# =========================
# MATERIAL DENTRO DE TARJETA
# =========================
class TarjetaMaterial(db.Model):
    __bind_key__ = 'manto'
    __tablename__ = 'tarjeta_material'

    id = db.Column(db.Integer, primary_key=True)
    tarjeta_id = db.Column(db.Integer, db.ForeignKey('tarjetas_prestamo.id'), nullable=False)
    inventario_id = db.Column(db.Integer, db.ForeignKey('inventario.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    # Agregado name para Postgres
    estado_salida = db.Column(
        db.Enum('bueno', 'regular', 'malo', name='estado_material_enum'), 
        nullable=False
    )
    estado_entrada = db.Column(
        db.Enum('bueno', 'regular', 'malo', name='estado_material_enum')
    )

    devuelto = db.Column(db.Boolean, default=False)
    fecha_salida = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_entrada = db.Column(db.DateTime)
    inventario = db.relationship('Inventario')

# =========================
# BITÁCORA MANTO
# =========================
class BitacoraManto(db.Model):
    __bind_key__ = 'manto'
    __tablename__ = 'bitacora_manto'

    id = db.Column(db.Integer, primary_key=True)
    tabla = db.Column(db.String(50), nullable=False)
    registro_id = db.Column(db.Integer, nullable=False)

    # Agregado name para Postgres
    accion = db.Column(
        db.Enum('INSERT', 'UPDATE', 'DELETE', name='accion_bitacora_enum'), 
        nullable=False
    )

    usuario = db.Column(db.String(100))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'tabla': self.tabla,
            'registro_id': self.registro_id,
            'accion': self.accion,
            'usuario': self.usuario,
            'fecha': self.fecha.isoformat(),
            'descripcion': self.descripcion
        }

# =========================
# EVIDENCIAS DE MANTENIMIENTO
# =========================
class Mantenimiento(db.Model):
    __bind_key__ = 'manto'
    __tablename__ = 'evidencias_mantenimiento'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    laboratorio = db.Column(db.String(100), nullable=False)
    especialista = db.Column(db.String(150), default='Carlos Iván Crespo Alvarado')
    area = db.Column(db.String(100), default='Mantenimiento Industrial')
    notas = db.Column(db.Text, nullable=True)
    
    foto_actual = db.Column(db.String(255))
    foto_proceso = db.Column(db.String(255))
    foto_completado = db.Column(db.String(255))
    
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'laboratorio': self.laboratorio,
            'especialista': self.especialista,
            'area': self.area,
            'notas': self.notas,  # <--- CORREGIDO: Eliminado db.Column que causaba el error
            'fecha': self.fecha_registro.strftime('%d/%m/%Y %H:%M'),
            'fotos': {
                'actual': f"/uploads/{self.foto_actual}" if self.foto_actual else None,
                'proceso': f"/uploads/{self.foto_proceso}" if self.foto_proceso else None,
                'completado': f"/uploads/{self.foto_completado}" if self.foto_completado else None
            }
        }
