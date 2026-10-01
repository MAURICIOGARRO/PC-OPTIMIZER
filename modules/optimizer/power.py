import subprocess
import re
from core.logger import logger

class PowerPlanManager:
    """Módulo de gestión y optimización de planes de energía de Windows."""

    ULTIMATE_GUID = "e9a42b02-d5df-448d-aa00-03f14749eb61"
    HIGH_PERF_GUID = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    BALANCED_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e"

    @classmethod
    def get_current_plan(cls) -> str:
        try:
            res = subprocess.run(
                ["powercfg", "/getactivescheme"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            out = res.stdout
            # Buscar el nombre entre paréntesis
            match = re.search(r'\((.*?)\)', out)
            if match:
                return match.group(1)
            return "Desconocido"
        except Exception:
            return "No disponible"

    @classmethod
    def set_ultimate_performance(cls) -> bool:
        """Habilita y activa el plan de Máximo Rendimiento (Ultimate Performance)."""
        logger.info("Activando plan de energía 'Máximo Rendimiento'...")
        try:
            # Primero intentar duplicar el esquema si no está presente
            res = subprocess.run(
                ["powercfg", "-duplicatescheme", cls.ULTIMATE_GUID],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # Buscar GUID en la respuesta
            guid_match = re.search(r'([0-9a-fA-F\-]{36})', res.stdout)
            guid = guid_match.group(1) if guid_match else cls.ULTIMATE_GUID

            # Activar el esquema
            subprocess.run(
                ["powercfg", "/setactive", guid],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            logger.success("Plan 'Máximo Rendimiento' activado con éxito.")
            return True
        except Exception as e:
            logger.warning(f"No se pudo activar Ultimate Performance, intentando Alto Rendimiento: {e}")
            try:
                subprocess.run(["powercfg", "/setactive", cls.HIGH_PERF_GUID], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                logger.success("Plan 'Alto Rendimiento' activado.")
                return True
            except Exception as e2:
                logger.error(f"Error al configurar energía: {e2}")
                return False

    @classmethod
    def set_balanced(cls) -> bool:
        """Restaura el plan equilibrado."""
        try:
            subprocess.run(["powercfg", "/setactive", cls.BALANCED_GUID], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info("Plan 'Equilibrado' restaurado.")
            return True
        except Exception as e:
            logger.error(f"Error al cambiar a Equilibrado: {e}")
            return False
