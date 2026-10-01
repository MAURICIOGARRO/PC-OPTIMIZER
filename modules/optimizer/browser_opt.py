import winreg
import subprocess
import psutil
import ctypes
from core.logger import logger

class GoogleChromeOptimizer:
    """Módulo de optimización y reducción extrema de consumo de recursos de Google Chrome."""

    @staticmethod
    def apply_chrome_optimizations() -> bool:
        """
        Aplica políticas en el registro para:
        1. Desactivar ejecución de Chrome en segundo plano al cerrar la ventana.
        2. Activar modo Ahorro de Memoria de alta eficiencia.
        3. Desactivar precarga innecesaria de páginas web (ahorro de RAM y red).
        4. Desactivar telemetría de métricas de Google.
        """
        logger.info("=== OPTIMIZANDO CONSUMO DE RECURSOS DE GOOGLE CHROME ===")
        success = True

        # Políticas en HKLM y HKCU
        keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Google\Chrome"),
            (winreg.HKEY_CURRENT_USER, r"Software\Policies\Google\Chrome"),
        ]

        for root_key, subkey in keys:
            try:
                k = winreg.CreateKey(root_key, subkey)
                # 1. BackgroundModeEnabled = 0 (No seguir ejecutando apps en 2do plano al cerrar)
                winreg.SetValueEx(k, "BackgroundModeEnabled", 0, winreg.REG_DWORD, 0)
                # 2. HighEfficiencyModeEnabled = 1 (Ahorro de Memoria activo)
                winreg.SetValueEx(k, "HighEfficiencyModeEnabled", 0, winreg.REG_DWORD, 1)
                # 3. NetworkPredictionOptions = 2 (Desactivar precarga de páginas)
                winreg.SetValueEx(k, "NetworkPredictionOptions", 0, winreg.REG_DWORD, 2)
                # 4. MetricsReportingEnabled = 0 (Desactivar telemetría)
                winreg.SetValueEx(k, "MetricsReportingEnabled", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(k)
            except Exception as e:
                logger.warning(f"Aviso en registro de Chrome: {e}")
                success = False

        # Configurar servicios de actualización de Google a manual (demand) para que no estén activos todo el tiempo
        try:
            logger.info("Configurando servicios de Google Update para que no corran constantemente de fondo...")
            cmd_services = (
                "Get-Service -Name '*googleupdater*', '*googlechrome*' -ErrorAction SilentlyContinue | "
                "Set-Service -StartupType Manual"
            )
            subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd_services],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception:
            pass

        if success:
            logger.success("¡Políticas de ahorro de memoria de Google Chrome aplicadas correctamente!")
            logger.info("Chrome ya no se quedará abierto en segundo plano y suspenderá pestañas inactivas.")
        return success

    @staticmethod
    def purge_chrome_memory() -> dict:
        """
        Llama a EmptyWorkingSet en todos los procesos activos de Google Chrome,
        reduciendo su consumo de RAM de inmediato sin cerrar tus pestañas ni ventanas.
        """
        logger.info("Purgando memoria RAM ocupada por procesos de Google Chrome...")
        freed_mb = 0
        pids_trimmed = 0

        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi

        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    initial_rss = proc.info['memory_info'].rss
                    handle = kernel32.OpenProcess(0x0400 | 0x0100, False, proc.info['pid'])
                    if handle:
                        if psapi.EmptyWorkingSet(handle):
                            pids_trimmed += 1
                            # Calcular reducción
                            try:
                                final_rss = proc.memory_info().rss
                                freed_mb += max(0, initial_rss - final_rss) / (1024 * 1024)
                            except Exception:
                                pass
                        kernel32.CloseHandle(handle)
            except Exception:
                pass

        freed_mb = round(freed_mb, 1)
        msg = f"¡Memoria de Chrome purgada! Se optimizaron {pids_trimmed} procesos de Chrome, liberando {freed_mb} MB de RAM."
        logger.success(msg)
        return {"processes": pids_trimmed, "freed_mb": freed_mb}

    @staticmethod
    def close_all_chrome_processes() -> int:
        """Cierra todos los procesos de Chrome (útil para limpiar procesos zombis colgados)."""
        logger.info("Cerrando procesos de Google Chrome...")
        killed = 0
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    proc.terminate()
                    killed += 1
            except Exception:
                pass
        logger.success(f"Se finalizaron {killed} procesos de Chrome.")
        return killed
