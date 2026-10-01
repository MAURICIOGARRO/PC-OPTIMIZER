import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ui.app import MainWindow
from core.elevation import is_admin, elevate

def main():
    # Si se pasa el argumento --require-admin y no es admin, se auto-eleva
    if "--require-admin" in sys.argv and not is_admin():
        elevate()
        return

    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
