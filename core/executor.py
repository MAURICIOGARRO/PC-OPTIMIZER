import subprocess
import threading
from typing import Callable, Optional
from core.logger import logger

class CommandExecutor:
    """Ejecutor de comandos en segundo plano con transmisión de salida en tiempo real."""

    @staticmethod
    def run_command(
        cmd: list or str,
        on_line: Optional[Callable[[str], None]] = None,
        on_finish: Optional[Callable[[int], None]] = None,
        is_powershell: bool = False
    ) -> threading.Thread:
        """
        Ejecuta un comando en un hilo separado para no bloquear la interfaz gráfica.
        """
        def worker():
            try:
                if is_powershell:
                    if isinstance(cmd, list):
                        ps_cmd = " ".join(cmd)
                    else:
                        ps_cmd = cmd
                    full_cmd = [
                        "powershell.exe",
                        "-NoProfile",
                        "-ExecutionPolicy", "Bypass",
                        "-Command", ps_cmd
                    ]
                else:
                    full_cmd = cmd

                # Configurar subprocess para captura en tiempo real
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

                process = subprocess.Popen(
                    full_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    text=True,
                    encoding="cp850",
                    errors="replace",
                    bufsize=1,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                for line in iter(process.stdout.readline, ''):
                    clean_line = line.strip()
                    if clean_line:
                        logger.info(clean_line)
                        if on_line:
                            try:
                                on_line(clean_line)
                            except Exception:
                                pass

                process.stdout.close()
                retcode = process.wait()

                if on_finish:
                    on_finish(retcode)
                return retcode

            except Exception as e:
                logger.error(f"Error al ejecutar comando: {e}")
                if on_finish:
                    on_finish(-1)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread

    @staticmethod
    def run_sync(cmd: str, is_powershell: bool = True) -> str:
        """Ejecuta un comando de forma síncrona y retorna la salida."""
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            if is_powershell:
                full_cmd = [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy", "Bypass",
                    "-Command", cmd
                ]
            else:
                full_cmd = cmd

            res = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                encoding="cp850",
                errors="replace",
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=30
            )
            return res.stdout.strip()
        except Exception as e:
            return ""
