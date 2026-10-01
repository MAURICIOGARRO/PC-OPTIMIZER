import subprocess
import psutil
import json
from core.logger import logger

class OEMDebloater:
    """
    Módulo universal multi-fabricante de alto rendimiento para detectar y desactivar
    servicios, procesos en segundo plano y telemetría de cualquier marca de PC:
    Lenovo, HP, Dell, ASUS, Acer, MSI, Samsung, Razer, etc.
    """

    OEM_CATALOG = {
        "Lenovo": {
            "services": [
                "ImControllerService",
                "LenovoUtilityService",
                "LenovoFnAndFunctionKeys",
                "LNVGService",
                "LenovoVantageService"
            ],
            "processes": [
                "Lenovo.Modern.ImController.exe",
                "LenovoUtilityService.exe",
                "LenovoFnAndFunctionKeys.exe",
                "LenovoVantage.exe"
            ],
            "task_paths": ["\\Lenovo*"]
        },
        "HP": {
            "services": [
                "HpTouchpointAnalyticsService",
                "HPAppHelperCap",
                "HPDiagsCap",
                "HPNetworkCap",
                "HPSysInfoCap",
                "HPCommRecovery",
                "HP Support Solutions Framework Service"
            ],
            "processes": [
                "TouchpointAnalyticsClient.exe",
                "HPAudioSwitch.exe",
                "HP.Omen.OmenCommandCenter.exe",
                "HPSupportSolutionsFrameworkService.exe"
            ],
            "task_paths": ["\\Hewlett-Packard*", "\\HP*"]
        },
        "Dell": {
            "services": [
                "DellDataVault",
                "DellDataVaultWDA",
                "SupportAssistAgent",
                "DellClientManagementService",
                "DellTechHub",
                "DellOptimizerCore"
            ],
            "processes": [
                "SupportAssistAgent.exe",
                "DellDataVault.exe",
                "Dell.TechHub.exe",
                "DellOptimizer.exe"
            ],
            "task_paths": ["\\Dell*"]
        },
        "ASUS": {
            "services": [
                "ArmouryCrateControlInterface",
                "AsusSystemAnalysis",
                "AsusSystemDiagnosis",
                "ASUSOptimization",
                "AsusLinkNearService",
                "ROG Live Service"
            ],
            "processes": [
                "ArmouryCrate.exe",
                "AsusSystemAnalysis.exe",
                "AsusSystemDiagnosis.exe"
            ],
            "task_paths": ["\\ASUS*"]
        },
        "Acer": {
            "services": [
                "AcerCareCenterService",
                "ACCService",
                "AcerQuickAccessService"
            ],
            "processes": [
                "AcerCareCenter.exe",
                "AcerQuickAccess.exe"
            ],
            "task_paths": ["\\Acer*"]
        },
        "MSI": {
            "services": [
                "MSI Central Service",
                "MSIDragonCenter",
                "MSI_Central_Service"
            ],
            "processes": [
                "MSICenter.exe",
                "DragonCenter.exe"
            ],
            "task_paths": ["\\MSI*"]
        },
        "Razer": {
            "services": [
                "Razer Synapse Service",
                "Razer Game Manager",
                "Razer Central Service"
            ],
            "processes": [
                "RazerSynapse.exe",
                "RazerCentral.exe"
            ],
            "task_paths": ["\\Razer*"]
        }
    }

    _cached_hw = None

    @classmethod
    def get_hardware_identity(cls) -> dict:
        """Detecta fabricante y modelo exacto del equipo actual."""
        if cls._cached_hw:
            return cls._cached_hw

        manufacturer = "Genérico"
        model = "PC"
        try:
            cmd = "Get-CimInstance Win32_ComputerSystem | Select-Object -Property Manufacturer, Model | ConvertTo-Json"
            res = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=5
            )
            data = json.loads(res.stdout)
            if isinstance(data, dict):
                manufacturer = data.get("Manufacturer", "Genérico").strip()
                model = data.get("Model", "PC").strip()
        except Exception:
            pass

        cls._cached_hw = {
            "manufacturer": manufacturer,
            "model": model,
            "full_name": f"{manufacturer} {model}"
        }
        return cls._cached_hw

    @classmethod
    def scan_installed_oem_bloat(cls) -> dict:
        """
        Escaneo ultrarrápido nativo (sin llamadas repetidas a PowerShell)
        de procesos y servicios OEM activos en este equipo.
        """
        found_services = []
        found_processes = []
        target_brands = set()

        # 1. Escanear Procesos Activos en RAM
        for p in psutil.process_iter(['name', 'pid', 'memory_info']):
            try:
                pname = p.info['name']
                if not pname:
                    continue
                for brand, data in cls.OEM_CATALOG.items():
                    for proc_pattern in data["processes"]:
                        if proc_pattern.lower() in pname.lower():
                            mem_mb = round(p.info['memory_info'].rss / (1024 * 1024), 1)
                            found_processes.append({
                                "brand": brand,
                                "name": pname,
                                "pid": p.info['pid'],
                                "mem_mb": mem_mb
                            })
                            target_brands.add(brand)
            except Exception:
                pass

        # 2. Escaneo nativo ultrarrápido con sc.exe query
        for brand, data in cls.OEM_CATALOG.items():
            for s_name in data["services"]:
                try:
                    res = subprocess.run(
                        ["sc.exe", "query", s_name],
                        capture_output=True,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        timeout=1
                    )
                    if res.returncode == 0:
                        status = "ACTIVO" if "RUNNING" in res.stdout else "INSTALADO"
                        found_services.append({
                            "brand": brand,
                            "name": s_name,
                            "status": status
                        })
                        target_brands.add(brand)
                except Exception:
                    pass

        return {
            "hardware": cls.get_hardware_identity(),
            "detected_brands": list(target_brands),
            "services": found_services,
            "processes": found_processes,
            "total_items": len(found_services) + len(found_processes)
        }

    @classmethod
    def disable_all_oem_bloat(cls) -> dict:
        """
        Detiene y deshabilita todos los servicios y tareas programadas
        de telemetría de fabricantes (OEM) encontrados en el equipo.
        """
        hw = cls.get_hardware_identity()
        logger.info(f"=== DESACTIVANDO TELEMETRÍA Y SERVICIOS OEM PARA: {hw['full_name']} ===")

        stopped_procs = 0
        disabled_services = 0

        # 1. Terminar procesos activos
        for p in psutil.process_iter(['name']):
            try:
                pname = p.info['name']
                if not pname:
                    continue
                for brand, data in cls.OEM_CATALOG.items():
                    for proc_pattern in data["processes"]:
                        if proc_pattern.lower() in pname.lower():
                            p.terminate()
                            stopped_procs += 1
                            logger.info(f"[{brand}] Proceso cerrado: {pname}")
            except Exception:
                pass

        # 2. Deshabilitar y detener servicios
        for brand, data in cls.OEM_CATALOG.items():
            for s_name in data["services"]:
                try:
                    res_chk = subprocess.run(
                        ["sc.exe", "query", s_name],
                        capture_output=True,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    if res_chk.returncode == 0:
                        subprocess.run(["sc.exe", "stop", s_name], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        subprocess.run(["sc.exe", "config", s_name, "start=", "disabled"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        disabled_services += 1
                        logger.info(f"[{brand}] Servicio deshabilitado: {s_name}")
                except Exception:
                    pass

        # 3. Desactivar tareas programadas
        for brand, data in cls.OEM_CATALOG.items():
            for t_path in data.get("task_paths", []):
                try:
                    cmd_tasks = f"Get-ScheduledTask -TaskPath '{t_path}' -ErrorAction SilentlyContinue | Disable-ScheduledTask"
                    subprocess.run(
                        ["powershell.exe", "-NoProfile", "-Command", cmd_tasks],
                        capture_output=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                except Exception:
                    pass

        logger.success(
            f"¡Limpieza OEM completada! Se deshabilitaron {disabled_services} servicios de fabricante "
            f"y se finalizaron {stopped_procs} procesos de fondo."
        )

        return {
            "disabled_services": disabled_services,
            "stopped_procs": stopped_procs
        }

    @classmethod
    def enable_all_oem_bloat(cls) -> bool:
        """Restaura los servicios de fabricantes a inicio automático si se necesitan."""
        logger.info("Restableciendo servicios de fabricante a inicio automático...")
        for brand, data in cls.OEM_CATALOG.items():
            for s_name in data["services"]:
                try:
                    subprocess.run(["sc.exe", "config", s_name, "start=", "auto"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    subprocess.run(["sc.exe", "start", s_name], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                except Exception:
                    pass

            for t_path in data.get("task_paths", []):
                try:
                    cmd_tasks = f"Get-ScheduledTask -TaskPath '{t_path}' -ErrorAction SilentlyContinue | Enable-ScheduledTask"
                    subprocess.run(["powershell.exe", "-NoProfile", "-Command", cmd_tasks], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                except Exception:
                    pass

        logger.success("Servicios de fabricantes restablecidos a automático.")
        return True
