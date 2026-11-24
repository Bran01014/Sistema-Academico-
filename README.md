# Sistema Académico — Proyecto Final (POO)

**Integrantes:**
- Oswaldo Collazo
- Brandon Ramirez

## Descripción
Sistema orientado a objetos desarrollado en Python para la administración académica básica de una institución educativa. Permite dar de alta alumnos, profesores y cursos con un docente titular y cupo limitado, inscribir estudiantes evitando duplicados o sobrecupo, calcular promedios finales y alertar sobre calificaciones reprobatorias, manteniendo la persistencia de datos en formato JSON.

## Estructura del Proyecto y Diagrama de Clases
El diseño se fundamenta en dos pilares de la Programación Orientada a Objetos:
1. **Herencia (`ES-UNA`):** La clase base `Persona` concentra los atributos comunes (`_nombre`, `_edad`, `_correo`) y define la interfaz polimórfica `describir()`, la cual es sobrescrita por las subclases `Alumno` y `Profesor`.
2. **Composición (`TIENE-UNA`):** La clase `Curso` actúa como contenedor que gestiona una lista interna de objetos `Alumno` inscritos y una referencia a su `Profesor` titular, controlando la integridad de las inscripciones.

### Archivos del repositorio
- `persona.py`: Clase base `Persona` con encapsulamiento y validaciones generales.
- `alumno.py`: Clase `Alumno` (hereda de `Persona`); gestiona código único, notas, promedio y alertas.
- `profesor.py`: Clase `Profesor` (hereda de `Persona`); gestiona ID de nómina, especialidad y materias impartidas.
- `curso.py`: Clase `Curso`; valida el cupo máximo, evita inscripciones duplicadas y exige un profesor titular.
- `sistema.py`: Clase `SistemaAcademico` y funciones del contrato obligatorio (`registrar`, `asignar`, `listar`, `guardar`, `cargar`).
- `main.py`: Script principal de demostración, persistencia y casos de validación.
- `test_sistema.py`: Suite de pruebas unitarias propias con `unittest`.

## Validaciones Implementadas
El sistema rechaza entradas inválidas lanzando excepciones (`ValueError`) descriptivas:
- Registro de personas/alumnos con nombre vacío o edad/correo inválido.
- Códigos de alumno con menos de 4 caracteres o caracteres no alfanuméricos.
- Registro de calificaciones fuera del rango `0` a `100`.
- Creación de un curso sin un profesor asignado o con cupo menor o igual a `0`.
- Inscripción de un alumno duplicado en el mismo curso.
- Matrícula de alumnos cuando el curso ha alcanzado su cupo máximo.
- Detección de archivos JSON dañados o corruptos al cargar datos, lanzando un `ValueError` controlado en lugar de detener el programa sin control.

## Ejecución y Pruebas

**1. Ejecutar el programa principal:**
```bash
python main.py
