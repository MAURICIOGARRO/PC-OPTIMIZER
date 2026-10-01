import threading
import customtkinter as ctk
from ui.theme import Theme
from modules.office.detector import OfficeDetector
from modules.office.odt_manager import OfficeODTManager
from modules.office.updater import OfficeUpdater
from core.logger import logger

class OfficeView(ctk.CTkScrollableFrame):
    """Vista HUD Gamer de gestión, detección, instalación modular y actualización de Microsoft Office en español."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._build_header()
        self._build_detector_section()
        self._build_installer_section()

    def _build_header(self):
        banner = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        banner.pack(fill="x", padx=16, pady=(16, 10))

        left = ctk.CTkFrame(banner, fg_color="transparent")
        left.pack(side="left", padx=18, pady=16)

        title = ctk.CTkLabel(
            left,
            text="📑 GESTOR DE OFFICE // INSTALADOR MODULAR OFICIAL",
            font=(Theme.FONT_FAMILY_TITLE, 20, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(anchor="w")

        sub = ctk.CTkLabel(
            left,
            text="Detección de versión en registro, actualización oficial C2R y despliegue modular de apps seleccionadas.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        sub.pack(anchor="w", pady=(2, 0))

        # Botón de Actualizar Office
        self.btn_update = ctk.CTkButton(
            banner,
            text="🔄 ACTUALIZAR OFFICE OFICIAL",
            height=34,
            font=(Theme.FONT_CODE, 11, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._update_office
        )
        self.btn_update.pack(side="right", padx=16)

    def _build_detector_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=6)

        head = ctk.CTkFrame(frame, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=(14, 8))

        ctk.CTkLabel(
            head,
            text="🔎 DETECCIÓN DE OFFICE EN ESTE EQUIPO // ESCANEO DE REGISTRO",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_PURPLE
        ).pack(side="left")

        ctk.CTkButton(
            head,
            text="DETECTAR AHORA",
            width=120,
            height=26,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._detect_office
        ).pack(side="right")

        self.detect_info_box = ctk.CTkFrame(frame, fg_color="#090E1A", corner_radius=8, border_width=1, border_color=Theme.BORDER)
        self.detect_info_box.pack(fill="x", padx=18, pady=(0, 14))

        self.detect_status_lbl = ctk.CTkLabel(
            self.detect_info_box,
            text="Escaneando el sistema en busca de versiones activas de Microsoft Office...",
            font=(Theme.FONT_CODE, 11),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w"
        )
        self.detect_status_lbl.pack(fill="x", padx=14, pady=12)

        self.after(500, self._detect_office)

    def _detect_office(self):
        def worker():
            info = OfficeDetector.detect_installed_office()
            def done():
                for w in self.detect_info_box.winfo_children():
                    w.destroy()

                if not info["installed"]:
                    ctk.CTkLabel(
                        self.detect_info_box,
                        text="[ESTADO: NINGUNO] No se detectó ninguna instalación activa de Microsoft Office en este equipo.",
                        font=(Theme.FONT_CODE, 11, "bold"),
                        text_color=Theme.NEON_GOLD,
                        anchor="w"
                    ).pack(fill="x", padx=14, pady=12)
                else:
                    top_line = ctk.CTkFrame(self.detect_info_box, fg_color="transparent")
                    top_line.pack(fill="x", padx=14, pady=(10, 4))

                    badge = ctk.CTkLabel(
                        top_line,
                        text="INSTALADO // ACTIVO",
                        font=(Theme.FONT_CODE, 10, "bold"),
                        fg_color="#082A1B",
                        text_color=Theme.NEON_GREEN,
                        corner_radius=4,
                        padx=8,
                        pady=2
                    )
                    badge.pack(side="left", padx=(0, 10))

                    name_lbl = ctk.CTkLabel(
                        top_line,
                        text=f"{info['product_name']}  (v{info.get('version', 'Detectada') or 'N/A'} - {info['architecture']})",
                        font=(Theme.FONT_FAMILY, 12, "bold"),
                        text_color=Theme.TEXT_PRIMARY
                    )
                    name_lbl.pack(side="left")

                    apps_str = ", ".join(info["installed_apps"]) if info["installed_apps"] else "No se detectaron binarios individuales"
                    apps_lbl = ctk.CTkLabel(
                        self.detect_info_box,
                        text=f"APLICACIONES ACTIVAS: {apps_str}",
                        font=(Theme.FONT_CODE, 10),
                        text_color=Theme.NEON_CYAN,
                        anchor="w"
                    )
                    apps_lbl.pack(fill="x", padx=14, pady=(0, 10))
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _update_office(self):
        self.btn_update.configure(state="disabled", text="BUSCANDO...")
        def worker():
            OfficeUpdater.check_and_update()
            self.after(0, lambda: self.btn_update.configure(state="normal", text="🔄 ACTUALIZAR OFFICE OFICIAL"))
        threading.Thread(target=worker, daemon=True).start()

    def _build_installer_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=(6, 16))

        ctk.CTkLabel(
            frame,
            text="📦 SELECTOR MODULAR DE APLICACIONES // MOTOR OFICIAL ODT",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_CYAN
        ).pack(anchor="w", padx=18, pady=(14, 2))

        ctk.CTkLabel(
            frame,
            text="Marca ÚNICAMENTE las aplicaciones que deseas instalar (ejemplo: si solo marcas PowerPoint, solo se instalará PowerPoint).",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        ).pack(anchor="w", padx=18, pady=(0, 10))

        # Atajos en español
        presets = ctk.CTkFrame(frame, fg_color="transparent")
        presets.pack(fill="x", padx=18, pady=(0, 10))

        btn_style = {
            "height": 26,
            "font": (Theme.FONT_CODE, 10, "bold"),
            "fg_color": "#0F1728",
            "hover_color": Theme.BG_CARD_HOVER,
            "text_color": Theme.TEXT_SECONDARY,
            "border_width": 1,
            "border_color": Theme.BORDER
        }

        ctk.CTkButton(presets, text="SOLO POWERPOINT", width=140, command=self._select_only_powerpoint, **btn_style).pack(side="left", padx=(0, 6))
        ctk.CTkButton(presets, text="BÁSICO (WORD+EXCEL+PPT)", width=190, command=self._select_basic, **btn_style).pack(side="left", padx=(0, 6))
        ctk.CTkButton(presets, text="SELECCIONAR TODO", width=140, command=self._select_all, **btn_style).pack(side="left", padx=(0, 6))
        ctk.CTkButton(presets, text="LIMPIAR", width=80, command=self._clear_all, **btn_style).pack(side="left")

        # Grid de Checkboxes
        grid = ctk.CTkFrame(frame, fg_color="#090E1A", corner_radius=8, border_width=1, border_color=Theme.BORDER)
        grid.pack(fill="x", padx=18, pady=6)
        grid.columnconfigure((0, 1, 2), weight=1)

        self.app_vars = {}
        apps = [
            ("PowerPoint", "Presentaciones y diapositivas", True),
            ("Word", "Procesador de textos profesional", True),
            ("Excel", "Hojas de cálculo y fórmulas", True),
            ("Outlook", "Gestor de correo electrónico", False),
            ("OneNote", "Bloc de notas digital", False),
            ("Access", "Bases de datos de escritorio", False),
            ("Publisher", "Diseño editorial y publicaciones", False),
            ("Teams", "Reuniones y colaboración", False),
            ("OneDrive", "Sincronización en la nube", False),
        ]

        for i, (app_name, app_desc, default_val) in enumerate(apps):
            r = i // 3
            c = i % 3

            cell = ctk.CTkFrame(grid, fg_color="transparent")
            cell.grid(row=r, column=c, padx=12, pady=10, sticky="w")

            var = ctk.BooleanVar(value=default_val)
            self.app_vars[app_name] = var

            chk = ctk.CTkCheckBox(
                cell,
                text=app_name,
                variable=var,
                font=(Theme.FONT_FAMILY, 12, "bold"),
                text_color=Theme.TEXT_PRIMARY,
                fg_color=Theme.NEON_CYAN,
                hover_color=Theme.PRIMARY_HOVER,
                border_color=Theme.BORDER
            )
            chk.pack(anchor="w")

            ctk.CTkLabel(
                cell,
                text=app_desc,
                font=(Theme.FONT_FAMILY, 10),
                text_color=Theme.TEXT_MUTED
            ).pack(anchor="w", padx=(26, 0))

        # Configuración ODT
        config_row = ctk.CTkFrame(frame, fg_color="transparent")
        config_row.pack(fill="x", padx=18, pady=(12, 14))

        ctk.CTkLabel(config_row, text="EDICIÓN:", font=(Theme.FONT_CODE, 10, "bold"), text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self.combo_edition = ctk.CTkComboBox(
            config_row,
            values=["ProPlus2021Retail", "O365ProPlusRetail", "ProPlus2019Retail", "HomeBusiness2021Retail"],
            width=165,
            font=(Theme.FONT_CODE, 10)
        )
        self.combo_edition.set("ProPlus2021Retail")
        self.combo_edition.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(config_row, text="ARQUITECTURA:", font=(Theme.FONT_CODE, 10, "bold"), text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self.combo_arch = ctk.CTkComboBox(
            config_row,
            values=["64", "32"],
            width=65,
            font=(Theme.FONT_CODE, 10)
        )
        self.combo_arch.set("64")
        self.combo_arch.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(config_row, text="IDIOMA:", font=(Theme.FONT_CODE, 10, "bold"), text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self.combo_lang = ctk.CTkComboBox(
            config_row,
            values=["es-es", "en-us", "MatchOS"],
            width=90,
            font=(Theme.FONT_CODE, 10)
        )
        self.combo_lang.set("es-es")
        self.combo_lang.pack(side="left", padx=(0, 14))

        # Botón de instalación
        self.btn_install = ctk.CTkButton(
            config_row,
            text="🚀 INSTALAR SELECCIÓN OFICIAL",
            height=34,
            font=(Theme.FONT_CODE, 11, "bold"),
            fg_color=Theme.NEON_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            text_color="#04060A",
            command=self._start_custom_install
        )
        self.btn_install.pack(side="right")

    def _select_only_powerpoint(self):
        for k, v in self.app_vars.items():
            v.set(k == "PowerPoint")

    def _select_basic(self):
        for k, v in self.app_vars.items():
            v.set(k in ("Word", "Excel", "PowerPoint"))

    def _select_all(self):
        for v in self.app_vars.values():
            v.set(True)

    def _clear_all(self):
        for v in self.app_vars.values():
            v.set(False)

    def _start_custom_install(self):
        selected = [name for name, var in self.app_vars.items() if var.get()]
        if not selected:
            logger.warning("Debes seleccionar al menos una aplicación para instalar.")
            return

        self.btn_install.configure(state="disabled", text="INSTALANDO...")
        edition = self.combo_edition.get()
        arch = self.combo_arch.get()
        lang = self.combo_lang.get()

        def on_done(ok):
            self.after(0, lambda: self.btn_install.configure(state="normal", text="🚀 INSTALAR SELECCIÓN OFICIAL"))
            self._detect_office()

        OfficeODTManager.install_custom_office(
            selected_apps=selected,
            edition=edition,
            arch=arch,
            lang=lang,
            on_finish=on_done
        )
