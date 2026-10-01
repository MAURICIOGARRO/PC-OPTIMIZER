import subprocess
import winreg

class SecurityAuditor:
    """Módulo de auditoría de seguridad esencial de Windows (Defender, Firewall, UAC)."""

    @staticmethod
    def audit_security() -> dict:
        results = {
            "defender_realtime": True,
            "firewall_active": True,
            "uac_enabled": True,
            "warnings": []
        }

        # 1. Comprobar Windows Defender
        try:
            cmd = "Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled"
            res = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=8
            )
            val = res.stdout.strip().lower()
            if "false" in val:
                results["defender_realtime"] = False
                results["warnings"].append("La protección en tiempo real de Windows Defender está desactivada.")
        except Exception:
            pass

        # 2. Comprobar Firewall
        try:
            cmd_fw = "Get-NetFirewallProfile | Where-Object {$_.Enabled -eq 'False'}"
            res_fw = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd_fw],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=8
            )
            if res_fw.stdout.strip():
                results["firewall_active"] = False
                results["warnings"].append("Uno o más perfiles del Firewall de Windows están deshabilitados.")
        except Exception:
            pass

        # 3. Comprobar UAC (Control de Cuentas de Usuario)
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                0,
                winreg.KEY_READ
            )
            val, _ = winreg.QueryValueEx(key, "EnableLUA")
            winreg.CloseKey(key)
            if val == 0:
                results["uac_enabled"] = False
                results["warnings"].append("El Control de Cuentas de Usuario (UAC) se encuentra completamente desactivado.")
        except Exception:
            pass

        return results
