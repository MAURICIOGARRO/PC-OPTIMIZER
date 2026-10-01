import subprocess
from core.logger import logger

class WindowsDebloater:
    """Módulo para remover bloatware y aplicaciones basura preinstaladas en Windows."""

    COMMON_BLOATWARE = [
        {"id": "Microsoft.3DBuilder", "name": "3D Builder", "desc": "Visor y editor 3D básico"},
        {"id": "Microsoft.Microsoft3DViewer", "name": "Visor 3D", "desc": "Visor de modelos 3D"},
        {"id": "Microsoft.BingNews", "name": "Noticias Bing", "desc": "Feed de noticias de Microsoft"},
        {"id": "Microsoft.BingWeather", "name": "El Tiempo Bing", "desc": "Clima de Bing"},
        {"id": "Microsoft.BingFinance", "name": "Finanzas Bing", "desc": "Cotizaciones y finanzas"},
        {"id": "Microsoft.BingSports", "name": "Deportes Bing", "desc": "Noticias deportivas"},
        {"id": "Microsoft.GetHelp", "name": "Obtener Ayuda", "desc": "Asistente de ayuda"},
        {"id": "Microsoft.Getstarted", "name": "Primeros Pasos", "desc": "Consejos y sugerencias"},
        {"id": "Microsoft.MicrosoftSolitaireCollection", "name": "Solitario", "desc": "Juegos con publicidad"},
        {"id": "Microsoft.People", "name": "Contactos", "desc": "Libreta de contactos de Windows"},
        {"id": "Microsoft.SkypeApp", "name": "Skype", "desc": "App de videollamadas clásica"},
        {"id": "Microsoft.ZuneMusic", "name": "Groove Música", "desc": "Reproductor heredado"},
        {"id": "Microsoft.ZuneVideo", "name": "Películas y TV", "desc": "Reproductor multimedia de tienda"},
        {"id": "Microsoft.XboxTCUI", "name": "Xbox UI", "desc": "Interfaz complementaria de Xbox"},
        {"id": "Microsoft.XboxGameOverlay", "name": "Xbox Game Overlay", "desc": "Superposición de Xbox"},
    ]

    @classmethod
    def get_installed_bloatware(cls) -> list:
        """Verifica cuáles de estas aplicaciones están instaladas en la máquina."""
        found = []
        try:
            cmd = "Get-AppxPackage | Select-Object -ExpandProperty Name"
            res = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=10
            )
            installed_names = res.stdout.lower()
            for item in cls.COMMON_BLOATWARE:
                if item["id"].lower() in installed_names:
                    found.append(item)
        except Exception:
            pass
        return found

    @classmethod
    def remove_app(cls, app_id: str) -> bool:
        """Desinstala una aplicación específica mediante Remove-AppxPackage."""
        logger.info(f"Desinstalando bloatware: {app_id}...")
        try:
            cmd = f"Get-AppxPackage -Name '*{app_id}*' | Remove-AppxPackage -ErrorAction SilentlyContinue"
            subprocess.run(
                ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=30
            )
            logger.success(f"App {app_id} desinstalada correctamente.")
            return True
        except Exception as e:
            logger.error(f"Error al desinstalar {app_id}: {e}")
            return False

    @classmethod
    def remove_selected(cls, app_ids: list) -> int:
        count = 0
        for aid in app_ids:
            if cls.remove_app(aid):
                count += 1
        return count
