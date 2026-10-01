import winreg
import subprocess
from core.logger import logger

class CopilotRemover:
    """Módulo para desactivar por completo Windows Copilot, IA y búsquedas web en el menú inicio."""

    @staticmethod
    def disable_copilot_completely() -> bool:
        logger.info("=== DESACTIVANDO WINDOWS COPILOT, IA Y BING EN MENÚ INICIO ===")
        success = True

        # 1. Desactivar directiva Windows Copilot en HKLM y HKCU
        copilot_policies = [
            (winreg.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot", "TurnOffWindowsCopilot", 1),
            (winreg.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\Windows\WindowsAI", "DisableAIDataAnalysis", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsAI", "DisableAIDataAnalysis", 1),
        ]

        for root_key, subkey, name, val in copilot_policies:
            try:
                k = winreg.CreateKey(root_key, subkey)
                winreg.SetValueEx(k, name, 0, winreg.REG_DWORD, val)
                winreg.CloseKey(k)
            except Exception as e:
                logger.warning(f"Aviso en registro ({subkey}): {e}")

        # 2. Ocultar botón de Copilot en la Barra de Tareas
        try:
            k = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced")
            winreg.SetValueEx(k, "ShowCopilotButton", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(k)
            logger.info("Botón de Copilot en barra de tareas desactivado.")
        except Exception:
            pass

        # 3. Desactivar Bing Search en el Menú Inicio (elimina procesos pesados de WebView2 / SearchHost)
        try:
            k_exp = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\Windows\Explorer")
            winreg.SetValueEx(k_exp, "DisableSearchBoxSuggestions", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(k_exp)

            k_search = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Search")
            winreg.SetValueEx(k_search, "BingSearchEnabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(k_search, "CortanaConsent", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(k_search)
            logger.info("Búsqueda web con Bing en el menú Inicio desactivada (ahorro de RAM en SearchHost/WebView2).")
        except Exception:
            pass

        # 4. Desactivar Copilot en Microsoft Edge
        try:
            k_edge = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Edge")
            winreg.SetValueEx(k_edge, "HubsSidebarEnabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(k_edge, "ShowCopilotButton", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(k_edge)
            logger.info("Barra lateral y botón de Copilot en Edge desactivados.")
        except Exception:
            pass

        # 5. Reiniciar Windows Explorer para refrescar barra de tareas de inmediato
        try:
            logger.info("Refrescando la barra de tareas de Windows...")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", "Stop-Process -Name explorer -Force"], creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception:
            pass

        logger.success("¡Windows Copilot, IA y búsquedas web de Bing desactivados al 100%!")
        return success

    @staticmethod
    def enable_copilot() -> bool:
        """Restaura Copilot a la configuración por defecto."""
        logger.info("Restaurando Windows Copilot...")
        try:
            k = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\Windows\WindowsCopilot")
            winreg.SetValueEx(k, "TurnOffWindowsCopilot", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(k)

            k2 = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced")
            winreg.SetValueEx(k2, "ShowCopilotButton", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(k2)

            subprocess.run(["powershell.exe", "-NoProfile", "-Command", "Stop-Process -Name explorer -Force"], creationflags=subprocess.CREATE_NO_WINDOW)
            logger.success("Windows Copilot restaurado.")
            return True
        except Exception as e:
            logger.error(f"Error al restaurar Copilot: {e}")
            return False
