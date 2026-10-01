import sys
import ctypes

def is_admin() -> bool:
    """Verifica si el proceso actual tiene privilegios de Administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def elevate() -> bool:
    """Relanza la aplicación con elevación UAC de Administrador si no los tiene."""
    if is_admin():
        return True
    try:
        # Re-lanzar sys.executable con los argumentos originales usando 'runas'
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            params,
            None,
            1  # SW_SHOWNORMAL
        )
        if ret > 32:
            # Lanzado exitosamente como admin, el proceso actual debe cerrarse
            sys.exit(0)
        else:
            return False
    except Exception as e:
        print(f"Error al solicitar permisos de administrador: {e}")
        return False
