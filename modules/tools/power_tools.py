import os
import subprocess
from core.logger import logger

class PowerTools:
    """Módulo de utilidades avanzadas: archivos gigantes, apagado programado, claves y atajos."""

    @staticmethod
    def get_windows_product_key() -> str:
        """Obtiene la clave original de Windows incrustada en BIOS/UEFI."""
        try:
            cmd = "(Get-CimInstance -ClassName SoftwareLicensingService).OA3xOriginalProductKey"
            res = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            key = res.stdout.strip()
            if key:
                return key
            return "Clave digital vinculada a cuenta Microsoft / OEM estándar"
        except Exception:
            return "No se pudo recuperar"

    @staticmethod
    def schedule_shutdown(minutes: int) -> bool:
        """Programa el apagado del PC en N minutos."""
        try:
            seconds = minutes * 60
            subprocess.run(["shutdown", "/s", "/t", str(seconds)], creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info(f"Apagado programado en {minutes} minutos.")
            return True
        except Exception as e:
            logger.error(f"Error al programar apagado: {e}")
            return False

    @staticmethod
    def cancel_shutdown() -> bool:
        """Cancela cualquier apagado programado."""
        try:
            subprocess.run(["shutdown", "/a"], creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info("Apagado programado cancelado.")
            return True
        except Exception:
            return False

    @staticmethod
    def find_large_files(min_mb: int = 500, max_results: int = 15) -> list:
        """Busca archivos grandes en las carpetas personales del usuario."""
        user_profile = os.environ.get("USERPROFILE", "C:\\Users")
        target_dirs = [
            os.path.join(user_profile, "Downloads"),
            os.path.join(user_profile, "Documents"),
            os.path.join(user_profile, "Videos"),
            os.path.join(user_profile, "Desktop")
        ]

        found = []
        min_bytes = min_mb * 1024 * 1024

        for d in target_dirs:
            if not os.path.exists(d):
                continue
            for root, _, files in os.walk(d):
                for f in files:
                    try:
                        fp = os.path.join(root, f)
                        if not os.path.islink(fp):
                            size = os.path.getsize(fp)
                            if size >= min_bytes:
                                found.append({
                                    "name": f,
                                    "path": fp,
                                    "size_mb": round(size / (1024 * 1024), 1),
                                    "size_gb": round(size / (1024**3), 2)
                                })
                    except Exception:
                        pass

        found.sort(key=lambda x: x["size_mb"], reverse=True)
        return found[:max_results]

    @staticmethod
    def launch_tool(tool_name: str):
        """Lanza herramientas administrativas integradas de Windows."""
        tools = {
            "taskmgr": ["taskmgr.exe"],
            "devmgmt": ["devmgmt.msc"],
            "services": ["services.msc"],
            "regedit": ["regedit.exe"],
            "cleanmgr": ["cleanmgr.exe"],
            "gpedit": ["gpedit.msc"],
            "godmode": [
                "explorer.exe",
                r"shell:::{ED7BA470-8E54-465E-825C-99712043E01C}"
            ]
        }
        if tool_name in tools:
            try:
                subprocess.Popen(tools[tool_name])
            except Exception as e:
                logger.error(f"Error al abrir {tool_name}: {e}")
