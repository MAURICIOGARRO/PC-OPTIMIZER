import winreg
from core.logger import logger

class LatencyTweaks:
    """Módulo de optimización de latencia de red, juegos y respuesta del sistema."""

    @staticmethod
    def apply_latency_tweaks() -> bool:
        """Aplica configuraciones en el registro para mejorar la respuesta y reducir input lag."""
        logger.info("Aplicando optimizaciones de latencia y juegos...")
        success = True

        # 1. Desactivar limitación de red multimedia (Network Throttling)
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile")
            winreg.SetValueEx(key, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 0xffffffff)
            winreg.SetValueEx(key, "SystemResponsiveness", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            logger.info("Optimizado Network Throttling y System Responsiveness (Prioridad a apps en primer plano).")
        except Exception as e:
            logger.warning(f"No se pudo ajustar SystemProfile: {e}")
            success = False

        # 2. Desactivar Game DVR y capturas en segundo plano (elimina micro-stutters)
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore")
            winreg.SetValueEx(key, "GameDVR_Enabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)

            key2 = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\GameDVR")
            winreg.SetValueEx(key2, "AllowGameDVR", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key2)
            logger.info("Desactivada grabación en segundo plano de Game DVR.")
        except Exception as e:
            logger.warning(f"No se pudo ajustar GameDVR: {e}")

        # 3. Optimización de entrega de Windows Update (evitar que use tu ancho de banda para subir datos)
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config")
            winreg.SetValueEx(key, "DODownloadMode", 0, winreg.REG_DWORD, 0)  # Solo HTTP, no P2P
            winreg.CloseKey(key)
            logger.info("Desactivado P2P de Delivery Optimization (ahorro de ancho de banda).")
        except Exception:
            pass

        if success:
            logger.success("Optimizaciones de latencia aplicadas correctamente.")
        return success
