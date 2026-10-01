import threading
from core.logger import logger
from core.executor import CommandExecutor

class RuntimesInstaller:
    """Módulo para instalar Visual C++ All-In-One y librerías DirectX."""

    @classmethod
    def install_vc_redist(cls, on_finish=None) -> threading.Thread:
        logger.info("=== INSTALANDO VISUAL C++ REDISTRIBUTABLES (x64 y x86) ===")
        # Microsoft.VCRedist.2015+.x64 y x86
        def step2(code1):
            logger.info("Instalando Visual C++ x86...")
            cmd2 = ["winget", "install", "--id", "Microsoft.VCRedist.2015+.x86", "--silent", "--accept-package-agreements", "--accept-source-agreements"]
            CommandExecutor.run_command(cmd2, on_finish=on_finish)

        logger.info("Instalando Visual C++ x64...")
        cmd1 = ["winget", "install", "--id", "Microsoft.VCRedist.2015+.x64", "--silent", "--accept-package-agreements", "--accept-source-agreements"]
        return CommandExecutor.run_command(cmd1, on_finish=step2)

    @classmethod
    def install_directx(cls, on_finish=None) -> threading.Thread:
        logger.info("=== INSTALANDO DIRECTX END-USER RUNTIMES ===")
        cmd = ["winget", "install", "--id", "Microsoft.DirectX", "--silent", "--accept-package-agreements", "--accept-source-agreements"]
        return CommandExecutor.run_command(cmd, on_finish=on_finish)
