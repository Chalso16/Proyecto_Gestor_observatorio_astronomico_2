"""Comprobaciones de los apartados 1, 2 y 5. Entrega 1"""
"""Comprobaciones de los apartados 1, 2, . Entrega 2"""

import weakref
from modelo import (
    CatalogoObservatorio,
    SesionObservacion,
    TelescopioRefractor,
    crear_catalogo_ejemplo,
    mostrar_resumen,
)

def main() -> None:
    # --- Comprobaciones Apartado 1 ---
    catalogo = crear_catalogo_ejemplo()
    print("Objetos iniciales:", len(catalogo.objetos))
    print("Capacidad máxima:", catalogo.capacidad_maxima)
    assert len(catalogo.objetos) == 8
    assert catalogo.capacidad_maxima == 24

    # Corrección: Instanciar TelescopioRefractor en lugar de Telescopio (ABC)
    telescopio = TelescopioRefractor("Refractor Principal")
    print("Lectura inicial:", telescopio.nombre, telescopio.horas_uso)
    telescopio.nombre = "Refractor Norte"
    telescopio.horas_uso = 5
    print("Tras escritura:", telescopio.nombre, telescopio.horas_uso)

    for atributo, valor in (("horas_uso", -5), ("nombre", "   ")):
        try:
            setattr(telescopio, atributo, valor)
        except (ValueError, TypeError) as error:
            print(f"{type(error).__name__}: {error}")
        else:
            raise AssertionError("La asignación inválida se ha aceptado")

    try:
        TelescopioRefractor("")
    except (ValueError, TypeError) as error:
        print(f"Constructor -> {type(error).__name__}: {error}")
    else:
        raise AssertionError("El constructor ha aceptado un nombre vacío")

    assert telescopio.nombre == "Refractor Norte"
    assert telescopio.horas_uso == 5

    sesion = SesionObservacion("2026-09-22", telescopio, catalogo.objetos[0])
    print("Sesión:", sesion.resumen())
    print("Telescopio compartido:", sesion.telescopio is telescopio)

    # =========================================================================
    # APARTADO 2: PROTOCOLO (typing.Protocol), POLIMORFISMO Y PREDICCIÓN
    # =========================================================================
    print("\n" + "=" * 55)
    print("APARTADO 2: Polimorfismo con Resumible (Duck Typing)")
    print("=" * 55)

    # 1. Clases no relacionadas por herencia:
    #    - sesion: Instancia de SesionObservacion
    #    - catalogo: Instancia de CatalogoObservatorio
    #    Ambas implementan def resumen(self) -> str sin heredar de Resumible.

    # 2. Predicción de la salida polimórfica:
    prediccion_sesion = "Sesión 2026-09-22: Sol con Refractor Norte"
    prediccion_catalogo = "Catálogo 'Test Catalogo' con 8/24 objetos registrados"

    print("[Predicción]")
    print(f"  sesion   -> {prediccion_sesion}")
    print(f"  catalogo -> {prediccion_catalogo}")

    print("\n[Ejecución real]")
    print("  sesion   -> ", end="")
    mostrar_resumen(sesion)
    print("  catalogo -> ", end="")
    mostrar_resumen(catalogo)

    # Verificación de que la salida real coincide con la predicción
    assert sesion.resumen() == prediccion_sesion
    assert catalogo.resumen() == prediccion_catalogo
    print("\nComparación: Salida predicha y ejecución coinciden al 100%.")
    print("=" * 55 + "\n")

    # --- Comprobaciones de Ciclo de Vida y Memoria ---
    t1 = TelescopioRefractor("Ciclo")
    t2 = t1
    seguimiento = weakref.ref(t1)  # No mantiene vivo el objeto
    print("Alias antes de mutar:", t1 is t2)
    t1.horas_uso = 4
    print("Horas vistas por t2:", t2.horas_uso)
    t1 = 100  # Rebinding: t1 deja de referirse al telescopio
    print("Tras rebinding:", t1, t2.nombre)
    print("Sigue vivo por t2:", seguimiento() is t2)
    del t1  # Elimina el nombre ligado al entero, no el telescopio
    t2 = None  # Ya no queda ninguna referencia fuerte
    print("Objeto liberado en CPython:", seguimiento() is None)

if __name__ == "__main__":
    main()