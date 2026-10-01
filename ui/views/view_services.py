import threading
import customtkinter as ctk
from ui.theme import Theme
from modules.tools.background_services import BackgroundServicesManager
from modules.tools.oem_debloat import OEMDebloater
from modules.tools.copilot_remover import CopilotRemover
from modules.tools.privacy import WindowsPrivacy
from core.logger import logger

class ServicesView(ctk.CTkScrollableFrame):
    """Vista dedicada y unificada para auditar y controlar todos los servicios en segundo plano."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._build_header()
        self._build_teamviewer_and_xbox_section()
        self._build_oem_section()
        self._build_copilot_and_telemetry_section()

        # Actualizar estados automáticamente
        self.after(500, self._refresh_all_status)

    def _build_header(self):
        banner = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        banner.pack(fill="x", padx=16, pady=(16, 10))

        title = ctk.CTkLabel(
            banner,
            text="🛑 CONTROL DE SERVICIOS EN SEGUNDO PLANO",
            font=(Theme.FONT_FAMILY_TITLE, 20, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=20, pady=(14, 2))

        sub = ctk.CTkLabel(
            banner,
            text="Apaga programas y servicios que corren 24/7 sin tu permiso: TeamViewer, Xbox Gaming Services, Telemetría OEM, Copilot y Windows.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        sub.pack(anchor="w", padx=20, pady=(0, 14))

    def _build_teamviewer_and_xbox_section(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=4)
        grid.columnconfigure((0, 1), weight=1, uniform="svc_cols")

        # 1. TeamViewer
        tv_card = ctk.CTkFrame(grid, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        tv_card.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        ctk.CTkLabel(
            tv_card,
            text="📡 TEAMVIEWER & ACCESO REMOTO",
            font=(Theme.FONT_CODE, 12, "bold"),
            text_color=Theme.NEON_CYAN
        ).pack(anchor="w", padx=16, pady=(12, 2))

        self.tv_status_lbl = ctk.CTkLabel(
            tv_card,
            text="Estado: Consultando servicio...",
            font=(Theme.FONT_CODE, 10),
            text_color=Theme.NEON_GOLD
        )
        self.tv_status_lbl.pack(anchor="w", padx=16, pady=(0, 4))

        ctk.CTkLabel(
            tv_card,
            text="Configura TeamViewer para que solo inicie cuando abras su icono (Manual), evitando que consuma RAM y red cuando no lo estás usando.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=360,
            anchor="w"
        ).pack(anchor="w", padx=16, pady=(0, 10))

        tv_btns = ctk.CTkFrame(tv_card, fg_color="transparent")
        tv_btns.pack(fill="x", padx=16, pady=(0, 14))

        self.btn_tv_manual = ctk.CTkButton(
            tv_btns,
            text="SOLO BAJO DEMANDA",
            height=28,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=lambda: self._set_tv_mode("manual")
        )
        self.btn_tv_manual.pack(side="left", padx=(0, 6))

        self.btn_tv_disable = ctk.CTkButton(
            tv_btns,
            text="DESHABILITAR",
            height=28,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.NEON_RED,
            border_width=1,
            border_color="#7F1D1D",
            command=lambda: self._set_tv_mode("disabled")
        )
        self.btn_tv_disable.pack(side="left", padx=(0, 6))

        self.btn_tv_auto = ctk.CTkButton(
            tv_btns,
            text="RESTAURAR",
            height=28,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=lambda: self._set_tv_mode("auto")
        )
        self.btn_tv_auto.pack(side="left")

        # 2. Xbox & Gaming Services
        xbox_card = ctk.CTkFrame(grid, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        xbox_card.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        ctk.CTkLabel(
            xbox_card,
            text="🎮 XBOX & GAMING SERVICES DE WINDOWS",
            font=(Theme.FONT_CODE, 12, "bold"),
            text_color=Theme.NEON_GREEN
        ).pack(anchor="w", padx=16, pady=(12, 2))

        self.xbox_status_lbl = ctk.CTkLabel(
            xbox_card,
            text="Estado: Consultando Gaming Services...",
            font=(Theme.FONT_CODE, 10),
            text_color=Theme.NEON_GOLD
        )
        self.xbox_status_lbl.pack(anchor="w", padx=16, pady=(0, 4))

        ctk.CTkLabel(
            xbox_card,
            text="Si juegas en Steam, Epic o no estás usando Xbox Game Pass en este momento, Gaming Services se ejecuta innecesariamente consumiendo ciclos.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=360,
            anchor="w"
        ).pack(anchor="w", padx=16, pady=(0, 10))

        xbox_btns = ctk.CTkFrame(xbox_card, fg_color="transparent")
        xbox_btns.pack(fill="x", padx=16, pady=(0, 14))

        self.btn_xbox_disable = ctk.CTkButton(
            xbox_btns,
            text="DESACTIVAR GAMING SERVICES",
            height=28,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            text_color="#04060A",
            command=self._disable_xbox
        )
        self.btn_xbox_disable.pack(side="left", padx=(0, 6))

        self.btn_xbox_enable = ctk.CTkButton(
            xbox_btns,
            text="RESTAURAR (GAME PASS)",
            height=28,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._enable_xbox
        )
        self.btn_xbox_enable.pack(side="left")

    def _build_oem_section(self):
        card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        card.pack(fill="x", padx=16, pady=6)

        hw = OEMDebloater.get_hardware_identity()
        self.oem_title = ctk.CTkLabel(
            card,
            text=f"💻 SERVICIOS & TELEMETRÍA OEM // {hw['manufacturer'].upper()} ({hw['model']})",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_GOLD
        )
        self.oem_title.pack(anchor="w", padx=18, pady=(14, 2))

        self.oem_desc = ctk.CTkLabel(
            card,
            text=f"Detecta la marca de este PC ({hw['full_name']}) y desactiva servicios en segundo plano del fabricante que devoran CPU y RAM: Lenovo Vantage/ImController, Dell SupportAssist, HP Touchpoint, ASUS Armoury, etc.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w"
        )
        self.oem_desc.pack(fill="x", padx=18, pady=(0, 10))

        oem_btns = ctk.CTkFrame(card, fg_color="transparent")
        oem_btns.pack(fill="x", padx=18, pady=(0, 14))

        self.btn_disable_oem = ctk.CTkButton(
            oem_btns,
            text="DESHABILITAR SERVICIOS DEL FABRICANTE",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_GOLD,
            hover_color="#CC9300",
            text_color="#04060A",
            command=self._disable_oem
        )
        self.btn_disable_oem.pack(side="left", padx=(0, 8))

        self.btn_scan_oem = ctk.CTkButton(
            oem_btns,
            text="ESCANEAR MARCA",
            height=30,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._scan_oem
        )
        self.btn_scan_oem.pack(side="left", padx=(0, 8))

        self.btn_restore_oem = ctk.CTkButton(
            oem_btns,
            text="RESTAURAR SERVICIOS OEM",
            height=30,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=lambda: threading.Thread(target=OEMDebloater.enable_all_oem_bloat, daemon=True).start()
        )
        self.btn_restore_oem.pack(side="left")

    def _build_copilot_and_telemetry_section(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=6)
        grid.columnconfigure((0, 1), weight=1, uniform="cop_tel")

        # Copilot
        cop_card = ctk.CTkFrame(grid, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        cop_card.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        ctk.CTkLabel(
            cop_card,
            text="🤖 WINDOWS COPILOT & IA",
            font=(Theme.FONT_CODE, 12, "bold"),
            text_color=Theme.NEON_CYAN
        ).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            cop_card,
            text="Elimina Copilot de la barra de tareas, Edge y las búsquedas web con Bing en el Menú Inicio (evitando que SearchHost consuma RAM con múltiples procesos de WebView2).",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=360,
            anchor="w"
        ).pack(anchor="w", padx=16, pady=(0, 10))

        cop_btns = ctk.CTkFrame(cop_card, fg_color="transparent")
        cop_btns.pack(fill="x", padx=16, pady=(0, 14))

        self.btn_copilot = ctk.CTkButton(
            cop_btns,
            text="DESACTIVAR COPILOT TOTAL",
            height=28,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._disable_copilot
        )
        self.btn_copilot.pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            cop_btns,
            text="RESTAURAR",
            height=28,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=lambda: threading.Thread(target=CopilotRemover.enable_copilot, daemon=True).start()
        ).pack(side="left")

        # Telemetría de Windows
        tel_card = ctk.CTkFrame(grid, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        tel_card.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        ctk.CTkLabel(
            tel_card,
            text="🛡️ TELEMETRÍA Y ESPIONAJE DE WINDOWS",
            font=(Theme.FONT_CODE, 12, "bold"),
            text_color=Theme.NEON_PURPLE
        ).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            tel_card,
            text="Detiene servicios de rastreo y diagnóstico de Microsoft (DiagTrack, dmwappushservice), publicidad y sugerencias invasivas del sistema.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=360,
            anchor="w"
        ).pack(anchor="w", padx=16, pady=(0, 10))

        tel_btns = ctk.CTkFrame(tel_card, fg_color="transparent")
        tel_btns.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkButton(
            tel_btns,
            text="BLOQUEAR TODA LA TELEMETRÍA",
            height=28,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_PURPLE,
            hover_color=Theme.SECONDARY_HOVER,
            text_color="#FFFFFF",
            command=lambda: threading.Thread(target=WindowsPrivacy.apply_privacy_tweaks, daemon=True).start()
        ).pack(side="left")

    def _refresh_all_status(self):
        def worker():
            tv = BackgroundServicesManager.get_teamviewer_status()
            xbox = BackgroundServicesManager.get_xbox_status()
            scan = OEMDebloater.scan_installed_oem_bloat()

            def done():
                # TeamViewer
                if tv["installed"]:
                    run_txt = "[ACTIVO EN FONDO]" if tv["running"] else "[DETENIDO]"
                    self.tv_status_lbl.configure(text=f"Servicio: {run_txt} // Modo: {tv['start_type']}")
                else:
                    self.tv_status_lbl.configure(text="TeamViewer no está instalado en este equipo.")

                # Xbox
                if xbox["installed"]:
                    run_txt = f"[ACTIVO ({xbox['running_count']} servicios)]" if xbox["running"] else "[DETENIDO]"
                    self.xbox_status_lbl.configure(text=f"Gaming Services: {run_txt}")
                else:
                    self.xbox_status_lbl.configure(text="Gaming Services no está presente.")

                # OEM
                hw = scan["hardware"]
                brands = ", ".join(scan["detected_brands"]) if scan["detected_brands"] else "Sin telemetría OEM activa"
                self.oem_title.configure(text=f"💻 SERVICIOS & TELEMETRÍA OEM // {hw['manufacturer'].upper()} ({hw['model']})")
                self.oem_desc.configure(
                    text=f"Equipo: {hw['full_name']}. Se detectaron {scan['total_items']} componentes de fondo de fabricante ({brands}). Pulsa 'DESHABILITAR' para liberar recursos."
                )

            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _set_tv_mode(self, mode: str):
        def worker():
            BackgroundServicesManager.set_teamviewer_mode(mode)
            self._refresh_all_status()
        threading.Thread(target=worker, daemon=True).start()

    def _disable_xbox(self):
        self.btn_xbox_disable.configure(state="disabled", text="DESACTIVANDO...")
        def worker():
            BackgroundServicesManager.disable_xbox_services()
            self.after(0, lambda: self.btn_xbox_disable.configure(state="normal", text="DESACTIVAR GAMING SERVICES"))
            self._refresh_all_status()
        threading.Thread(target=worker, daemon=True).start()

    def _enable_xbox(self):
        def worker():
            BackgroundServicesManager.enable_xbox_services()
            self._refresh_all_status()
        threading.Thread(target=worker, daemon=True).start()

    def _disable_oem(self):
        self.btn_disable_oem.configure(state="disabled", text="DESACTIVANDO...")
        def worker():
            OEMDebloater.disable_all_oem_bloat()
            self.after(0, lambda: self.btn_disable_oem.configure(state="normal", text="DESHABILITAR SERVICIOS DEL FABRICANTE"))
            self._refresh_all_status()
        threading.Thread(target=worker, daemon=True).start()

    def _scan_oem(self):
        self._refresh_all_status()

    def _disable_copilot(self):
        self.btn_copilot.configure(state="disabled", text="DESACTIVANDO...")
        def worker():
            CopilotRemover.disable_copilot_completely()
            self.after(0, lambda: self.btn_copilot.configure(state="normal", text="DESACTIVAR COPILOT TOTAL"))
        threading.Thread(target=worker, daemon=True).start()
