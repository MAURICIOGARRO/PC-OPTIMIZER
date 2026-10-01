import os
import winreg
from core.logger import logger

class StartupManager:
    """Gestor de aplicaciones de inicio automático de Windows."""

    STARTUP_LOCATIONS = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "Usuario Actual (HKCU)"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "Máquina Local (HKLM)"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run-Disabled", "Deshabilitados (HKCU)"),
    ]

    @classmethod
    def get_startup_apps(cls) -> list:
        apps = []
        for root_key, subkey, loc_name in cls.STARTUP_LOCATIONS:
            try:
                key = winreg.OpenKey(root_key, subkey, 0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, val, _ = winreg.EnumValue(key, i)
                        is_disabled = "Disabled" in subkey
                        apps.append({
                            "name": name,
                            "command": val,
                            "root": "HKCU" if root_key == winreg.HKEY_CURRENT_USER else "HKLM",
                            "subkey": subkey,
                            "location": loc_name,
                            "enabled": not is_disabled
                        })
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except Exception:
                pass

        # Carpeta Startup de usuario
        appdata = os.environ.get("APPDATA", "")
        startup_folder = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup")
        if os.path.exists(startup_folder):
            for f in os.listdir(startup_folder):
                if f.lower().endswith((".lnk", ".bat", ".cmd", ".exe")):
                    apps.append({
                        "name": f,
                        "command": os.path.join(startup_folder, f),
                        "root": "FOLDER",
                        "subkey": startup_folder,
                        "location": "Carpeta Inicio de Windows",
                        "enabled": True
                    })

        return apps

    @classmethod
    def toggle_app(cls, app: dict, enable: bool) -> bool:
        """Habilita o deshabilita un programa de inicio moviéndolo a una clave secundaria."""
        try:
            root_key = winreg.HKEY_CURRENT_USER if app["root"] == "HKCU" else winreg.HKEY_LOCAL_MACHINE
            source_subkey = app["subkey"]
            
            if enable:
                target_subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            else:
                target_subkey = r"Software\Microsoft\Windows\CurrentVersion\Run-Disabled"

            # Abrir o crear subkey destino
            tgt_key = winreg.CreateKey(root_key, target_subkey)
            winreg.SetValueEx(tgt_key, app["name"], 0, winreg.REG_SZ, app["command"])
            winreg.CloseKey(tgt_key)

            # Borrar de origen
            src_key = winreg.OpenKey(root_key, source_subkey, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(src_key, app["name"])
            winreg.CloseKey(src_key)

            status = "habilitado" if enable else "deshabilitado"
            logger.success(f"Programa '{app['name']}' {status} para el inicio.")
            return True
        except Exception as e:
            logger.error(f"Error al cambiar estado de '{app.get('name')}': {e}")
            return False
