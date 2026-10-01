import psutil
from core.logger import logger

class ProcessManager:
    """Módulo para listar y administrar procesos demandantes."""

    @staticmethod
    def get_top_processes(limit: int = 8, sort_by: str = "memory") -> list:
        """
        Obtiene los procesos más pesados del sistema.
        sort_by: 'memory' o 'cpu'
        """
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                info = p.info
                mem_mb = round(info['memory_info'].rss / (1024 * 1024), 1)
                cpu_p = info['cpu_percent'] or 0.0
                procs.append({
                    "pid": info['pid'],
                    "name": info['name'],
                    "cpu": cpu_p,
                    "mem_mb": mem_mb
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            except Exception:
                pass

        if sort_by == "cpu":
            procs.sort(key=lambda x: x["cpu"], reverse=True)
        else:
            procs.sort(key=lambda x: x["mem_mb"], reverse=True)

        return procs[:limit]

    @staticmethod
    def kill_process(pid: int) -> bool:
        """Termina un proceso por su identificador PID."""
        try:
            p = psutil.Process(pid)
            p_name = p.name()
            p.terminate()
            logger.info(f"Proceso {p_name} (PID: {pid}) finalizado con éxito.")
            return True
        except Exception as e:
            logger.error(f"No se pudo terminar el proceso PID {pid}: {e}")
            return False
