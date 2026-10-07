#Apartado 1.1: Definir 4 clases principales con sus constructores
#Apartado 1.2: Añadir encapsulamiento (getter)
#Apartado 1.4: Sobrecarga __repr__ (representar obj como texto) y __eq__ (para decidir cuando dos obj son iguales)
#Apartado 1.6: Uso de tuplas o listas

#Apartado 2.1: Definir 1 clase abstracta y 2 subclases concretas
#Apartado 2.2: Definir interfaz (Protocol)
#Apartado 2.3: Implementar excepciones
#Apartado 2.4: Genericidad [T]

#1
from types import NotImplementedType

#2
from abc import ABC, abstractmethod
from typing import Protocol
from typing import Generic, TypeVar, Iterator


#2.2 Interface
class Resumible(Protocol) :
    def resumen(self)->str:
        pass



#1.1 clase1
class ObjetoCeleste:
    #1.1 constructor, 1.6 uso de tupla
    def __init__(self, identificador:str, tipo:str, coordenadas:tuple[float,float]) -> None:
        # .strip() quita los espacios
        if not identificador.strip() or not tipo.strip():
            raise ValueError("El identificador y el tipo NO pueden estar vacios")
        if len(coordenadas) != 2 :
            raise ValueError("Se necesitan exactamente 2 coordenadas, AR y declinacion ")
        ar, dec = (float(valor) for valor in coordenadas) #convertir los valores a float
        if ar <0 or ar > 360 or dec <-90 or dec>90 :
            raise ValueError("Coordenadas fuera de rango")

        self._identificador = identificador.strip()
        self._tipo = tipo.strip()
        self.__coordenadas = coordenadas

    # 1.2 getters (encapsulamiento)
    @property
    def identificador(self) -> str:
        return self._identificador

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def coordenadas(self) -> tuple[float, float]:
        return self.__coordenadas

    #sobrecarga representacion como texto
    def __repr__(self) -> str:
        return f"ObjetoCeleste({self.identificador!r}, {self.tipo!r}, {self.coordenadas!r})"

    #sobrecarga equivalente
    def __eq__(self, otro:object) -> bool | NotImplementedType:
        #comprobacion si "otro" es una instancia de ObjetoCeleste
        if not isinstance(otro, ObjetoCeleste):
            return NotImplemented
        #retorno de igualdad por valor
        return (self.identificador, self.tipo, self.coordenadas) == (otro.identificador, otro.tipo, otro.coordenadas)

#1.1 clase2
class Telescopio(ABC) :
    UNIDAD_HORAS = 'h'
    #1.1 constructor
    def __init__(self, nombre:str, horas_uso:int = 0, diametro_mm:int=0) -> None:
        #usamos el setter
        self.nombre = nombre
        self.horas_uso = horas_uso
        self.diametro_mm = diametro_mm

    #2.1 metodo abstracto
    @abstractmethod
    def descripcion_tecnica(self)->str:
        pass

    #1.2 getter (encapsulamiento)
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def horas_uso(self) -> int:
        return self.__horas_uso

     #(añadido para la segunda entrega)
    @property
    def diametro_mm(self) -> int:
        return self.__diametro_mm

    @nombre.setter
    def nombre(self, nuevo_valor:str)->None:
        if not isinstance(nuevo_valor, str):
            raise TypeError("El nombre tiene que ser un string")
        if not nuevo_valor.strip() :
            raise TypeError("El nombre del telescopio no puede estar vacio")
        self.__nombre = nuevo_valor.strip()

    @horas_uso.setter
    def horas_uso(self, nuevo_valor:int)->None:
        if type(nuevo_valor) is not int :
            raise TypeError("Las horas de uso tienen que ser un int")
        if nuevo_valor < 0 :
            raise TypeError("Las horas de uso tienen que ser mayor o igual a 0")
        #Aqui se instancia el atributo
        self.__horas_uso = nuevo_valor

    # (añadido para la segunda entrega)
    @diametro_mm.setter
    def diametro_mm(self, nuevo_valor:int)->None:
        if type(nuevo_valor) is not int :
            raise TypeError("El diametro tiene que ser un int")
        if nuevo_valor <= 0 :
            raise TypeError("El diametro tiene que ser mayor a 0")
        #Aqui se instancia el atributo
        self.__diametro_mm = nuevo_valor

#2.1 instancias clase abstracta
class TelescopioRefractor(Telescopio):
    def __init__(self, nombre:str, horas_uso:int = 0, diametro_mm:int = 100):
        super().__init__(nombre, horas_uso, diametro_mm)
    def descripcion_tecnica(self)->str:
        return f" {self.nombre} (Refractor de lentes), diámetro: {self.diametro_mm} mm"

class TelescopioReflector(Telescopio):
    def __init__(self, nombre:str, horas_uso:int = 0, diametro_mm:int = 200):
        super().__init__(nombre, horas_uso, diametro_mm)
    def descripcion_tecnica(self) ->str:
        return f" {self.nombre} (Reflector de espejos), diámetro: {self.diametro_mm} mm"



#1.1 clase3
class SesionObservacion:
    #1.1 constructor
    def __init__(self, fecha:str, telescopio:Telescopio, objetivo:ObjetoCeleste) -> None:
        #instanciar atributos
        self.fecha = fecha
        self.telescopio = telescopio
        self.objetivo = objetivo

    def resumen(self) -> str:
        return f"Sesión {self.fecha}: {self.objetivo.identificador} con {self.telescopio.nombre}"

#1.1 clase4
class CatalogoObservatorio:
    #1.1 constructor, 1.6 uso de lista
    def __init__(self, nombre:str, objetos_iniciales:list[ObjetoCeleste]) -> None:
        #instanciar atributos
        self.nombre = nombre
        self.objetos = objetos_iniciales
        #capacidad maxima de 24
        self.__capacidad_maxima = len(objetos_iniciales) * 3

    #1.2 getter (encapsulamiento)
    @property
    def capacidad_maxima(self) -> int:
        return self.__capacidad_maxima

    #2.3 excepciones
    def anadir(self, objeto: ObjetoCeleste) -> None:
        if len(self.objetos) >= self.capacidad_maxima:
            raise CapacidadMaximaError(
                f"No se puede registrar '{objeto.identificador}'. Capacidad máxima alcanzada.",
                len(self.objetos),
                self.capacidad_maxima,
            )
        self.objetos.append(objeto)

    #2.2
    def resumen(self) -> str:
        return f"Catálogo '{self.nombre}' con {len(self.objetos)}/{self.capacidad_maxima} objetos registrados"


#Creamos un ejemplo de catalogo
def crear_catalogo_ejemplo() -> CatalogoObservatorio :
    #datos, ar y dec en grados
    #Exactamente 8 elementos como pide el enunciado
    elementos = [
        ObjetoCeleste("Sol", "Estrella", (10.68, 41.27)),
        ObjetoCeleste("Luna", "Luna", (83.82, -5.39)),
        ObjetoCeleste("Sirio", "Estrella", (101.29, -16.72)),
        ObjetoCeleste("Júpiter", "Planeta", (0.0, 0.0)),
        ObjetoCeleste("Saturno", "Planeta", (1.0, 1.0)),
        ObjetoCeleste("Neptuno", "Planeta", (83.63, 22.01)),
        ObjetoCeleste("M45", "Cúmulo", (56.75, 24.12)),
        ObjetoCeleste("Pluton", "Planeta", (88.79, 7.41)),
    ]

    return CatalogoObservatorio("Test Catalogo", elementos)


#2.2 funcion polimorfica
def mostrar_resumen(elemento: Resumible) ->None:
    print(elemento.resumen())


#2.3 excepciones
class CapacidadMaximaError(Exception):
    """Excepción lanzada cuando el catálogo alcanza su límite de capacidad."""
    def __init__(self, mensaje: str, capacidad_actual: int, capacidad_maxima: int) -> None:
        super().__init__(mensaje)
        self.capacidad_actual = capacidad_actual
        self.capacidad_maxima = capacidad_maxima

#2.4 Genericidad
T = TypeVar("T")

class Repositorio(Generic[T]):
    """Estructura genérica tipada para almacenar colecciones de elementos."""
    def __init__(self) -> None:
        self._elementos: list[T] = []

    def agregar(self, item: T) -> None:
        self._elementos.append(item)

    def obtener_todos(self) -> list[T]:
        return list(self._elementos)

    def __len__(self) -> int:
        return len(self._elementos)

    def __iter__(self) -> Iterator[T]:
        return iter(self._elementos)

#2.6 Excepciones de validación
class RegistroInvalidoError(Exception):
    """Excepción lanzada cuando un registro de entrada no cumple los criterios de validación."""
    pass