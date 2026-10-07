# Gestor de Observatorio Astronómico — Práctica 2

**Asignatura:** Técnicas de Programación Avanzada  
**Grado:** Grado en Ingeniería Informática — Universidad Nebrija  
**Autores:** Carlos Balbás, Lucas Parreño, Víctor Llorente  

---

## 1. Descripción del Proyecto

Este proyecto amplía el modelo de dominio del **Gestor de Observatorio Astronómico** desarrollado en la Práctica 1, incorporando mecanismos avanzados de orientación a objetos y diseño en Python:
- **Herencia nominal y clases abstractas (`abc.ABC`):** Jerarquías con métodos abstractos y especialización de comportamiento.
- **Tipado estructural e interfaces con `typing.Protocol`:** Polimorfismo sobre clases no vinculadas jerárquicamente (*duck typing* estático).
- **Manejo robusto de excepciones:** Jerarquías de errores propios del dominio, orden correcto de captura en bloques `try-except-else-finally` y propagación controlada.
- **Genericidad y Persistencia:** Colección genérica (`Generic[T]`, `TypeVar`) y serialización/deserialización de entidades en formato JSON.
- **Validación con expresiones regulares:** Verificación estricta de formatos del dominio mediante las bibliotecas `re` y `regex`.

---

## 2. Requisitos y Versión de Python

- **Python:** Versión `3.10` o superior (probado y verificado en `Python 3.11`/`3.12`).
- **Gestor de paquetes:** `pip`.

### Dependencias Externas

La práctica utiliza la biblioteca de la biblioteca estándar de Python salvo por la biblioteca de terceros **`regex`**, requerida para las pruebas comparativas de validación avanzada del Apartado 6.

Para instalar las dependencias necesarias:

```bash
python3 -m pip install regex

