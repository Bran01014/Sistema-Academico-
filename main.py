"""Archivo principal para probar el funcionamiento del sistema."""

from alumno import Alumno
from profesor import Profesor
from curso import Curso
from sistema import SistemaAcademico, guardar, cargar


def main():
    """Ejecuta pruebas de registro, persistencia y validaciones."""
    archivo_datos = "datos.json"
    sistema = SistemaAcademico()

    cargar(sistema, archivo_datos)

    if not sistema._registros:
        prof = Profesor("Roberto Gomez", 45, "rgomez@escuela.edu", "P001", "Programacion")
        a1 = Alumno("Oswaldo Collazo", 20, "oswaldo@escuela.edu", "A001")
        a2 = Alumno("Brandon Ramirez", 21, "brandon@escuela.edu", "A002")

        a1.registrar_nota(92)
        a1.registrar_nota(85)
        a2.registrar_nota(58)

        sistema.registrar(prof)
        sistema.registrar(a1)
        sistema.registrar(a2)

        curso = Curso("POO", 2, prof)
        sistema.registrar(curso)

        sistema.asignar("A001", "POO")
        sistema.asignar("A002", "POO")

        guardar(sistema, archivo_datos)

    print("--- Registros en el sistema ---")
    sistema.listar()

    print("\n--- Probando validaciones ---")
    pruebas = [
        lambda: Alumno("", 20, "x@escuela.edu", "A005"),
        lambda: sistema._registros["A001"].registrar_nota(120),
        lambda: Alumno("Luis", 19, "luis@escuela.edu", "12"),
        lambda: Curso("Base de Datos", 10, None),
        lambda: sistema.asignar("A001", "POO"),
    ]

    for p in pruebas:
        try:
            p()
        except ValueError as e:
            print(f"Validacion correcta: {e}")

    try:
        a3 = Alumno("Maria Lopez", 20, "maria@escuela.edu", "A003")
        sistema.registrar(a3)
        sistema.asignar("A003", "POO")
    except ValueError as e:
        print(f"Validacion correcta: {e}")


if __name__ == "__main__":
    main()
