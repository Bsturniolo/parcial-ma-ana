from typing import Generic, List, TypeVar

T = TypeVar("T")

class Observer(Generic[T]):
    def actualizar(self, valor: T) -> None:
        raise NotImplementedError

class Observable(Generic[T]):
    def __init__(self) -> None:
        self._obs: List[Observer[T]] = []

    # Nombres “clásicos”
    def suscribir(self, o: "Observer[T]") -> None:
        self._obs.append(o)

    def desuscribir(self, o: "Observer[T]") -> None:
        self._obs = [x for x in self._obs if x is not o]

    def notificar(self, v: T) -> None:
        for o in list(self._obs):
            o.actualizar(v)

    # Aliases que pide la rúbrica / README
    def agregar_observador(self, observador: "Observer[T]") -> None:
        self.suscribir(observador)

    def eliminar_observador(self, observador: "Observer[T]") -> None:
        self.desuscribir(observador)

    def notificar_observadores(self, evento: T) -> None:
        self.notificar(evento)
