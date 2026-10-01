import subprocess
from core.logger import logger

class DiskRepair:
    """Módulo para comprobación y reparación de sectores del disco duro."""

    @staticmethod
    def run_online_scan() -> bool:
        """Ejecuta chkdsk C: /scan en línea sin necesidad de reiniciar de inmediato."""
        logger.info("=== ANALIZANDO ESTADO DEL SISTEMA DE ARCHIVOS (CHKDSK ONLINE) ===")
        try:
            res = subprocess.run(
                ["chkdsk", "C:", "/scan"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            logger.info(res.stdout[:500] if res.stdout else "Análisis completado.")
            if res.returncode == 0:
                logger.success("No se encontraron daños en el sistema de archivos del disco C:.")
                return True
            else:
                logger.warning("Se detectaron posibles inconsistencias. Se recomienda programar un escaneo con reinicio.")
                return False
        except Exception as e:
            logger.error(f"Error al analizar disco: {e}")
            return False

    @staticmethod
    def schedule_boot_repair() -> bool:
        """Programa chkdsk C: /f /r para el próximo reinicio."""
        logger.info("Programando reparación completa de disco para el próximo reinicio...")
        try:
            # Enviar 'Y' para confirmar la programación
            proc = subprocess.Popen(
                ["chkdsk", "C:", "/f", "/r"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            out, _ = proc.communicate(input="S\nY\n", timeout=10)
            logger.success("¡Comprobación de disco programada! Se ejecutará la próxima vez que reinicies el PC.")
            return True
        except Exception as e:
            logger.error(f"Error al programar chkdsk: {e}")
            return False
