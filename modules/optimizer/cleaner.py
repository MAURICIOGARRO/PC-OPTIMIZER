import os
import shutil
import tempfile
import glob
from core.logger import logger

class SystemCleaner:
    """Módulo de escaneo y limpieza profunda de archivos temporales y basura."""

    @staticmethod
    def get_categories():
        user_profile = os.environ.get("USERPROFILE", "")
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        program_data = os.environ.get("PROGRAMDATA", "C:\\ProgramData")
        win_dir = os.environ.get("WINDIR", "C:\\Windows")

        return {
            "temp_user": {
                "name": "Temporales de Usuario",
                "paths": [tempfile.gettempdir()],
                "desc": "Archivos temporales generados por programas del usuario."
            },
            "temp_windows": {
                "name": "Temporales de Windows",
                "paths": [os.path.join(win_dir, "Temp")],
                "desc": "Archivos temporales del sistema operativo."
            },
            "prefetch": {
                "name": "Caché de Prefetch",
                "paths": [os.path.join(win_dir, "Prefetch")],
                "desc": "Rastros de ejecución antiguos del sistema."
            },
            "wupdate_cache": {
                "name": "Caché de Windows Update",
                "paths": [os.path.join(win_dir, "SoftwareDistribution", "Download")],
                "desc": "Instaladores descargados de actualizaciones pasadas."
            },
            "crash_dumps": {
                "name": "Volcados de Error (Dumps)",
                "paths": [
                    os.path.join(local_app_data, "CrashDumps"),
                    os.path.join(win_dir, "Minidump"),
                    os.path.join(program_data, "Microsoft", "Windows", "WER", "ReportQueue")
                ],
                "desc": "Reportes de fallos y cierres inesperados de aplicaciones."
            },
            "browser_cache": {
                "name": "Caché de Navegadores",
                "paths": [
                    os.path.join(local_app_data, "Google", "Chrome", "User Data", "Default", "Cache"),
                    os.path.join(local_app_data, "Microsoft", "Edge", "User Data", "Default", "Cache"),
                    os.path.join(local_app_data, "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cache"),
                    os.path.join(local_app_data, "Mozilla", "Firefox", "Profiles")
                ],
                "desc": "Archivos de imágenes y páginas web cacheadas."
            },
            "logs_windows": {
                "name": "Archivos de Registro (Logs)",
                "paths": [
                    os.path.join(win_dir, "Logs"),
                    os.path.join(win_dir, "Panther")
                ],
                "desc": "Historiales de texto y auditorías antiguas de Windows."
            }
        }

    @staticmethod
    def _calc_dir_size(path: str) -> tuple[int, int]:
        """Retorna (bytes_totales, cantidad_archivos) de un directorio de forma segura."""
        total_size = 0
        total_files = 0
        if not os.path.exists(path):
            return 0, 0
        try:
            for root, _, files in os.walk(path, onerror=lambda e: None):
                for f in files:
                    try:
                        fp = os.path.join(root, f)
                        if not os.path.islink(fp):
                            total_size += os.path.getsize(fp)
                            total_files += 1
                    except Exception:
                        pass
        except Exception:
            pass
        return total_size, total_files

    @classmethod
    def scan(cls) -> dict:
        """Escanea todas las categorías y devuelve el tamaño encontrado."""
        results = {}
        total_bytes = 0
        total_files = 0
        categories = cls.get_categories()

        for key, cat in categories.items():
            cat_bytes = 0
            cat_files = 0
            for p in cat["paths"]:
                if os.path.exists(p):
                    b, f = cls._calc_dir_size(p)
                    cat_bytes += b
                    cat_files += f

            results[key] = {
                "name": cat["name"],
                "desc": cat["desc"],
                "bytes": cat_bytes,
                "mb": round(cat_bytes / (1024 * 1024), 2),
                "files": cat_files
            }
            total_bytes += cat_bytes
            total_files += cat_files

        results["_summary"] = {
            "total_bytes": total_bytes,
            "total_mb": round(total_bytes / (1024 * 1024), 2),
            "total_files": total_files
        }
        return results

    @classmethod
    def clean(cls, categories_to_clean: list = None) -> dict:
        """Limpia las categorías seleccionadas de forma segura y devuelve lo liberado."""
        categories = cls.get_categories()
        if not categories_to_clean:
            categories_to_clean = list(categories.keys())

        freed_bytes = 0
        deleted_files = 0

        logger.info("Iniciando proceso de limpieza profunda del sistema...")

        for key in categories_to_clean:
            if key not in categories:
                continue

            cat = categories[key]
            logger.info(f"Limpiando: {cat['name']}...")

            for base_path in cat["paths"]:
                if not os.path.exists(base_path):
                    continue

                try:
                    for item in os.listdir(base_path):
                        item_path = os.path.join(base_path, item)
                        try:
                            if os.path.isfile(item_path) or os.path.islink(item_path):
                                size = os.path.getsize(item_path)
                                os.unlink(item_path)
                                freed_bytes += size
                                deleted_files += 1
                            elif os.path.isdir(item_path):
                                b, f = cls._calc_dir_size(item_path)
                                shutil.rmtree(item_path, ignore_errors=True)
                                freed_bytes += b
                                deleted_files += f
                        except Exception:
                            # Omitir archivos bloqueados por el sistema en uso
                            pass
                except Exception as e:
                    logger.warning(f"No se pudo acceder por completo a {base_path}: {e}")

        # Vaciar papelera de reciclaje mediante PowerShell
        try:
            logger.info("Vaciando Papelera de Reciclaje...")
            import subprocess
            subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=10
            )
        except Exception:
            pass

        freed_mb = round(freed_bytes / (1024 * 1024), 2)
        logger.success(f"¡Limpieza completada! Se liberaron {freed_mb} MB en {deleted_files} archivos.")
        return {
            "freed_bytes": freed_bytes,
            "freed_mb": freed_mb,
            "deleted_files": deleted_files
        }
