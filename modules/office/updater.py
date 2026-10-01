import os
import subprocess
from core.logger import logger

class OfficeUpdater:
    """Módulo para buscar y aplicar actualizaciones oficiales de Microsoft Office."""

    C2R_PATHS = [
        r"C:\Program Files\Common Files\microsoft shared\ClickToRun\OfficeC2RClient.exe",
        r"C:\Program Files (x86)\Common Files\microsoft shared\ClickToRun\OfficeC2RClient.exe",
    ]

    @classmethod
    def find_updater_client(cls) -> str:
        for p in cls.C2R_PATHS:
            if os.path.exists(p):
                return p
        return ""

    @classmethod
    def check_and_update(cls) -> bool:
        """Invoca el cliente oficial de actualización de Office."""
        client = cls.find_updater_client()
        if not client:
            logger.warning("No se encontró el cliente Click-To-Run de Office en las rutas estándar.")
            logger.info("Intentando actualizar mediante Windows Update...")
            try:
                subprocess.run(
                    ["powershell.exe", "-NoProfile", "-Command", "(New-Object -ComObject Microsoft.Update.AutoUpdate).DetectNow()"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                logger.info("Solicitud enviada a Windows Update para buscar parches de Office.")
                return True
            except Exception as e:
                logger.error(f"Error al invocar actualización: {e}")
                return False

        logger.info(f"Iniciando comprobación de actualización de Office con {client}...")
        try:
            # displaylevel=true muestra el cuadro oficial de progreso de Office si hay actualización
            cmd = f'"{client}" /update user displaylevel=true'
            subprocess.Popen(
                cmd,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            logger.success("Buscador de actualizaciones de Office iniciado. Observa la notificación de Microsoft Office.")
            return True
        except Exception as e:
            logger.error(f"Error al ejecutar actualizador de Office: {e}")
            return False
