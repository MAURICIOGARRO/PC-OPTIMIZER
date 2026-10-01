import subprocess
from core.logger import logger

class NetworkRepair:
    """Módulo para reparar problemas de conexión a Internet y reseteo de red."""

    @staticmethod
    def fix_network() -> bool:
        logger.info("=== INICIANDO RESTABLECIMIENTO DE CONEXIÓN DE RED ===")
        commands = [
            ("Vaciando caché de resolución DNS...", ["ipconfig", "/flushdns"]),
            ("Restableciendo catálogo Winsock...", ["netsh", "winsock", "reset"]),
            ("Restableciendo pila TCP/IP...", ["netsh", "int", "ip", "reset"]),
            ("Liberando concesión de dirección IP...", ["ipconfig", "/release"]),
            ("Renovando dirección IP...", ["ipconfig", "/renew"]),
            ("Reiniciando registro de nombres NetBIOS...", ["nbtstat", "-R"]),
        ]

        all_success = True
        for desc, cmd in commands:
            logger.info(desc)
            try:
                res = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=15
                )
                if res.returncode == 0:
                    logger.info(f"OK: {' '.join(cmd)}")
                else:
                    logger.warning(f"Aviso en {' '.join(cmd)}")
            except Exception as e:
                logger.error(f"Error al ejecutar {' '.join(cmd)}: {e}")
                all_success = False

        logger.success("¡Reparación de red completada! Se recomienda reiniciar si los problemas persisten.")
        return all_success
