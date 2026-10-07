"""Demostración de Entrega 2 Apartado 3: Jerarquía y gestión de excepciones."""

from modelo import (
    CatalogoObservatorio,
    ObjetoCeleste,
    CapacidadMaximaError,
    crear_catalogo_ejemplo,
)

# ----------------------------------------------------------------------
# 1. Versión con fallo: el manejador general intercepta al específico
# ----------------------------------------------------------------------
def anadir_con_fallo(catalogo: CatalogoObservatorio, objeto: ObjetoCeleste) -> None:
    try:
        catalogo.anadir(objeto)
    except Exception:
        # Al estar Exception arriba, cualquier subclase entra aquí
        print("[Con fallo] Capturado por: error general")
    except CapacidadMaximaError:
        # Inalcanzable (dead code)
        print("[Con fallo] Capturado por: no hay capacidad suficiente")


# ----------------------------------------------------------------------
# 2 y 3. Versión corregida: orden adecuado, try/except as/else/finally
# ----------------------------------------------------------------------
def anadir_corregido(catalogo: CatalogoObservatorio, objeto: ObjetoCeleste) -> None:
    try:
        catalogo.anadir(objeto)
    except CapacidadMaximaError as error:
        # Se captura la excepción específica y se acceden a los datos del dominio
        print(f"[Corregido] Error específico: {error}")
        print(f"            Detalle dominio -> Actual: {error.capacidad_actual}, Máximo: {error.capacidad_maxima}")
    except Exception as error_general:
        # Red de seguridad para cualquier otro error inesperado
        print(f"[Corregido] Error inesperado: {error_general}")
    else:
        # Se ejecuta solo si NO hubo ninguna excepción
        print(f"[Corregido] Objeto '{objeto.identificador}' añadido con éxito al catálogo.")
    finally:
        # Se ejecuta SIEMPRE (haya o no excepción)
        print(f"[Corregido] [FINALLY] Estado del catálogo: {len(catalogo.objetos)}/{catalogo.capacidad_maxima} objetos.")


def main() -> None:
    # Creamos un catálogo con 8 objetos (capacidad máxima = 24)
    catalogo = crear_catalogo_ejemplo()

    # Llenamos el catálogo hasta su límite (24 objetos)
    nuevo_obj = ObjetoCeleste("Andromeda", "Galaxia", (10.0, 41.0))
    while len(catalogo.objetos) < catalogo.capacidad_maxima:
        catalogo.anadir(nuevo_obj)

    obj_extra = ObjetoCeleste("Exceso", "Nebulosa", (12.0, 15.0))

    print("=" * 60)
    print("1. EJECUCIÓN CON FALLO (El manejador específico nunca se ejecuta)")
    print("=" * 60)
    anadir_con_fallo(catalogo, obj_extra)

    print("\n" + "=" * 60)
    print("2 y 3. EJECUCIÓN CORREGIDA (Manejador específico + else + finally)")
    print("=" * 60)
    # Caso con error de capacidad
    print("--- Intento que produce CapacidadMaximaError ---")
    anadir_corregido(catalogo, obj_extra)

    # Caso exitoso (eliminamos un objeto para probar la rama else)
    print("\n--- Intento exitoso (ejecución de else) ---")
    catalogo.objetos.pop()
    anadir_corregido(catalogo, obj_extra)


if __name__ == "__main__":
    main()