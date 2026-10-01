import subprocess
import json

class SmartDiskAnalyzer:
    """Módulo para consultar el estado de salud físico de los discos (SMART)."""

    @staticmethod
    def get_disks_health() -> list:
        disks = []
        try:
            cmd = (
                "Get-PhysicalDisk | Select-Object FriendlyName, MediaType, "
                "HealthStatus, OperationalStatus, Size | ConvertTo-Json"
            )
            res = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=10
            )

            if not res.stdout.strip():
                return disks

            data = json.loads(res.stdout)
            if isinstance(data, dict):
                data = [data]

            for d in data:
                size_gb = round(d.get("Size", 0) / (1024**3), 1)
                health = d.get("HealthStatus", "Healthy")
                disks.append({
                    "name": d.get("FriendlyName", "Disco Desconocido"),
                    "type": d.get("MediaType", "SSD/HDD"),
                    "health": health,
                    "status": d.get("OperationalStatus", "OK"),
                    "size_gb": size_gb,
                    "is_ok": health.lower() == "healthy"
                })
        except Exception:
            # Fallback en caso de que Get-PhysicalDisk falle
            try:
                cmd_wmic = "wmic diskdrive get model, status /format:csv"
                res_w = subprocess.run(cmd_wmic, shell=True, capture_output=True, text=True, timeout=5)
                lines = [l.strip() for l in res_w.stdout.splitlines() if l.strip()]
                for l in lines[1:]:
                    parts = l.split(",")
                    if len(parts) >= 3:
                        disks.append({
                            "name": parts[1],
                            "type": "Almacenamiento",
                            "health": parts[2],
                            "status": parts[2],
                            "size_gb": 0,
                            "is_ok": parts[2].lower() == "ok"
                        })
            except Exception:
                pass

        return disks
