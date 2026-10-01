import subprocess
import threading
from core.logger import logger
from core.executor import CommandExecutor

class WingetAppInstaller:
    """Módulo para instalar aplicaciones esenciales desatendidas vía Winget."""

    ESSENTIAL_APPS = [
        {"cat": "Navegadores", "id": "Google.Chrome", "name": "Google Chrome", "desc": "Navegador web rápido y seguro"},
        {"cat": "Navegadores", "id": "Mozilla.Firefox", "name": "Mozilla Firefox", "desc": "Navegador web enfocado en privacidad"},
        {"cat": "Navegadores", "id": "Brave.Brave", "name": "Brave Browser", "desc": "Navegador con bloqueo nativo de anuncios"},
        
        {"cat": "Compresores", "id": "7zip.7zip", "name": "7-Zip", "desc": "Compresor y descompresor universal libre"},
        {"cat": "Compresores", "id": "RARLab.WinRAR", "name": "WinRAR", "desc": "Gestor de archivos comprimidos RAR y ZIP"},

        {"cat": "Multimedia", "id": "VideoLAN.VLC", "name": "VLC Media Player", "desc": "Reproductor universal de vídeo y audio"},
        {"cat": "Multimedia", "id": "Spotify.Spotify", "name": "Spotify", "desc": "Streaming de música digital"},

        {"cat": "Productividad", "id": "Notepad++.Notepad++", "name": "Notepad++", "desc": "Editor de texto avanzado y ligero"},
        {"cat": "Productividad", "id": "Adobe.Acrobat.Reader.64-bit", "name": "Adobe Acrobat Reader", "desc": "Visor estándar de documentos PDF"},
        {"cat": "Productividad", "id": "AnyDeskSoftwareGmbH.AnyDesk", "name": "AnyDesk", "desc": "Control remoto y soporte técnico"},

        {"cat": "Desarrollo & Gaming", "id": "Microsoft.VisualStudioCode", "name": "Visual Studio Code", "desc": "Editor de código profesional"},
        {"cat": "Desarrollo & Gaming", "id": "Git.Git", "name": "Git", "desc": "Control de versiones para desarrolladores"},
        {"cat": "Desarrollo & Gaming", "id": "Discord.Discord", "name": "Discord", "desc": "Comunicación por voz y chat"},
        {"cat": "Desarrollo & Gaming", "id": "Valve.Steam", "name": "Steam", "desc": "Plataforma de videojuegos"}
    ]

    @classmethod
    def install_app(cls, app_id: str, on_finish=None) -> threading.Thread:
        """Instala una app desatendida mediante winget."""
        logger.info(f"Iniciando instalación silenciosa de {app_id} vía Winget...")
        cmd = [
            "winget", "install",
            "--id", app_id,
            "--silent",
            "--accept-package-agreements",
            "--accept-source-agreements"
        ]
        def _done(code):
            if code == 0:
                logger.success(f"¡{app_id} se instaló correctamente!")
            else:
                logger.warning(f"Winget finalizó para {app_id} con código {code}.")
            if on_finish:
                on_finish(code == 0)

        return CommandExecutor.run_command(cmd, on_finish=_done)
