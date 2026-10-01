import subprocess
import psutil
from core.logger import logger
from modules.tools.oem_debloat import OEMDebloater
from modules.tools.copilot_remover import CopilotRemover
from modules.tools.privacy import WindowsPrivacy

class BackgroundServicesManager:
    """
    Gestor centralizado para auditar y controlar servicios pesados en segundo plano:
    TeamViewer, Xbox Gaming Services, Telemetría OEM, Windows Copilot y Telemetría del Sistema.
    """

    # --- TEAMVIEWER & REMOTO ---
    @staticmethod
    def get_teamviewer_status() -> dict:
        is_installed = False
        is_running = False
        start_type = "No instalado"

        try:
            res = subprocess.run(
                ["sc.exe", "query", "TeamViewer"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if res.returncode == 0:
                is_installed = True
                is_running = "RUNNING" in res.stdout

            res_cfg = subprocess.run(
                ["sc.exe", "qc", "TeamViewer"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if "AUTO_START" in res_cfg.stdout:
                start_type = "Automático (Inicia con Windows)"
            elif "DEMAND_START" in res_cfg.stdout:
                start_type = "Manual (Solo bajo demanda)"
            elif "DISABLED" in res_cfg.stdout:
                start_type = "Deshabilitado"
        except Exception:
            pass

        return {
            "installed": is_installed,
            "running": is_running,
            "start_type": start_type
        }

    @classmethod
    def set_teamviewer_mode(cls, mode: str) -> bool:
        """
        mode: 'manual' (solo cuando abres la app), 'disabled' (apagado total) o 'auto' (arranque con Windows)
        """
        logger.info(f"Configurando TeamViewer en modo: {mode.upper()}...")
        try:
            if mode in ("manual", "disabled"):
                # Detener procesos activos
                for p in psutil.process_iter(['name']):
                    try:
                        if p.info['name'] and 'teamviewer' in p.info['name'].lower():
                            p.terminate()
                    except Exception:
                        pass

                subprocess.run(["sc.exe", "stop", "TeamViewer"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                st_arg = "demand" if mode == "manual" else "disabled"
                subprocess.run(["sc.exe", "config", "TeamViewer", f"start= {st_arg}"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                logger.success(f"TeamViewer configurado en modo {mode.upper()} (ya no consumirá recursos de fondo).")
            else:
                subprocess.run(["sc.exe", "config", "TeamViewer", "start= auto"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["sc.exe", "start", "TeamViewer"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                logger.success("TeamViewer restaurado a inicio automático.")
            return True
        except Exception as e:
            logger.error(f"Error al configurar TeamViewer: {e}")
            return False

    # --- XBOX & GAMING SERVICES ---
    XBOX_SERVICES = [
        "GamingServices",
        "GamingServicesNet",
        "XboxGipSvc",
        "XboxNetApiSvc"
    ]

    @classmethod
    def get_xbox_status(cls) -> dict:
        running_count = 0
        total_installed = 0
        for s in cls.XBOX_SERVICES:
            try:
                res = subprocess.run(["sc.exe", "query", s], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if res.returncode == 0:
                    total_installed += 1
                    if "RUNNING" in res.stdout:
                        running_count += 1
            except Exception:
                pass
        return {
            "installed": total_installed > 0,
            "running": running_count > 0,
            "running_count": running_count,
            "total_count": total_installed
        }

    @classmethod
    def disable_xbox_services(cls) -> bool:
        """Detiene y deshabilita los servicios pesados de Xbox y Gaming Services."""
        logger.info("Desactivando Gaming Services y servicios de fondo de Xbox...")
        for s in cls.XBOX_SERVICES:
            try:
                subprocess.run(["sc.exe", "stop", s], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["sc.exe", "config", s, "start= disabled"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                logger.info(f"Servicio detenido y deshabilitado: {s}")
            except Exception:
                pass
        logger.success("¡Servicios de fondo de Xbox y Gaming Services desactivados!")
        return True

    @classmethod
    def enable_xbox_services(cls) -> bool:
        """Restaura los servicios de Xbox si el usuario va a jugar en Xbox App o Game Pass."""
        logger.info("Restaurando servicios de Xbox y Gaming Services...")
        for s in cls.XBOX_SERVICES:
            try:
                subprocess.run(["sc.exe", "config", s, "start= auto"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["sc.exe", "start", s], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception:
                pass
        logger.success("Servicios de Xbox restaurados.")
        return True
