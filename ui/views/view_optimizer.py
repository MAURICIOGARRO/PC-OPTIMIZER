import threading
import customtkinter as ctk
from ui.theme import Theme
from modules.optimizer.cleaner import SystemCleaner
from modules.optimizer.ram import RAMOptimizer
from modules.optimizer.startup import StartupManager
from modules.optimizer.power import PowerPlanManager
from modules.optimizer.latency import LatencyTweaks
from modules.optimizer.browser_opt import GoogleChromeOptimizer
from core.logger import logger

class OptimizerView(ctk.CTkScrollableFrame):
    """Vista de optimización extrema del sistema y acelerador gaming en español."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._build_header()
        self._build_cleaner_section()
        self._build_ram_section()
        self._build_chrome_section()
        self._build_power_and_latency_section()
        self._build_startup_section()

    def _build_header(self):
        banner = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        banner.pack(fill="x", padx=16, pady=(16, 10))

        title = ctk.CTkLabel(
            banner,
            text="⚡ OPTIMIZACIÓN & MODO TURBO GAMER",
            font=(Theme.FONT_FAMILY_TITLE, 20, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=20, pady=(14, 2))

        sub = ctk.CTkLabel(
            banner,
            text="Purga masiva de memoria RAM, optimización de Google Chrome, latencia cero en juegos y arranque ultra rápido.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        sub.pack(anchor="w", padx=20, pady=(0, 14))

    def _build_cleaner_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=6)

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        lbl = ctk.CTkLabel(
            header,
            text="🧹 LIMPIEZA PROFUNDA // ARCHIVOS TEMPORALES & CACHÉ",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_CYAN
        )
        lbl.pack(side="left")

        btn_box = ctk.CTkFrame(header, fg_color="transparent")
        btn_box.pack(side="right")

        self.btn_scan_junk = ctk.CTkButton(
            btn_box,
            text="ESCANEAR BASURA",
            width=130,
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._scan_junk
        )
        self.btn_scan_junk.pack(side="left", padx=4)

        self.btn_clean_junk = ctk.CTkButton(
            btn_box,
            text="LIMPIAR TODO",
            width=110,
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._clean_junk
        )
        self.btn_clean_junk.pack(side="left", padx=4)

        self.junk_status_lbl = ctk.CTkLabel(
            frame,
            text="Presiona 'ESCANEAR BASURA' para calcular el espacio recuperable en el disco.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w"
        )
        self.junk_status_lbl.pack(fill="x", padx=18, pady=(0, 14))

    def _scan_junk(self):
        self.btn_scan_junk.configure(state="disabled", text="ESCANEANDO...")
        self.junk_status_lbl.configure(text="Calculando tamaño de archivos temporales...")

        def worker():
            res = SystemCleaner.scan()
            def done():
                mb = res["_summary"]["total_mb"]
                files = res["_summary"]["total_files"]
                self.junk_status_lbl.configure(
                    text=f"[ESCANEO COMPLETADO] Se detectaron {mb} MB de archivos basura en {files} archivos."
                )
                self.btn_scan_junk.configure(state="normal", text="ESCANEAR BASURA")
            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    def _clean_junk(self):
        self.btn_clean_junk.configure(state="disabled", text="LIMPIANDO...")
        def worker():
            res = SystemCleaner.clean()
            def done():
                self.junk_status_lbl.configure(
                    text=f"[LIMPIEZA COMPLETADA] ¡Se liberaron exitosamente {res['freed_mb']} MB de almacenamiento!"
                )
                self.btn_clean_junk.configure(state="normal", text="LIMPIAR TODO")
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _build_ram_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=6)

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=14)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        title = ctk.CTkLabel(
            left,
            text="🚀 LIBERADOR DE RAM // VACIADO DE STANDBY LIST & CACHÉ",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_GREEN
        )
        title.pack(anchor="w")

        self.ram_info_lbl = ctk.CTkLabel(
            left,
            text="Fuerza a Windows a vaciar el Working Set innecesario, reduciendo latencias y tirones en juegos.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        self.ram_info_lbl.pack(anchor="w", pady=(2, 0))

        self.btn_opt_ram = ctk.CTkButton(
            header,
            text="LIBERAR RAM AHORA",
            width=160,
            height=34,
            font=(Theme.FONT_CODE, 11, "bold"),
            fg_color=Theme.NEON_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            text_color="#04060A",
            command=self._optimize_ram
        )
        self.btn_opt_ram.pack(side="right")

    def _optimize_ram(self):
        self.btn_opt_ram.configure(state="disabled", text="LIBERANDO...")
        def worker():
            res = RAMOptimizer.optimize_ram()
            def done():
                self.ram_info_lbl.configure(
                    text=f"[RAM OPTIMIZADA] Liberados {res['freed_mb']} MB ({res['initial_percent']}% → {res['final_percent']}%) en {res['processes_trimmed']} procesos."
                )
                self.btn_opt_ram.configure(state="normal", text="LIBERAR RAM AHORA")
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _build_chrome_section(self):
        """Sección especializada para optimizar el consumo desmedido de recursos de Google Chrome."""
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=6)

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 6))

        lbl = ctk.CTkLabel(
            header,
            text="🌐 OPTIMIZADOR DE GOOGLE CHROME // CONTROL DE RAM & FONDOS",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_CYAN
        )
        lbl.pack(side="left")

        desc = ctk.CTkLabel(
            frame,
            text="Evita que Chrome siga corriendo en 2do plano al cerrarse, activa el Ahorro de Memoria de alta eficiencia, desactiva la precarga innecesaria y detiene los servicios de actualización continua.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
            wraplength=780
        )
        desc.pack(fill="x", padx=18, pady=(0, 10))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 14))

        self.btn_chrome_opt = ctk.CTkButton(
            btn_row,
            text="APLICAR POLÍTICAS DE AHORRO",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._apply_chrome_opt
        )
        self.btn_chrome_opt.pack(side="left", padx=(0, 8))

        self.btn_chrome_purge = ctk.CTkButton(
            btn_row,
            text="PURGAR RAM DE CHROME EN VIVO",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            text_color="#04060A",
            command=self._purge_chrome_ram
        )
        self.btn_chrome_purge.pack(side="left", padx=(0, 8))

        self.btn_chrome_kill = ctk.CTkButton(
            btn_row,
            text="CERRAR PROCESOS ZOMBIS",
            height=30,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=lambda: threading.Thread(target=GoogleChromeOptimizer.close_all_chrome_processes, daemon=True).start()
        )
        self.btn_chrome_kill.pack(side="left")

    def _apply_chrome_opt(self):
        self.btn_chrome_opt.configure(state="disabled", text="APLICANDO...")
        def worker():
            GoogleChromeOptimizer.apply_chrome_optimizations()
            self.after(0, lambda: self.btn_chrome_opt.configure(state="normal", text="APLICAR POLÍTICAS DE AHORRO"))
        threading.Thread(target=worker, daemon=True).start()

    def _purge_chrome_ram(self):
        self.btn_chrome_purge.configure(state="disabled", text="PURGANDO...")
        def worker():
            GoogleChromeOptimizer.purge_chrome_memory()
            self.after(0, lambda: self.btn_chrome_purge.configure(state="normal", text="PURGAR RAM DE CHROME EN VIVO"))
        threading.Thread(target=worker, daemon=True).start()

    def _build_power_and_latency_section(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=6)
        grid.columnconfigure((0, 1), weight=1, uniform="subcols")

        # Plan de Energía
        p_card = ctk.CTkFrame(grid, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        p_card.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        ctk.CTkLabel(p_card, text="⚡ PLAN DE ENERGÍA DE WINDOWS", font=(Theme.FONT_CODE, 12, "bold"), text_color=Theme.NEON_GOLD).pack(anchor="w", padx=16, pady=(12, 4))
        self.power_lbl = ctk.CTkLabel(p_card, text=f"ACTIVO: {PowerPlanManager.get_current_plan()}", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_SECONDARY)
        self.power_lbl.pack(anchor="w", padx=16, pady=(0, 10))

        p_btns = ctk.CTkFrame(p_card, fg_color="transparent")
        p_btns.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkButton(
            p_btns,
            text="MÁXIMO RENDIMIENTO",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_GOLD,
            hover_color="#CC9300",
            text_color="#04060A",
            command=self._set_ultimate_power
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            p_btns,
            text="EQUILIBRADO",
            height=30,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._set_balanced_power
        ).pack(side="left")

        # Tweaks de Latencia y Gaming
        l_card = ctk.CTkFrame(grid, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        l_card.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        ctk.CTkLabel(l_card, text="🎮 LATENCIA MÍNIMA & CERO LAG", font=(Theme.FONT_CODE, 12, "bold"), text_color=Theme.NEON_PURPLE).pack(anchor="w", padx=16, pady=(12, 4))
        ctk.CTkLabel(l_card, text="Desactiva micro-stutters, elimina limitación de red TCP y prioriza procesos de juegos.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=16, pady=(0, 10))

        ctk.CTkButton(
            l_card,
            text="APLICAR OPTIMIZACIONES DE JUEGOS",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_PURPLE,
            hover_color=Theme.SECONDARY_HOVER,
            text_color="#FFFFFF",
            command=lambda: LatencyTweaks.apply_latency_tweaks()
        ).pack(anchor="w", padx=16, pady=(0, 14))

    def _set_ultimate_power(self):
        PowerPlanManager.set_ultimate_performance()
        self.power_lbl.configure(text=f"ACTIVO: {PowerPlanManager.get_current_plan()}")

    def _set_balanced_power(self):
        PowerPlanManager.set_balanced()
        self.power_lbl.configure(text=f"ACTIVO: {PowerPlanManager.get_current_plan()}")

    def _build_startup_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=(6, 16))

        head = ctk.CTkFrame(frame, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=(14, 8))

        lbl = ctk.CTkLabel(
            head,
            text="⏱️ GESTOR DE ARRANQUE // PROGRAMAS DE INICIO",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_CYAN
        )
        lbl.pack(side="left")

        ctk.CTkButton(
            head,
            text="RECARGAR",
            width=85,
            height=24,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._load_startup_apps
        ).pack(side="right")

        self.startup_container = ctk.CTkFrame(frame, fg_color="transparent")
        self.startup_container.pack(fill="x", padx=18, pady=(0, 14))

        self._load_startup_apps()

    def _load_startup_apps(self):
        for w in self.startup_container.winfo_children():
            w.destroy()

        def worker():
            apps = StartupManager.get_startup_apps()
            def done():
                if not apps:
                    ctk.CTkLabel(self.startup_container, text="No se detectaron aplicaciones en el inicio.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_MUTED).pack(anchor="w", pady=6)
                    return

                for app in apps:
                    row = ctk.CTkFrame(self.startup_container, fg_color="transparent", height=32)
                    row.pack(fill="x", pady=2)

                    ctk.CTkLabel(row, text=f"• {app['name']}", font=(Theme.FONT_FAMILY, 11, "bold"), text_color=Theme.TEXT_PRIMARY, width=220, anchor="w").pack(side="left")
                    ctk.CTkLabel(row, text=app["location"], font=(Theme.FONT_CODE, 10), text_color=Theme.TEXT_MUTED, width=180, anchor="w").pack(side="left")

                    status_text = "[HABILITADO]" if app["enabled"] else "[DESHABILITADO]"
                    status_col = Theme.NEON_GREEN if app["enabled"] else Theme.TEXT_MUTED

                    badge = ctk.CTkLabel(row, text=status_text, font=(Theme.FONT_CODE, 10, "bold"), text_color=status_col, width=105)
                    badge.pack(side="left")

                    is_en = app["enabled"]
                    btn_text = "DESHABILITAR" if is_en else "HABILITAR"
                    btn_col = "#1E2A44" if is_en else Theme.NEON_CYAN
                    btn_text_col = Theme.TEXT_SECONDARY if is_en else "#04060A"

                    def on_toggle(target_app=app, target_en=is_en):
                        StartupManager.toggle_app(target_app, not target_en)
                        self._load_startup_apps()

                    ctk.CTkButton(
                        row,
                        text=btn_text,
                        width=100,
                        height=22,
                        font=(Theme.FONT_CODE, 10, "bold"),
                        fg_color=btn_col,
                        hover_color=Theme.BG_CARD_HOVER,
                        text_color=btn_text_col,
                        command=on_toggle
                    ).pack(side="right")

            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()
