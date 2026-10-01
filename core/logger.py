import datetime
import threading
from typing import Callable, List

class Logger:
    """Sistema centralizado de logs en tiempo real para la consola de la UI."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logger, cls).__new__(cls)
                cls._instance.callbacks: List[Callable[[str, str], None]] = []
                cls._instance.history: List[tuple] = []
        return cls._instance

    def subscribe(self, callback: Callable[[str, str], None]):
        """Registra un callback (mensaje, nivel) para la interfaz gráfica."""
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[str, str], None]):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def log(self, message: str, level: str = "INFO"):
        """
        Niveles soportados: INFO, SUCCESS, WARNING, ERROR, PROGRESS
        """
        now = datetime.datetime.now().strftime("%H:%M:%S")
        formatted = f"[{now}] [{level}] {message}"
        self.history.append((formatted, level))
        
        # Mantener solo los últimos 500 logs en memoria
        if len(self.history) > 500:
            self.history.pop(0)

        # Notificar a los suscriptores de forma segura
        for cb in list(self.callbacks):
            try:
                cb(formatted, level)
            except Exception:
                pass

    def info(self, msg: str):
        self.log(msg, "INFO")

    def success(self, msg: str):
        self.log(msg, "SUCCESS")

    def warning(self, msg: str):
        self.log(msg, "WARNING")

    def error(self, msg: str):
        self.log(msg, "ERROR")

# Instancia global
logger = Logger()
