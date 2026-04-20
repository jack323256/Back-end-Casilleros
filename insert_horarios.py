# insert_horarios.py
from app import create_app, db
from app.models import Horario
import json

# Tus datos del JSON (pégalos exactamente como están)
horarios_json = [
  {
    "Dia": "Jueves",
    "Materia": "TERMODINÁMICA",
    "Docente": "Melo Ortega Óscar",
    "Grupo": "2A MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "1 h",
    "horaInicio": "13:30",
    "horaFin": "15:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "TERMODINÁMICA",
    "Docente": "Melo Ortega Óscar",
    "Grupo": "2A MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "1 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "TERMODINÁMICA",
    "Docente": "Vargas Ferrer Juan",
    "Grupo": "2A MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "1 h",
    "horaInicio": "14:30",
    "horaFin": "15:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "TERMODINÁMICA",
    "Docente": "Morato González Mariela",
    "Grupo": "2E MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "1 h",
    "horaInicio": "15:30",
    "horaFin": "16:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Lunes",
    "Materia": "GESTIÓN DEL MANTENIMIENTO",
    "Docente": "López Pacheco Karla Paola",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "08:00",
    "horaFin": "10:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Lunes",
    "Materia": "INGLÉS II",
    "Docente": "Gómez Paniagua Jorge Armando",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Lunes",
    "Materia": "CÁLCULO DIFERENCIAL",
    "Docente": "Carrillo Ramírez Juan de Dios",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Lunes",
    "Materia": "TERMODINÁMICA",
    "Docente": "Galindo Mentle Margarita",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "1 h",
    "horaInicio": "14:30",
    "horaFin": "15:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Martes",
    "Materia": "TERMODINÁMICA",
    "Docente": "Galindo Mentle Margarita",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "07:00",
    "horaFin": "09:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Miércoles",
    "Materia": "FÍSICA",
    "Docente": "Arroyo López Carlos",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "07:00",
    "horaFin": "09:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Miércoles",
    "Materia": "PROBABILIDAD Y ESTADÍSTICA",
    "Docente": "Valdez Aparicio María Magdalena",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "09:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Miércoles",
    "Materia": "INGLÉS II",
    "Docente": "Gómez Paniagua Jorge Armando",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "CÁLCULO DIFERENCIAL",
    "Docente": "Carrillo Ramírez Juan de Dios",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "08:00",
    "horaFin": "10:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "FÍSICA",
    "Docente": "Arroyo López Carlos",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "GESTIÓN DEL MANTENIMIENTO",
    "Docente": "López Pacheco Karla Paola",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "INGLÉS II",
    "Docente": "Gómez Paniagua Jorge Armando",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "14:30",
    "horaFin": "15:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "GESTIÓN DEL MANTENIMIENTO",
    "Docente": "López Pacheco Karla Paola",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "08:00",
    "horaFin": "10:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "FÍSICA",
    "Docente": "Arroyo López Carlos",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "CÁLCULO DIFERENCIAL",
    "Docente": "Carrillo Ramírez Juan de Dios",
    "Grupo": "2A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "PROYECTO INTEGRADOR 2",
    "Docente": "Galindo Mentle Margarita",
    "Grupo": "5B MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "PROYECTO INTEGRADOR 2",
    "Docente": "Galindo Mentle Margarita",
    "Grupo": "5B MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "AUTOMATIZACIÓN Y ROBÓTICA",
    "Docente": "Blas Sánchez Luis Ángel",
    "Grupo": "5B MI",
    "Laboratorio": "Lab de Automatización",
    "Duracion": "2 h",
    "horaInicio": "14:30",
    "horaFin": "16:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "PROYECTO INTEGRADOR 2",
    "Docente": "Galindo Mentle Margarita",
    "Grupo": "5C MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "1 h",
    "horaInicio": "09:00",
    "horaFin": "10:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "AUTOMATIZACIÓN Y ROBÓTICA",
    "Docente": "Blas Sánchez Luis Ángel",
    "Grupo": "5C MI",
    "Laboratorio": "Lab de Automatización",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "AUTOMATIZACIÓN Y ROBÓTICA",
    "Docente": "Blas Sánchez Luis Ángel",
    "Grupo": "5C MI",
    "Laboratorio": "Lab de Automatización",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Miércoles",
    "Materia": "PROYECTO INTEGRADOR 2",
    "Docente": "Galindo Mentle Margarita",
    "Grupo": "5D MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "1 h",
    "horaInicio": "14:30",
    "horaFin": "15:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "PROYECTO INTEGRADOR 2",
    "Docente": "Galindo Mentle Margarita",
    "Grupo": "5D MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "INGLÉS V",
    "Docente": "Pérez Olivares Raúl Arturo",
    "Grupo": "5D MI",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "1 h",
    "horaInicio": "12:30",
    "horaFin": "13:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "SISTEMAS TÉRMICOS E INDUSTRIALES",
    "Docente": "Martínez Martínez Aristides",
    "Grupo": "5D MI",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "2 h",
    "horaInicio": "13:30",
    "horaFin": "15:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "AUTOMATIZACIÓN Y ROBÓTICA",
    "Docente": "Blas Sánchez Luis Ángel",
    "Grupo": "5D MI",
    "Laboratorio": "Lab de Automatización",
    "Duracion": "2 h",
    "horaInicio": "15:30",
    "horaFin": "17:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "TG 5D MI",
    "Docente": "Blas Sánchez Luis Ángel",
    "Grupo": "5D MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "1 h",
    "horaInicio": "09:00",
    "horaFin": "10:00",
    "responsableCierre": "",
    "programas": ["Tutoría"]
  },
  {
    "Dia": "Viernes",
    "Materia": "AUTOMATIZACIÓN Y ROBÓTICA",
    "Docente": "Blas Sánchez Luis Ángel",
    "Grupo": "5D MI",
    "Laboratorio": "Lab de Automatización",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "ECUACIONES DIFERENCIALES",
    "Docente": "Carbajal Fosado Arely",
    "Grupo": "5D MI",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "14:30",
    "horaFin": "16:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Martes",
    "Materia": "CIENCIA DE MATERIALES",
    "Docente": "Saavedra Arellano Dennis Abril",
    "Grupo": "5E MI",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "INGLÉS V",
    "Docente": "Pérez Olivares Raúl Arturo",
    "Grupo": "5E MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "AUTOMATIZACIÓN Y ROBÓTICA",
    "Docente": "Flores Valderrabano Fermín",
    "Grupo": "5E MI",
    "Laboratorio": "Lab de Automatización",
    "Duracion": "2 h",
    "horaInicio": "13:30",
    "horaFin": "15:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "PROYECTO INTEGRADOR 2",
    "Docente": "Arroyo López Carlos",
    "Grupo": "5E MI",
    "Laboratorio": "Lab Electrónica",
    "Duracion": "2 h",
    "horaInicio": "07:00",
    "horaFin": "09:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "INGLÉS V",
    "Docente": "Pérez Olivares Raúl Arturo",
    "Grupo": "5E MI",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Martes",
    "Materia": "INGENIERÍA DE POZOS",
    "Docente": "Saavedra Arellano Dennis Abril",
    "Grupo": "5A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "10:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Martes",
    "Materia": "PROYECTO INTEGRADOR 2",
    "Docente": "Galindo Mentle Margarita",
    "Grupo": "5A MP",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "1 h",
    "horaInicio": "13:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Martes",
    "Materia": "INSTRUMENTACIÓN INDUSTRIAL",
    "Docente": "Carrillo Ramírez Juan de Dios",
    "Grupo": "5A MP",
    "Laboratorio": "Lab de Ciencias Básicas",
    "Duracion": "2 h",
    "horaInicio": "14:30",
    "horaFin": "16:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Miércoles",
    "Materia": "HERRAMIENTAS Y EQUIPOS DE PERFORACIÓN",
    "Docente": "Licona González Marlon",
    "Grupo": "5A MP",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "1 h",
    "horaInicio": "13:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Miércoles",
    "Materia": "INGENIERÍA DE POZOS",
    "Docente": "Saavedra Arellano Dennis Abril",
    "Grupo": "5A MP",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "2 h",
    "horaInicio": "15:30",
    "horaFin": "17:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "TI 5A MP",
    "Docente": "Melo Ortega Óscar",
    "Grupo": "5A MP",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "1 h",
    "horaInicio": "10:00",
    "horaFin": "11:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Viernes",
    "Materia": "TG 5A MP",
    "Docente": "Melo Ortega Óscar",
    "Grupo": "5A MP",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "1 h",
    "horaInicio": "11:00",
    "horaFin": "12:00",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "INTEGRADORA 1",
    "Docente": "Quiroz Rodríguez Adolfo",
    "Grupo": "8A IMI",
    "Laboratorio": "Lab Eléctrica",
    "Duracion": "1 h",
    "horaInicio": "16:30",
    "horaFin": "17:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica y Práctica"]
  },
  {
    "Dia": "Jueves",
    "Materia": "OPTATIVA 1 GESTIÓN AMBIENTAL",
    "Docente": "Aparicio Maldonado Jenny",
    "Grupo": "8B IMI",
    "Laboratorio": "Lab de Automatización",
    "Duracion": "2 h",
    "horaInicio": "12:30",
    "horaFin": "14:30",
    "responsableCierre": "",
    "programas": ["Clase Teórica"]
  }
]

app = create_app()
with app.app_context():
    # Limpiar tabla (opcional, solo si quieres empezar de cero)
    # Horario.query.delete()
    # db.session.commit()

    count = 0
    for item in horarios_json:
        existe = Horario.query.filter_by(
            dia=item["Dia"],
            materia=item["Materia"],
            docente=item["Docente"],
            grupo=item["Grupo"],
            horaInicio=item["horaInicio"],
            laboratorio=item["Laboratorio"]
        ).first()

        if not existe:
            nuevo = Horario(
                dia=item["Dia"],
                materia=item["Materia"],
                docente=item["Docente"],
                grupo=item["Grupo"],
                laboratorio=item["Laboratorio"],
                duracion=item.get("Duracion"),
                horaInicio=item["horaInicio"],
                horaFin=item["horaFin"],
                responsable_cierre=item.get("responsableCierre", ""),
                programas=json.dumps(item.get("programas", [])),
                logo_carrera=None,  # Puedes poner rutas después
                logo_area=None
            )
            db.session.add(nuevo)
            count += 1

    db.session.commit()
    print(f"¡Listo! Se insertaron {count} horarios nuevos en la base de datos.")