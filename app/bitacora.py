# app/routes/bitacora.py
from flask_restx import Namespace, Resource
from app.models import Bitacora  # ← CAMBIO AQUÍ: import absoluto

bitacora_namespace = Namespace('bitacora', description='Operaciones de bitácora de cambios')

@bitacora_namespace.route('')
class BitacoraList(Resource):
    def get(self):
        """Obtiene todos los registros de la bitácora ordenados por fecha descendente"""
        try:
            logs = Bitacora.query.order_by(Bitacora.fecha_hora.desc()).all()
            
            result = []
            for log in logs:
                result.append({
                    'id_bitacora': log.id_bitacora,
                    'operacion': log.operacion,
                    'usuario': log.usuario or 'Sistema',
                    'fecha_hora': log.fecha_hora.isoformat() if log.fecha_hora else None,
                    'id_registro': log.id_registro,
                    
                    # Valores antiguos
                    'alumno_antiguo': log.alumno_antiguo,
                    'cuatrimestre_antiguo': log.cuatrimestre_antiguo,
                    'grupo_antiguo': log.grupo_antiguo,
                    'tutor_antiguo': log.tutor_antiguo,
                    'celular_antiguo': log.celular_antiguo,
                    'matricula_antigua': log.matricula_antigua,
                    'numero_casillero_antiguo': log.numero_casillero_antiguo,
                    'pagado_antiguo': log.pagado_antiguo,
                    'en_uso_antiguo': log.en_uso_antiguo,
                    'fecha_prestamo_antigua': log.fecha_prestamo_antigua.isoformat() if log.fecha_prestamo_antigua else None,
                    
                    # Valores nuevos
                    'alumno_nuevo': log.alumno_nuevo,
                    'cuatrimestre_nuevo': log.cuatrimestre_nuevo,
                    'grupo_nuevo': log.grupo_nuevo,
                    'tutor_nuevo': log.tutor_nuevo,
                    'celular_nuevo': log.celular_nuevo,
                    'matricula_nueva': log.matricula_nueva,
                    'numero_casillero_nuevo': log.numero_casillero_nuevo,
                    'pagado_nuevo': log.pagado_nuevo,
                    'en_uso_nuevo': log.en_uso_nuevo,
                    'fecha_prestamo_nueva': log.fecha_prestamo_nueva.isoformat() if log.fecha_prestamo_nueva else None,
                })
            
            return result, 200
            
        except Exception as e:
            return {'error': 'Error al obtener la bitácora', 'details': str(e)}, 500