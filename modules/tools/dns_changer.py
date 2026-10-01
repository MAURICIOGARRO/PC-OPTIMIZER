import subprocess
import re
from core.logger import logger

class DNSChanger:
    """Módulo para cambiar servidores DNS rápidamente y medir latencia."""

    PRESETS = {
        "Cloudflare": {
            "name": "Cloudflare DNS (1.1.1.1)",
            "primary": "1.1.1.1",
            "secondary": "1.0.0.1",
            "desc": "Máxima velocidad y privacidad garantizada."
        },
        "Google": {
            "name": "Google Public DNS (8.8.8.8)",
            "primary": "8.8.8.8",
            "secondary": "8.8.4.4",
            "desc": "Alta estabilidad y compatibilidad global."
        },
        "AdGuard": {
            "name": "AdGuard DNS (Anti-Publicidad)",
            "primary": "94.140.14.14",
            "secondary": "94.140.15.15",
            "desc": "Bloquea publicidad y rastreadores en todo el equipo sin extensiones."
        },
        "Quad9": {
            "name": "Quad9 DNS (Anti-Malware)",
            "primary": "9.9.9.9",
            "secondary": "149.112.112.112",
            "desc": "Bloquea dominios maliciosos, phishing y estafas."
        }
    }

    @classmethod
    def set_dns(cls, preset_key: str) -> bool:
        """Aplica el DNS seleccionado a los adaptadores de red activos."""
        try:
            if preset_key == "DHCP":
                logger.info("Restableciendo DNS a Automático (DHCP)...")
                cmd = "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Set-DnsClientServerAddress -ResetServerAddresses"
            else:
                preset = cls.PRESETS[preset_key]
                primary = preset["primary"]
                secondary = preset["secondary"]
                logger.info(f"Configurando {preset['name']}: {primary}, {secondary}...")
                cmd = (
                    f"Get-NetAdapter | Where-Object {{$_.Status -eq 'Up'}} | "
                    f"Set-DnsClientServerAddress -ServerAddresses ('{primary}','{secondary}')"
                )

            res = subprocess.run(
                ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Vaciar DNS para aplicar de inmediato
            subprocess.run(["ipconfig", "/flushdns"], creationflags=subprocess.CREATE_NO_WINDOW)

            if res.returncode == 0:
                logger.success(f"DNS actualizado con éxito.")
                return True
            else:
                logger.warning(f"Aviso al configurar DNS: {res.stderr.strip() or res.stdout.strip()}")
                return False
        except Exception as e:
            logger.error(f"Error al cambiar DNS: {e}")
            return False

    @staticmethod
    def ping_test(host: str) -> int:
        """Retorna la latencia en milisegundos hacia el servidor o -1 si falla."""
        try:
            res = subprocess.run(
                ["ping", "-n", "1", "-w", "1000", host],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # Buscar 'tiempo=XXms' o 'time=XXms'
            match = re.search(r'(?:tiempo|time)[=<]([0-9]+)\s*ms', res.stdout, re.IGNORECASE)
            if match:
                return int(match.group(1))
            return -1
        except Exception:
            return -1
