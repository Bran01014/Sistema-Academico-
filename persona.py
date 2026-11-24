"""Clase base Persona."""


class Persona:
    """Representa una persona dentro del sistema."""

    def __init__(self, nombre, edad, correo):
        """Inicializa los datos basicos de la persona."""
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre no puede estar vacio. Ingrese un nombre.")
        if not isinstance(edad, int) or isinstance(edad, bool) or edad <= 0:
            raise ValueError("La edad debe ser un entero positivo.")
        if not correo or "@" not in str(correo):
            raise ValueError("El correo no es valido.")

        self._nombre = str(nombre).strip()
        self._edad = edad
        self._correo = str(correo).strip()

    def obtener_nombre(self):
        """Devuelve el nombre de la persona."""
        return self._nombre

    def describir(self):
        """Devuelve la informacion general de la persona."""
        return f"Nombre: {self._nombre}, Edad: {self._edad}, Correo: {self._correo}"
