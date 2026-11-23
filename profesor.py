"""Clase Profesor que hereda de Persona."""

from persona import Persona


class Profesor(Persona):
    """Representa un docente del sistema."""

    def __init__(self, nombre, edad, correo, id_nomina, especialidad):
        """Inicializa el profesor con su nomina y especialidad."""
        super().__init__(nombre, edad, correo)

        if not id_nomina or not str(id_nomina).strip():
            raise ValueError("El ID de nomina no puede estar vacio.")
        if not especialidad or not str(especialidad).strip():
            raise ValueError("La especialidad no puede estar vacia.")

        self._id_nomina = str(id_nomina).strip().upper()
        self._especialidad = str(especialidad).strip()
        self._materias = []

    def obtener_id_nomina(self):
        """Devuelve el ID de nomina del profesor."""
        return self._id_nomina

    def asignar_materia(self, materia):
        """Agrega una materia a la lista del profesor."""
        if not materia or not str(materia).strip():
            raise ValueError("El nombre de la materia no puede estar vacio.")
        mat = str(materia).strip()
        if mat not in self._materias:
            self._materias.append(mat)

    def describir(self):
        """Muestra los datos del profesor y sus materias."""
        materias = ", ".join(self._materias) if self._materias else "Ninguna"
        return f"Profesor [{self._id_nomina}]: {self._nombre} | Especialidad: {self._especialidad} | Materias: {materias}"

    def a_dict(self):
        """Convierte el profesor a diccionario para guardarlo."""
        return {
            "tipo": "Profesor",
            "nombre": self._nombre,
            "edad": self._edad,
            "correo": self._correo,
            "id_nomina": self._id_nomina,
            "especialidad": self._especialidad,
            "materias": self._materias
        }