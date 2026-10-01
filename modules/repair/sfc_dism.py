import threading
from typing import Callable, Optional
from core.executor import CommandExecutor
from core.logger import logger

class SystemFileRepair:
    """Módulo para ejecutar DISM y SFC /scannow con reporte en vivo."""

    @classmethod
    def run_dism_repair(cls, on_finish: Optional[Callable[[bool], None]] = None) -> threading.Thread:
        """Ejecuta DISM /Online /Cleanup-Image /RestoreHealth."""
        logger.info("=== INICIANDO REPARACIÓN DE IMAGEN DE WINDOWS (DISM) ===")
        logger.info("Esto puede tardar varios minutos. Por favor no apagues el equipo...")

        def _on_finish(code):
            if code == 0:
                logger.success("DISM: Imagen del sistema reparada o verificada sin errores.")
                if on_finish:
                    on_finish(True)
            else:
                logger.warning(f"DISM finalizó con código {code}.")
                if on_finish:
                    on_finish(False)

        cmd = ["DISM.exe", "/Online", "/Cleanup-Image", "/RestoreHealth"]
        return CommandExecutor.run_command(cmd, on_finish=_on_finish)

    @classmethod
    def run_sfc_scan(cls, on_finish: Optional[Callable[[bool], None]] = None) -> threading.Thread:
        """Ejecuta sfc /scannow para reparar archivos corruptos."""
        logger.info("=== INICIANDO COMPROBACIÓN DE ARCHIVOS DEL SISTEMA (SFC) ===")
        logger.info("Examinando integridad de los archivos de Windows...")

        def _on_finish(code):
            if code == 0:
                logger.success("SFC: No se encontraron infracciones de integridad o fueron reparadas exitosamente.")
                if on_finish:
                    on_finish(True)
            else:
                logger.warning(f"SFC finalizó con código {code}.")
                if on_finish:
                    on_finish(False)

        cmd = ["sfc.exe", "/scannow"]
        return CommandExecutor.run_command(cmd, on_finish=_on_finish)

    @classmethod
    def run_full_repair(cls, on_finish: Optional[Callable[[bool], None]] = None):
        """Ejecuta secuencialmente DISM y luego SFC."""
        def step2(dism_ok):
            logger.info("DISM completado. Iniciando ahora SFC /scannow...")
            cls.run_sfc_scan(on_finish=on_finish)

        cls.run_dism_repair(on_finish=step2)
