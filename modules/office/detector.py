import os
import winreg

class OfficeDetector:
    """Módulo para detectar instalaciones existentes de Microsoft Office y sus aplicaciones individuales."""

    OFFICE_APPS = {
        "Word": ["WINWORD.EXE"],
        "Excel": ["EXCEL.EXE"],
        "PowerPoint": ["POWERPNT.EXE"],
        "Outlook": ["OUTLOOK.EXE"],
        "Access": ["MSACCESS.EXE"],
        "Publisher": ["MSPUB.EXE"],
        "OneNote": ["ONENOTE.EXE"]
    }

    ROOT_PATHS = [
        r"C:\Program Files\Microsoft Office\root\Office16",
        r"C:\Program Files (x86)\Microsoft Office\root\Office16",
        r"C:\Program Files\Microsoft Office\Office16",
        r"C:\Program Files (x86)\Microsoft Office\Office16",
        r"C:\Program Files\Microsoft Office\root\Office15",
        r"C:\Program Files (x86)\Microsoft Office\root\Office15",
    ]

    @classmethod
    def detect_installed_office(cls) -> dict:
        """
        Detecta la presencia de Office, versión reportada, arquitectura y aplicaciones presentes.
        """
        info = {
            "installed": False,
            "product_name": "No instalado",
            "version": "",
            "architecture": "x64",
            "channel": "Current",
            "installed_apps": [],
            "missing_apps": []
        }

        # 1. Consultar registro ClickToRun
        try:
            key_path = r"SOFTWARE\Microsoft\Office\ClickToRun\Configuration"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
            try:
                version, _ = winreg.QueryValueEx(key, "VersionToReport")
                info["version"] = version
                info["installed"] = True
            except OSError:
                pass

            try:
                platform, _ = winreg.QueryValueEx(key, "Platform")
                info["architecture"] = platform
            except OSError:
                pass

            try:
                prod_ids, _ = winreg.QueryValueEx(key, "ProductReleaseIds")
                info["product_name"] = prod_ids
            except OSError:
                pass

            winreg.CloseKey(key)
        except Exception:
            pass

        # 2. Consultar Desinstaladores de Windows si el registro C2R no dio nombre amigable
        if not info["installed"] or info["product_name"] == "No instalado":
            uninstall_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            for u_path in uninstall_paths:
                try:
                    u_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, u_path, 0, winreg.KEY_READ)
                    for i in range(winreg.QueryInfoKey(u_key)[0]):
                        sub_name = winreg.EnumKey(u_key, i)
                        sub_k = winreg.OpenKey(u_key, sub_name, 0, winreg.KEY_READ)
                        try:
                            display_name, _ = winreg.QueryValueEx(sub_k, "DisplayName")
                            if "Microsoft Office" in display_name or "Microsoft 365" in display_name:
                                info["installed"] = True
                                info["product_name"] = display_name
                                try:
                                    disp_ver, _ = winreg.QueryValueEx(sub_k, "DisplayVersion")
                                    info["version"] = disp_ver
                                except Exception:
                                    pass
                                winreg.CloseKey(sub_k)
                                break
                        except OSError:
                            pass
                        winreg.CloseKey(sub_k)
                    winreg.CloseKey(u_key)
                except Exception:
                    pass

        # 3. Detectar qué ejecutables de Office están presentes en el disco
        found_apps = []
        for app_name, exe_list in cls.OFFICE_APPS.items():
            app_found = False
            for root in cls.ROOT_PATHS:
                for exe in exe_list:
                    full_p = os.path.join(root, exe)
                    if os.path.exists(full_p):
                        app_found = True
                        break
                if app_found:
                    break
            if app_found:
                found_apps.append(app_name)

        if found_apps and not info["installed"]:
            info["installed"] = True
            info["product_name"] = "Microsoft Office (Detectado por binarios)"

        info["installed_apps"] = found_apps
        info["missing_apps"] = [a for a in cls.OFFICE_APPS if a not in found_apps]

        return info
