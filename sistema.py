"""Modulo principal del sistema academico y metodos del contrato."""

import json
import os
from alumno import Alumno
from profesor import Profesor
from curso import Curso


class SistemaAcademico:
    """Gestiona los registros de alumnos, profesores y cursos."""

    def __init__(self):
        """Inicializa los diccionarios de almacenamiento del sistema."""
        self._registros = {}
        self._cursos = {}

    def agregar_curso(self, curso):
        """Agrega un curso nuevo al sistema."""
        if not isinstance(curso, Curso):
            raise ValueError("El objeto debe ser un Curso.")
        nombre = curso.obtener_nombre_curso()
        if nombre in self._cursos:
            raise ValueError("Ese curso ya esta registrado.")
        self._cursos[nombre] = curso

    def registrar(self, objeto):
        """Registra un Alumno o Profesor en el sistema."""
        if isinstance(objeto, Alumno):
            clave = objeto.obtener_codigo()
        elif isinstance(objeto, Profesor):
            clave = objeto.obtener_id_nomina()
        else:
            raise ValueError("Tipo de objeto no valido para registrar.")

        if clave in self._registros:
            raise ValueError(f"El identificador {clave} ya esta registrado.")

        self._registros[clave] = objeto

    def asignar(self, identificador, clave):
        """Asigna un alumno o profesor ya registrado al curso indicado."""
        id_usr = str(identificador).strip().upper()
        nombre_curso = str(clave).strip()

        if id_usr not in self._registros:
            raise ValueError(f"No se encontro ningun registro con ID {id_usr}.")
        if nombre_curso not in self._cursos:
            raise ValueError(f"No se encontro el curso {nombre_curso}.")

        persona = self._registros[id_usr]
        curso = self._cursos[nombre_curso]

        if isinstance(persona, Alumno):
            curso.inscribir_alumno(persona)
        elif isinstance(persona, Profesor):
            curso.asignar_profesor(persona)

    def listar(self):
        """Imprime todos los usuarios y cursos registrados."""
        for obj in self._registros.values():
            print(obj.describir())
        for curso in self._cursos.values():
            print(curso.describir())

    def guardar(self, ruta):
        """Guarda el estado actual del sistema en un archivo JSON."""
        datos = {
            "usuarios": [u.a_dict() for u in self._registros.values()],
            "cursos": [c.a_dict() for c in self._cursos.values()]
        }
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar(self, ruta):
        """Carga el estado del sistema desde un archivo JSON si existe."""
        if not os.path.exists(ruta):
            return

        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            if not contenido:
                return
            datos = json.loads(contenido)

        self._registros.clear()
        self._cursos.clear()

        for u in datos.get("usuarios", []):
            if u["tipo"] == "Alumno":
                alumno = Alumno(u["nombre"], u["edad"], u["correo"], u["codigo"])
                for nota in u.get("notas", []):
                    alumno.registrar_nota(nota)
                self._registros[alumno.obtener_codigo()] = alumno
            elif u["tipo"] == "Profesor":
                prof = Profesor(u["nombre"], u["edad"], u["correo"], u["id_nomina"], u["especialidad"])
                for mat in u.get("materias", []):
                    prof.asignar_materia(mat)
                self._registros[prof.obtener_id_nomina()] = prof

        for c in datos.get("cursos", []):
            docente = self._registros.get(c["docente_id"])
            if docente and isinstance(docente, Profesor):
                curso = Curso(c["nombre_curso"], c["cupo_maximo"], docente)
                for cod in c.get("inscritos", []):
                    alumno = self._registros.get(cod)
                    if alumno and isinstance(alumno, Alumno):
                        curso.inscribir_alumno(alumno)
                self._cursos[curso.obtener_nombre_curso()] = curso


_sistema = SistemaAcademico()


def registrar(objeto):
    """Da de alta un objeto Alumno o Profesor."""
    _sistema.registrar(objeto)


def asignar(identificador, clave):
    """Asigna el objeto registrado al curso indicado."""
    _sistema.asignar(identificador, clave)


def listar():
    """Imprime todos los registrados."""
    _sistema.listar()


def guardar(sistema, ruta):
    """Escribe el estado en el archivo."""
    instancia = sistema if isinstance(sistema, SistemaAcademico) else _sistema
    instancia.guardar(ruta)


def cargar(sistema, ruta):
    """Lee el archivo y reconstruye el estado."""
    instancia = sistema if isinstance(sistema, SistemaAcademico) else _sistema
    instancia.cargar(ruta)