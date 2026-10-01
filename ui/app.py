import customtkinter as ctk
from ui.theme import Theme
from ui.components.log_drawer import LogDrawer
from ui.views.view_dashboard import DashboardView
from ui.views.view_optimizer import OptimizerView
from ui.views.view_services import ServicesView
from ui.views.view_drivers import DriversView
from ui.views.view_repair import RepairView
from ui.views.view_office import OfficeView
from ui.views.view_tools import ToolsView
from core.elevation import is_admin, elevate
from core.logger import logger

class MainWindow(ctk.CTk):
    """Ventana principal moderna y minimalista de OptiCore Suite en español."""

    def __init__(self):
        super().__init__()

        self.title("OptiCore // Optimización, Diagnóstico y Reparación de Sistema")
        self.geometry("1240x840")
        self.minsize(1080, 700)

        # Modo oscuro minimalista
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=Theme.BG_MAIN)

        self._build_layout()
        self._init_views()
        self._show_view("dashboard")

        logger.info("OptiCore Suite inicializada correctamente.")
        if is_admin():
            logger.success("Privilegios de Administrador: Activos.")
        else:
            logger.warning("Usuario estándar detectado: Eleva a Administrador para control completo.")

    def _build_layout(self):
        # 1. Barra Lateral Minimalista
        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            fg_color=Theme.BG_SIDEBAR,
            corner_radius=0,
            border_width=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Borde divisor vertical
        self.sidebar_border = ctk.CTkFrame(self, width=1, fg_color=Theme.BORDER)
        self.sidebar_border.pack(side="left", fill="y")

        # Marca y Logotipo Minimalista
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=20, pady=(22, 16))

        logo_title = ctk.CTkLabel(
            brand_frame,
            text="OptiCore",
            font=(Theme.FONT_FAMILY_TITLE, 22, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        logo_title.pack(anchor="w")

        logo_sub = ctk.CTkLabel(
            brand_frame,
            text="SISTEMA & RENDIMIENTO",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            text_color=Theme.TEXT_MUTED
        )
        logo_sub.pack(anchor="w", pady=(1, 0))

        # Línea divisoria
        sep = ctk.CTkFrame(self.sidebar, height=1, fg_color=Theme.BORDER)
        sep.pack(fill="x", padx=16, pady=(0, 14))

        # Menú de navegación minimalista
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "Panel Principal"),
            ("optimizer", "Optimización & RAM"),
            ("services", "Servicios en Fondo"),
            ("drivers", "Controladores & Drivers"),
            ("repair", "Salud & Reparación"),
            ("office", "Gestor de Office"),
            ("tools", "Software & Utilidades"),
        ]

        for view_id, label in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                font=(Theme.FONT_FAMILY, 11),
                anchor="w",
                height=38,
                fg_color="transparent",
                text_color=Theme.TEXT_SECONDARY,
                hover_color=Theme.BG_CARD_HOVER,
                corner_radius=6,
                border_spacing=12,
                command=lambda vid=view_id: self._show_view(vid)
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[view_id] = btn

        # Badge de estado de Administrador en el pie
        admin_box = ctk.CTkFrame(
            self.sidebar,
            fg_color="#12141C",
            corner_radius=8,
            border_width=1,
            border_color=Theme.BORDER
        )
        admin_box.pack(side="bottom", fill="x", padx=12, pady=16)

        if is_admin():
            ctk.CTkLabel(
                admin_box,
                text="✓ Modo Administrador Activo",
                font=(Theme.FONT_FAMILY, 10, "bold"),
                text_color=Theme.SUCCESS
            ).pack(padx=10, pady=10)
        else:
            ctk.CTkLabel(
                admin_box,
                text="Modo Usuario Estándar",
                font=(Theme.FONT_FAMILY, 10),
                text_color=Theme.WARNING
            ).pack(padx=8, pady=(8, 2))

            ctk.CTkButton(
                admin_box,
                text="Elevar a Administrador",
                height=26,
                font=(Theme.FONT_FAMILY, 10, "bold"),
                fg_color=Theme.PRIMARY,
                hover_color=Theme.PRIMARY_HOVER,
                text_color="#FFFFFF",
                corner_radius=4,
                command=elevate
            ).pack(padx=8, pady=(0, 8))

        # 2. Contenedor Principal (Derecha)
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", fill="both", expand=True)

        # Consola de operaciones inferior (LogDrawer)
        self.log_drawer = LogDrawer(self.right_container)
        self.log_drawer.pack(side="bottom", fill="x", padx=16, pady=(0, 12))

        # Área de vistas dinámicas
        self.view_container = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.view_container.pack(side="top", fill="both", expand=True)

    def _init_views(self):
        self.views = {
            "dashboard": DashboardView(self.view_container),
            "optimizer": OptimizerView(self.view_container),
            "services": ServicesView(self.view_container),
            "drivers": DriversView(self.view_container),
            "repair": RepairView(self.view_container),
            "office": OfficeView(self.view_container),
            "tools": ToolsView(self.view_container),
        }

    def _show_view(self, view_id: str):
        for v in self.views.values():
            v.pack_forget()

        if view_id in self.views:
            self.views[view_id].pack(fill="both", expand=True)

        # Resaltado minimalista activo
        for vid, btn in self.nav_buttons.items():
            if vid == view_id:
                btn.configure(
                    fg_color="#1E2230",
                    text_color=Theme.PRIMARY,
                    border_width=1,
                    border_color="#2D3748"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=Theme.TEXT_SECONDARY,
                    border_width=0
                )
