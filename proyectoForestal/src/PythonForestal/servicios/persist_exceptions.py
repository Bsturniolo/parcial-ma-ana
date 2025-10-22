class PersistenciaException(Exception):
    def __init__(self, mensaje: str, nombre_archivo: str = "", operacion: str = ""):
        super().__init__(mensaje)
        self._mensaje = mensaje
        self._nombre = nombre_archivo
        self._op = operacion
    def get_user_message(self) -> str: return self._mensaje
    def get_nombre_archivo(self) -> str: return self._nombre
    def get_tipo_operacion(self) -> str: return self._op
