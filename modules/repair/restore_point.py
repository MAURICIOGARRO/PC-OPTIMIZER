import subprocess
from core.logger import logger

class RestorePointManager:
    """Módulo para crear y gestionar Puntos de Restauración del Sistema."""

    @staticmethod
    def create_restore_point(description: str = "OptiCore_RestorationPoint") -> bool:
        """Crea un punto de restauración del sistema de forma segura."""
        logger.info(f"Creando Punto de Restauración del Sistema ('{description}')...")
        try:
            # Primero asegurar que la protección esté habilitada en C:
            ps_enable = "Enable-ComputerRestore -Drive 'C:\\' -ErrorAction SilentlyContinue"
            subprocess.run(
                ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_enable],
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=20
            )

            # Crear el punto de restauración
            ps_cmd = f"Checkpoint-Computer -Description '{description}' -RestorePointType 'MODIFY_SETTINGS' -ErrorAction Stop"
            res = subprocess.run(
                ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=60
            )

            if res.returncode == 0:
                logger.success("¡Punto de Restauración creado exitosamente!")
                return True
            else:
                logger.warning(f"Aviso al crear punto de restauración: {res.stderr.strip() or res.stdout.strip()}")
                return False
        except subprocess.TimeoutExpired:
            logger.warning("La creación del punto de restauración tardó demasiado tiempo.")
            return False
        except Exception as e:
            logger.error(f"Error al crear punto de restauración: {e}")
            return False
