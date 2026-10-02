import sys
import os
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
        if getattr(sys, 'frozen', False):
            executable = sys.executable
            params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
            work_dir = os.path.dirname(sys.executable)
        else:
            executable = sys.executable
            params = " ".join([f'"{arg}"' for arg in sys.argv])
            work_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        ret = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            executable,
            params,
            work_dir,
            1  # SW_SHOWNORMAL
        )
        if ret > 32:
            sys.exit(0)
        else:
            return False
    except Exception as e:
        print(f"Error al solicitar permisos de administrador: {e}")
        return False
