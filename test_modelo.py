"""
test_modelo.py
- Pruebas de identidad, sobrecarga de operadores y alias (Práctica 1)
- Apartado 4 (Entrega 2): Genericidad, persistencia a JSON y predicción vs ejecución (== e is)
"""

import json
from modelo import ObjetoCeleste, Repositorio

INTEGRANTES: tuple[str, ...] = ("Carlos Balbas", "Lucas Parreño", "Victor Llorente")
ARCHIVO_JSON: str = "objetos_integrantes.json"


def main() -> None:
    # =========================================================================
    # PRUEBAS PRÁCTICA 1: IDENTIDAD, ALIAS, REPR Y SOBRECARGA DE IGUALDAD
    # =========================================================================
    print("=" * 70)
    print("PRÁCTICA 1: COMPROBACIONES DE IDENTIDAD, IGUALDAD Y ALIAS")
    print("=" * 70)

    for nombre in INTEGRANTES:
        identificador = f"OBJ-{nombre}"
        obj1 = ObjetoCeleste(identificador, "Ejemplo", (10.68, 41.27))
        obj2 = ObjetoCeleste(identificador, "Ejemplo", (10.68, 41.27))
        obj3 = ObjetoCeleste(identificador, "Ejemplo", (20.0, 30.0))
        alias_obj1 = obj1

        print("\nIntegrante:", nombre)
        print("repr(obj1):", repr(obj1))
        print("obj1 is obj2:", obj1 is obj2)
        print("obj1 == obj2:", obj1 == obj2)
        print("obj1 is alias_obj1:", obj1 is alias_obj1)
        print("obj1 == alias_obj1:", obj1 == alias_obj1)
        print("obj1 == obj3:", obj1 == obj3)
        print("id(obj1):", id(obj1))
        print("id(obj2):", id(obj2))
        print("id(alias_obj1):", id(alias_obj1))

        assert obj1 is not obj2 and obj1 == obj2
        assert alias_obj1 is obj1 and alias_obj1 == obj1
        assert obj1 != obj3

    # =========================================================================
    # APARTADO 4.1: ESTRUCTURA GENÉRICA (Generic[T] / TypeVar)
    # =========================================================================
    print("\n" + "=" * 70)
    print("APARTADO 4.1: Estructura Genérica Repositorio[ObjetoCeleste]")
    print("=" * 70)

    # Creamos un repositorio tipado usando los nombres de los integrantes
    repo_original: Repositorio[ObjetoCeleste] = Repositorio()

    for idx, nombre in enumerate(INTEGRANTES):
        # Coordenadas válidas derivadas para cada integrante
        coord = (10.0 * (idx + 1), 15.0 * (idx + 1))
        obj = ObjetoCeleste(f"OBJ-{nombre}", "Cuerpo-Integrantes", coord)
        repo_original.agregar(obj)

    print(f"Total de objetos registrados en el Repositorio: {len(repo_original)}")
    for obj in repo_original:
        print(f"  - Registrado: {obj}")

    # =========================================================================
    # APARTADO 4.2: PERSISTENCIA A JSON CON with open(...) Y RECONSTRUCCIÓN
    # =========================================================================
    print("\n" + "=" * 70)
    print("APARTADO 4.2: Persistencia a JSON y Reconstrucción")
    print("=" * 70)

    # 1. Guardar en JSON con with open(...)
    datos_serializados = [
        {
            "identificador": obj.identificador,
            "tipo": obj.tipo,
            "coordenadas": list(obj.coordenadas),
        }
        for obj in repo_original
    ]

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(datos_serializados, f, indent=4, ensure_ascii=False)
    print(f"-> Datos persistidos exitosamente en '{ARCHIVO_JSON}'.")

    # 2. Cargar desde JSON con with open(...) y reconstruir objetos
    repo_reconstruido: Repositorio[ObjetoCeleste] = Repositorio()

    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        datos_recuperados = json.load(f)

    for item in datos_recuperados:
        coord_rec = (float(item["coordenadas"][0]), float(item["coordenadas"][1]))
        obj_nuevo = ObjetoCeleste(item["identificador"], item["tipo"], coord_rec)
        repo_reconstruido.agregar(obj_nuevo)

    print(f"-> Objetos recargados y reconstruidos: {len(repo_reconstruido)}")

    # =========================================================================
    # APARTADO 4.3: PREDICCIÓN + EJECUCIÓN (== e is)
    # =========================================================================
    print("\n" + "=" * 70)
    print("APARTADO 4.3: Predicción vs. Ejecución (== e is)")
    print("=" * 70)

    print("[Predicción teórica]")
    print("  - orig == rec -> True  (el método __eq__ compara valores de atributos)")
    print("  - orig is rec -> False (son instancias creadas por separado en heap, con id() distinto)")

    print("\n[Ejecución real]")
    for orig, rec in zip(repo_original, repo_reconstruido):
        print(f"\n--- Comparando objeto del integrante: '{orig.identificador}' ---")
        print(f"  id(original)     = {id(orig)}")
        print(f"  id(reconstruido) = {id(rec)}")
        print(f"  orig == rec      -> {orig == rec}")
        print(f"  orig is rec      -> {orig is rec}")

        # Aserciones formales que certifican la predicción
        assert orig == rec, "Los objetos deben coincidir por valor/contenido (__eq__)"
        assert orig is not rec, "Los objetos deben ser instancias independientes en memoria"

    print("\n" + "=" * 70)
    print("Todas las pruebas del Apartado 4 se han completado con éxito.")
    print("=" * 70)


if __name__ == "__main__":
    main()