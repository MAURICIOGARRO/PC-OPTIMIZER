from modules.tools.oem_debloat import OEMDebloater

class LenovoDebloater:
    """Compatibilidad con Lenovo redirigida al módulo universal OEMDebloater."""
    @classmethod
    def get_status(cls):
        return OEMDebloater.scan_installed_oem_bloat()

    @classmethod
    def disable_lenovo_bloat(cls):
        return OEMDebloater.disable_all_oem_bloat()

    @classmethod
    def enable_lenovo_bloat(cls):
        return OEMDebloater.enable_all_oem_bloat()
