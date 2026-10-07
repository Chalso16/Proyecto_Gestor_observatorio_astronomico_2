"""Demostración del Apartado 6: Validación con Expresiones Regulares"""

import json
import re
import regex  # Requiere: pip install regex
from modelo import ObjetoCeleste, RegistroInvalidoError, Repositorio

ARCHIVO_PRUEBA = "datos_observatorio.json"


def main() -> None:
    # 1. Definición del patrón como raw string (r"...")
    # Explicación: ^ indica inicio, \d{4} son 4 dígitos, - es literal, \d{2} son 2 dígitos, $ indica fin.
    patron_str_raw = r"^\d{4}-\d{2}-\d{2}$"

    # Compilamos con el módulo estándar 're' y con la librería externa 'regex' para comparar
    compilado_re = re.compile(patron_str_raw)
    compilado_regex = regex.compile(patron_str_raw)

    print("=" * 60)
    print("APARTADO 6: VALIDACIÓN DE REGISTROS (regex y re)")
    print("=" * 60)

    # Predicción sin la "r" inicial
    print(
        "Predicción sin 'r': Si usamos \"^\\d{4}-\\d{2}-\\d{2}$\", Python interpreta '\\d' como una secuencia de escape inválida antes de pasársela al motor regex.")

    repo_validados = Repositorio[ObjetoCeleste]()

    with open(ARCHIVO_PRUEBA, "r", encoding="utf-8") as f:
        datos = json.load(f)

    print("\n--- Iniciando carga de 6 registros ---")
    for i, registro in enumerate(datos, 1):
        try:
            nombre = registro.get("identificador", f"Desconocido-{i}")

            # Comprobar si el campo existe
            if "fecha_descubrimiento" not in registro:
                raise RegistroInvalidoError(f"[{nombre}] Falla: Falta el campo obligatorio 'fecha_descubrimiento'.")

            fecha = registro["fecha_descubrimiento"]

            # Validar formato con regex compilado
            if not compilado_re.match(fecha):
                # Usamos regex para demostrar que ambos motores (re y regex) actúan igual
                assert not compilado_regex.match(fecha)
                raise RegistroInvalidoError(
                    f"[{nombre}] Falla: Formato de fecha '{fecha}' no es válido (Debe ser YYYY-MM-DD).")

            # Si pasa la validación, lo creamos y añadimos
            coord = (float(registro["coordenadas"][0]), float(registro["coordenadas"][1]))
            obj = ObjetoCeleste(registro["identificador"], registro["tipo"], coord)
            repo_validados.agregar(obj)
            print(f" {nombre}: Cargado con éxito.")

        except RegistroInvalidoError as e:
            # Capturamos el error de validación, imprimimos y permitimos que el bucle continúe
            print(f"RECHAZADO -> {e}")

    print("-" * 60)
    print(f"Resumen de carga: {len(repo_validados)} registros válidos guardados en el repositorio.")


if __name__ == "__main__":
    main()