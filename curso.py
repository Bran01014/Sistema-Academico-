"""Clase Curso que funciona como contenedor con cupo limitado."""

from alumno import Alumno
from profesor import Profesor


class Curso:
    """Administra las inscripciones de alumnos y el docente de un curso."""

    def __init__(self, nombre_curso, cupo_maximo, docente):
        """Crea un curso validando que tenga profesor asignado y cupo valido."""
        if not nombre_curso or not str(nombre_curso).strip():
            raise ValueError("El nombre del curso no puede estar vacio.")
        if not isinstance(cupo_maximo, int) or cupo_maximo <= 0:
            raise ValueError("El cupo maximo debe ser mayor a 0.")
        if docente is None or not isinstance(docente, Profesor):
            raise ValueError("No se puede crear un curso sin profesor asignado.")

        self._nombre_curso = str(nombre_curso).strip()
        self._cupo_maximo = cupo_maximo
        self._docente = docente
        self._inscritos = []
        self._docente.asignar_materia(self._nombre_curso)

    def obtener_nombre_curso(self):
        """Devuelve el nombre del curso."""
        return self._nombre_curso

    def asignar_profesor(self, profesor):
        """Asigna un nuevo profesor titular al curso."""
        if profesor is None or not isinstance(profesor, Profesor):
            raise ValueError("Debe asignar un profesor valido.")
        self._docente = profesor
        self._docente.asignar_materia(self._nombre_curso)

    def inscribir_alumno(self, alumno):
        """Inscribe un alumno validando cupo y que no este duplicado."""
        if not isinstance(alumno, Alumno):
            raise ValueError("Solo se pueden inscribir alumnos.")

        for inscrito in self._inscritos:
            if inscrito.obtener_codigo() == alumno.obtener_codigo():
                raise ValueError("El alumno ya esta inscrito en este curso.")

        if len(self._inscritos) >= self._cupo_maximo:
            raise ValueError("El curso esta lleno, no hay cupo disponible.")

        self._inscritos.append(alumno)
        return True

    def obtener_inscritos(self):
        """Devuelve la lista de alumnos inscritos."""
        return list(self._inscritos)

    def describir(self):
        """Muestra la informacion general del curso."""
        return (
            f"Curso: {self._nombre_curso} | Docente: {self._docente.obtener_nombre()} | "
            f"Inscritos: {len(self._inscritos)}/{self._cupo_maximo}"
        )

    def a_dict(self):
        """Convierte el curso a diccionario para guardarlo."""
        return {
            "nombre_curso": self._nombre_curso,
            "cupo_maximo": self._cupo_maximo,
            "docente_id": self._docente.obtener_id_nomina(),
            "inscritos": [a.obtener_codigo() for a in self._inscritos]
        }