import subprocess
import time
import os
import shutil
from core.logger import logger

class WindowsUpdateRepair:
    """Módulo para reparar Windows Update cuando se queda atascado o con errores."""

    @staticmethod
    def fix_windows_update() -> bool:
        logger.info("=== REPARANDO SERVICIOS DE WINDOWS UPDATE ===")
        services = ["wuauserv", "cryptSvc", "bits", "msiserver"]

        # 1. Detener servicios
        for s in services:
            logger.info(f"Deteniendo servicio {s}...")
            subprocess.run(["net", "stop", s, "/y"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        time.sleep(2)

        # 2. Purgar caché de SoftwareDistribution
        windir = os.environ.get("WINDIR", "C:\\Windows")
        soft_dist = os.path.join(windir, "SoftwareDistribution")
        catroot2 = os.path.join(windir, "System32", "catroot2")

        try:
            download_dir = os.path.join(soft_dist, "Download")
            if os.path.exists(download_dir):
                logger.info("Eliminando archivos corruptos de descarga de actualizaciones...")
                for item in os.listdir(download_dir):
                    p = os.path.join(download_dir, item)
                    try:
                        if os.path.isfile(p):
                            os.unlink(p)
                        else:
                            shutil.rmtree(p, ignore_errors=True)
                    except Exception:
                        pass
        except Exception as e:
            logger.warning(f"Aviso al limpiar descargas: {e}")

        # 3. Reiniciar servicios
        for s in services:
            logger.info(f"Iniciando servicio {s}...")
            subprocess.run(["net", "start", s], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        logger.success("¡Servicios de Windows Update restablecidos correctamente!")
        return True
