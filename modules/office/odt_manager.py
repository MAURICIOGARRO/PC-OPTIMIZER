import os
import subprocess
import requests
import xml.etree.ElementTree as ET
from core.logger import logger

class OfficeODTManager:
    """Gestor oficial de Office Deployment Tool (ODT) para instalación personalizada y modular."""

    ALL_APPS = [
        "Word",
        "Excel",
        "PowerPoint",
        "Outlook",
        "Access",
        "Publisher",
        "OneNote",
        "Teams",
        "OneDrive",
        "Groove",
        "Lync"
    ]

    ODT_URL = "https://download.microsoft.com/download/2/7/A/27AF1BE6-DD20-4CB4-B154-EBAB8A7D4A7E/officedeploymenttool_17328-20162.exe"

    @classmethod
    def get_work_dir(cls) -> str:
        base_dir = os.path.join(os.environ.get("LOCALAPPDATA", "C:\\"), "OptiCore", "ODT")
        os.makedirs(base_dir, exist_ok=True)
        return base_dir

    @classmethod
    def ensure_setup_exe(cls) -> str:
        """Verifica o descarga y extrae el setup.exe oficial de Microsoft ODT."""
        work_dir = cls.get_work_dir()
        setup_exe = os.path.join(work_dir, "setup.exe")
        if os.path.exists(setup_exe):
            return setup_exe

        logger.info("Descargando herramienta oficial de despliegue de Microsoft Office (ODT)...")
        installer_path = os.path.join(work_dir, "odt_installer.exe")
        try:
            r = requests.get(cls.ODT_URL, stream=True, timeout=30)
            with open(installer_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info("Extrayendo setup.exe oficial...")
            # El instalador de ODT es autoextraíble con /quiet /extract:ruta
            extract_cmd = f'"{installer_path}" /quiet /extract:"{work_dir}"'
            subprocess.run(
                extract_cmd,
                shell=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            if os.path.exists(setup_exe):
                logger.success("Setup.exe de Office listo para usar.")
                return setup_exe
            else:
                logger.error("No se pudo localizar setup.exe tras la extracción.")
                return ""
        except Exception as e:
            logger.error(f"Error al descargar/extraer ODT: {e}")
            return ""

    @classmethod
    def generate_config_xml(
        cls,
        selected_apps: list,
        edition: str = "ProPlus2021Retail",
        arch: str = "64",
        lang: str = "es-es"
    ) -> str:
        """
        Genera el archivo configuration.xml excluyendo todas las apps NO seleccionadas.
        Si sólo se marcó 'PowerPoint', todas las demás se excluyen.
        """
        work_dir = cls.get_work_dir()
        xml_path = os.path.join(work_dir, "configuration.xml")

        # Excluir todo lo que NO esté en selected_apps
        excluded = [app for app in cls.ALL_APPS if app not in selected_apps]

        xml_lines = [
            '<Configuration>',
            f'  <Add OfficeClientEdition="{arch}" Channel="Current">',
            f'    <Product ID="{edition}">',
            f'      <Language ID="{lang}" />'
        ]

        for exc in excluded:
            xml_lines.append(f'      <ExcludeApp ID="{exc}" />')

        xml_lines.extend([
            '    </Product>',
            '  </Add>',
            '  <Display Level="Full" AcceptEULA="TRUE" />',
            '  <Property Name="AUTOACTIVATE" Value="0" />',
            '</Configuration>'
        ])

        xml_content = "\n".join(xml_lines)
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        logger.info(f"Configuración XML generada. Apps a instalar: {', '.join(selected_apps)}")
        return xml_path

    @classmethod
    def install_custom_office(
        cls,
        selected_apps: list,
        edition: str = "ProPlus2021Retail",
        arch: str = "64",
        lang: str = "es-es",
        on_finish=None
    ):
        """Descarga e inicia la instalación con los componentes seleccionados."""
        setup_exe = cls.ensure_setup_exe()
        if not setup_exe:
            logger.error("No fue posible obtener el instalador oficial de Microsoft.")
            if on_finish:
                on_finish(False)
            return

        xml_path = cls.generate_config_xml(selected_apps, edition, arch, lang)

        logger.info("Iniciando instalador oficial de Microsoft Office con tu selección...")
        logger.info("Aparecerá la ventana oficial de instalación de Office. Por favor espera.")

        def run():
            try:
                cmd = f'"{setup_exe}" /configure "{xml_path}"'
                res = subprocess.run(
                    cmd,
                    shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                if res.returncode == 0:
                    logger.success("¡Instalación de Office completada con éxito!")
                    if on_finish:
                        on_finish(True)
                else:
                    logger.warning(f"El instalador de Office finalizó con código {res.returncode}.")
                    if on_finish:
                        on_finish(False)
            except Exception as e:
                logger.error(f"Error al ejecutar instalador: {e}")
                if on_finish:
                    on_finish(False)

        import threading
        t = threading.Thread(target=run, daemon=True)
        t.start()
        return t
