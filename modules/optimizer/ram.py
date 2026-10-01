import ctypes
import psutil
from core.logger import logger

class RAMOptimizer:
    """Módulo de optimización y liberación de memoria RAM activa."""

    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_SET_QUOTA = 0x0100

    @classmethod
    def get_ram_info(cls) -> dict:
        """Obtiene información actual de la memoria física."""
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "free_gb": round(mem.available / (1024**3), 2),
            "percent": mem.percent
        }

    @classmethod
    def optimize_ram(cls) -> dict:
        """
        Libera memoria llamando a EmptyWorkingSet en los procesos accesibles.
        """
        initial_mem = psutil.virtual_memory()
        logger.info(f"RAM antes de optimizar: {initial_mem.percent}% utilizado ({round(initial_mem.used / (1024**3), 2)} GB)")

        success_count = 0
        total_pids = 0

        # Cargar funciones de la API nativa de Windows
        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                if pid <= 4:
                    continue  # Saltar System e Idle

                total_pids += 1
                handle = kernel32.OpenProcess(
                    cls.PROCESS_QUERY_INFORMATION | cls.PROCESS_SET_QUOTA,
                    False,
                    pid
                )
                if handle:
                    if psapi.EmptyWorkingSet(handle):
                        success_count += 1
                    kernel32.CloseHandle(handle)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            except Exception:
                pass

        final_mem = psutil.virtual_memory()
        freed_bytes = max(0, initial_mem.used - final_mem.used)
        freed_mb = round(freed_bytes / (1024 * 1024), 2)
        freed_gb = round(freed_bytes / (1024**3), 2)

        msg = (
            f"Optimización de RAM finalizada. "
            f"Procesos optimizados: {success_count}. "
            f"Uso de RAM actual: {final_mem.percent}% (Reducción de {round(initial_mem.percent - final_mem.percent, 1)}%)."
        )
        logger.success(msg)

        return {
            "initial_percent": initial_mem.percent,
            "final_percent": final_mem.percent,
            "freed_mb": freed_mb,
            "freed_gb": freed_gb,
            "processes_trimmed": success_count
        }
