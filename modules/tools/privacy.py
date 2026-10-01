import subprocess
import winreg
from core.logger import logger

class WindowsPrivacy:
    """Módulo de privacidad y desactivación de telemetría y rastreo de Windows."""

    @staticmethod
    def apply_privacy_tweaks() -> bool:
        logger.info("=== APLICANDO AJUSTES DE PRIVACIDAD Y DES-TELEMETRÍA ===")
        success = True

        # 1. Desactivar servicios de telemetría de Windows (DiagTrack y dmwappushservice)
        telemetry_services = ["DiagTrack", "dmwappushservice"]
        for s in telemetry_services:
            try:
                logger.info(f"Desactivando servicio de rastreo: {s}...")
                subprocess.run(["sc", "stop", s], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                subprocess.run(["sc", "config", s, "start=", "disabled"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception:
                pass

        # 2. Desactivar datos de diagnóstico en registro (AllowTelemetry = 0)
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection")
            winreg.SetValueEx(key, "AllowTelemetry", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            logger.info("Telemetría de datos de diagnóstico configurada al mínimo.")
        except Exception as e:
            logger.warning(f"Aviso en DataCollection: {e}")

        # 3. Desactivar publicidad y apps sugeridas en el Menú Inicio
        try:
            key_content = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager")
            winreg.SetValueEx(key_content, "SystemPaneSuggestionsEnabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key_content, "SubscribedContent-338388Enabled", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key_content, "SubscribedContent-338389Enabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key_content)
            logger.info("Publicidad y recomendaciones del menú inicio desactivadas.")
        except Exception:
            pass

        # 4. Desactivar ID de anuncios para apps
        try:
            key_adv = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo")
            winreg.SetValueEx(key_adv, "Enabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key_adv)
            logger.info("ID de publicidad personalizado desactivado.")
        except Exception:
            pass

        logger.success("¡Ajustes de privacidad y des-telemetría aplicados con éxito!")
        return success
