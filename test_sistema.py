"""Pruebas unitarias propias para validar el Sistema Academico."""

import os
import unittest
from persona import Persona
from alumno import Alumno
from profesor import Profesor
from curso import Curso
from sistema import SistemaAcademico, registrar, asignar, listar, guardar, cargar


class TestSistemaAcademico(unittest.TestCase):
    """Suite de pruebas para validaciones, contrato y persistencia."""

    def setUp(self):
        """Prepara un entorno limpio antes de cada prueba."""
        self.sistema = SistemaAcademico()
        self.profesor = Profesor("Roberto Gomez", 45, "rgomez@escuela.edu", "P001", "Programacion")
        self.alumno1 = Alumno("Oswaldo Collazo", 20, "oswaldo@escuela.edu", "A001")
        self.alumno2 = Alumno("Brandon Ramirez", 21, "brandon@escuela.edu", "A002")
        self.archivo_test = "test_datos_temp.json"

    def tearDown(self):
        """Elimina archivos temporales al finalizar cada prueba."""
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)

    def test_crear_alumno_sin_nombre_falla(self):
        """Rechaza registrar un alumno o persona con el nombre vacio."""
        with self.assertRaises(ValueError):
            Alumno("", 20, "correo@escuela.edu", "A010")
        with self.assertRaises(ValueError):
            Alumno("   ", 20, "correo@escuela.edu", "A011")

    def test_nota_fuera_de_rango_falla(self):
        """Rechaza notas menores a 0 o mayores a 100."""
        with self.assertRaises(ValueError):
            self.alumno1.registrar_nota(-5)
        with self.assertRaises(ValueError):
            self.alumno1.registrar_nota(101)

    def test_codigo_alumno_invalido_falla(self):
        """Rechaza codigos de alumno menores a 4 caracteres o no alfanumericos."""
        with self.assertRaises(ValueError):
            Alumno("Luis Perez", 19, "luis@escuela.edu", "12")
        with self.assertRaises(ValueError):
            Alumno("Luis Perez", 19, "luis@escuela.edu", "A-01")

    def test_crear_curso_sin_profesor_falla(self):
        """Impide crear un curso sin un objeto Profesor valido."""
        with self.assertRaises(ValueError):
            Curso("Bases de Datos", 10, None)
        with self.assertRaises(ValueError):
            Curso("Bases de Datos", 10, "NoSoyProfesor")

    def test_inscribir_alumno_duplicado_falla(self):
        """Impide inscribir dos veces al mismo alumno en el mismo curso."""
        self.sistema.registrar(self.profesor)
        self.sistema.registrar(self.alumno1)
        curso = Curso("POO", 5, self.profesor)
        self.sistema.registrar(curso)

        self.sistema.asignar("A001", "POO")
        with self.assertRaises(ValueError):
            self.sistema.asignar("A001", "POO")

    def test_matricular_en_curso_sin_cupo_falla(self):
        """Bloquea la matricula cuando el curso alcanza su cupo maximo."""
        self.sistema.registrar(self.profesor)
        self.sistema.registrar(self.alumno1)
        self.sistema.registrar(self.alumno2)
        alumno3 = Alumno("Maria Lopez", 20, "maria@escuela.edu", "A003")
        self.sistema.registrar(alumno3)

        curso = Curso("POO", 2, self.profesor)
        self.sistema.registrar(curso)

        self.sistema.asignar("A001", "POO")
        self.sistema.asignar("A002", "POO")
        with self.assertRaises(ValueError):
            self.sistema.asignar("A003", "POO")

    def test_calculo_promedio_y_alerta_reprobatoria(self):
        """Verifica calculo de promedio y deteccion de notas menores a 60."""
        self.alumno1.registrar_nota(90)
        self.alumno1.registrar_nota(80)
        self.assertEqual(self.alumno1.calcular_promedio(), 85.0)
        self.assertFalse(self.alumno1.tiene_reprobadas())

        self.alumno2.registrar_nota(58)
        self.assertTrue(self.alumno2.tiene_reprobadas())
        self.assertIn("Alerta: nota reprobatoria", self.alumno2.describir())

    def test_persistencia_guardar_y_cargar(self):
        """Verifica que el estado sobrevive al guardar y recargar desde JSON."""
        self.alumno1.registrar_nota(95)
        self.sistema.registrar(self.profesor)
        self.sistema.registrar(self.alumno1)
        curso = Curso("Estructuras", 10, self.profesor)
        self.sistema.registrar(curso)
        self.sistema.asignar("A001", "Estructuras")

        guardar(self.sistema, self.archivo_test)

        nuevo_sistema = SistemaAcademico()
        cargar(nuevo_sistema, self.archivo_test)

        self.assertIn("A001", nuevo_sistema._registros)
        self.assertIn("P001", nuevo_sistema._registros)
        self.assertEqual(nuevo_sistema._registros["A001"].calcular_promedio(), 95.0)

    def test_cargar_archivo_inexistente_no_falla(self):
        """Verifica que el sistema arranca sin error si no existe archivo previo."""
        cargar(self.sistema, "archivo_que_no_existe_123.json")
        self.assertEqual(len(self.sistema._registros), 0)

    def test_registrar_curso_con_contrato(self):
        """Verifica que registrar() acepta un Curso directamente."""
        curso = Curso("Matematicas", 15, self.profesor)
        registrar(self.profesor)
        registrar(curso)
        self.assertIn("Matematicas", self.sistema._cursos)

    def test_funciones_modulo_sincronizadas_con_instancia(self):
        """Verifica que las funciones globales trabajan sobre la instancia activa."""
        s = SistemaAcademico()
        registrar(self.profesor)
        registrar(self.alumno1)
        curso = Curso("Fisica", 10, self.profesor)
        registrar(curso)
        asignar("A001", "Fisica")

        self.assertIn("A001", s._registros)
        self.assertEqual(len(s._cursos["Fisica"].obtener_inscritos()), 1)

    def test_json_danado_lanza_excepcion_controlada(self):
        """Verifica que un JSON corrupto lanza ValueError en lugar de morir."""
        with open(self.archivo_test, "w", encoding="utf-8") as f:
            f.write("{esto no es un json valido: [1, 2,")

        with self.assertRaises(ValueError):
            cargar(self.sistema, self.archivo_test)


if __name__ == "__main__":
    unittest.main(verbosity=2)