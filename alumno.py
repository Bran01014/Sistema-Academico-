"""Clase Alumno que hereda de Persona."""

from persona import Persona


class Alumno(Persona):
    """Representa un estudiante con codigo y calificaciones."""

    def __init__(self, nombre, edad, correo, codigo):
        """Inicializa el alumno y valida el formato de su codigo."""
        super().__init__(nombre, edad, correo)

        cod = str(codigo).strip() if codigo is not None else ""
        if len(cod) < 4 or not cod.isalnum():
            raise ValueError("Codigo de alumno invalido. Debe tener al menos 4 caracteres alfanumericos.")

        self._codigo = cod.upper()
        self._notas = []

    def obtener_codigo(self):
        """Devuelve el codigo del alumno."""
        return self._codigo

    def registrar_nota(self, nota):
        """Agrega una nota valida entre 0 y 100."""
        if not isinstance(nota, (int, float)) or nota < 0 or nota > 100:
            raise ValueError("La nota no es valida. Debe estar entre 0 y 100.")
        self._notas.append(float(nota))

    def calcular_promedio(self):
        """Calcula el promedio de las notas del alumno."""
        if not self._notas:
            return 0.0
        return round(sum(self._notas) / len(self._notas), 2)

    def tiene_reprobadas(self):
        """Verifica si el alumno tiene alguna nota menor a 60."""
        for n in self._notas:
            if n < 60:
                return True
        return False

    def describir(self):
        """Muestra los datos del alumno y su promedio."""
        prom = self.calcular_promedio()
        alerta = " - Alerta: nota reprobatoria" if self.tiene_reprobadas() else ""
        return f"Alumno [{self._codigo}]: {self._nombre} | Correo: {self._correo} | Promedio: {prom}{alerta}"

    def a_dict(self):
        """Convierte el alumno a diccionario para guardarlo."""
        return {
            "tipo": "Alumno",
            "nombre": self._nombre,
            "edad": self._edad,
            "correo": self._correo,
            "codigo": self._codigo,
            "notas": self._notas
        }