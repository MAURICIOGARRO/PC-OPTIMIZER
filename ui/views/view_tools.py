import threading
import customtkinter as ctk
from ui.theme import Theme
from modules.tools.debloater import WindowsDebloater
from modules.tools.winget_apps import WingetAppInstaller
from modules.tools.runtimes import RuntimesInstaller
from modules.tools.dns_changer import DNSChanger
from modules.tools.power_tools import PowerTools

class ToolsView(ctk.CTkScrollableFrame):
    """Vista HUD Gamer de utilidades: Debloater de Windows Store, Winget Apps, Runtimes, DNS y Power Tools."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._build_header()
        self._build_debloater_section()
        self._build_dns_section()
        self._build_winget_apps_section()
        self._build_runtimes_section()
        self._build_power_tools_section()

    def _build_header(self):
        banner = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        banner.pack(fill="x", padx=16, pady=(16, 10))

        title = ctk.CTkLabel(
            banner,
            text="📦 SOFTWARE, HERRAMIENTAS & UTILIDADES GAMER",
            font=(Theme.FONT_FAMILY_TITLE, 20, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=20, pady=(14, 2))

        sub = ctk.CTkLabel(
            banner,
            text="Desinstalador de Bloatware de Windows Store, instalador de aplicaciones oficiales (Winget), Runtimes C++/DirectX, DNS y atajos.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        sub.pack(anchor="w", padx=20, pady=(0, 14))

    def _build_debloater_section(self):
        """Card para eliminar bloatware y aplicaciones innecesarias precargadas de Windows Store."""
        card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        card.pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(
            card,
            text="🗑️ DESINSTALADOR DE BLOATWARE DE WINDOWS STORE",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_RED
        ).pack(anchor="w", padx=18, pady=(14, 4))

        self.deb_lbl = ctk.CTkLabel(
            card,
            text="Elimina aplicaciones basura precargadas que consumen espacio y recursos (Bing Noticias, Visor 3D, Solitario, Xbox Game Bar widgets, etc.).",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=780,
            anchor="w"
        )
        self.deb_lbl.pack(anchor="w", padx=18, pady=(0, 10))

        btn_box = ctk.CTkFrame(card, fg_color="transparent")
        btn_box.pack(fill="x", padx=18, pady=(0, 14))

        self.btn_scan_deb = ctk.CTkButton(
            btn_box,
            text="ESCANEAR BLOATWARE",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._scan_bloatware
        )
        self.btn_scan_deb.pack(side="left", padx=(0, 8))

        self.btn_remove_deb = ctk.CTkButton(
            btn_box,
            text="ELIMINAR TODO EL BLOATWARE DETECTADO",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_RED,
            hover_color=Theme.DANGER_HOVER,
            text_color="#FFFFFF",
            command=self._remove_all_bloatware
        )
        self.btn_remove_deb.pack(side="left")

    def _scan_bloatware(self):
        self.btn_scan_deb.configure(state="disabled", text="ESCANEANDO...")
        def worker():
            apps = WindowsDebloater.get_installed_bloatware()
            def done():
                count = len(apps)
                self.deb_lbl.configure(text=f"[ESTADO] Se detectaron {count} aplicaciones basura instaladas en el sistema. Pulsa 'ELIMINAR' para desinstalarlas.")
                self.btn_scan_deb.configure(state="normal", text="ESCANEAR BLOATWARE")
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _remove_all_bloatware(self):
        self.btn_remove_deb.configure(state="disabled", text="ELIMINANDO...")
        def worker():
            apps = WindowsDebloater.get_installed_bloatware()
            ids = [a["id"] for a in apps]
            count = WindowsDebloater.remove_selected(ids)
            def done():
                self.deb_lbl.configure(text=f"[LIMPIEZA COMPLETADA] Se desinstalaron con éxito {count} paquetes de bloatware del sistema.")
                self.btn_remove_deb.configure(state="normal", text="ELIMINAR TODO EL BLOATWARE DETECTADO")
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _build_dns_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(
            frame,
            text="🌐 CAMBIADOR RÁPIDO DE DNS & TEST DE LATENCIA (PING)",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_CYAN
        ).pack(anchor="w", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            frame,
            text="Reduce latencia en juegos multijugador o bloquea publicidad y malware directamente a nivel de red.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        ).pack(anchor="w", padx=18, pady=(0, 10))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=(0, 14))

        ctk.CTkLabel(row, text="PRESET:", font=(Theme.FONT_CODE, 10, "bold"), text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 8))

        self.dns_combo = ctk.CTkComboBox(
            row,
            values=["Cloudflare", "Google", "AdGuard", "Quad9", "DHCP"],
            width=150,
            font=(Theme.FONT_CODE, 10)
        )
        self.dns_combo.set("Cloudflare")
        self.dns_combo.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            row,
            text="APLICAR DNS",
            width=100,
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._apply_dns
        ).pack(side="left", padx=(0, 10))

        self.btn_ping = ctk.CTkButton(
            row,
            text="TEST DE PING",
            width=110,
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._test_dns_ping
        )
        self.btn_ping.pack(side="left", padx=(0, 10))

        self.ping_res_lbl = ctk.CTkLabel(row, text="", font=(Theme.FONT_CODE, 11, "bold"), text_color=Theme.NEON_GREEN)
        self.ping_res_lbl.pack(side="left")

    def _apply_dns(self):
        sel = self.dns_combo.get()
        threading.Thread(target=lambda: DNSChanger.set_dns(sel), daemon=True).start()

    def _test_dns_ping(self):
        sel = self.dns_combo.get()
        ip = "1.1.1.1" if sel == "Cloudflare" else ("8.8.8.8" if sel == "Google" else ("94.140.14.14" if sel == "AdGuard" else "9.9.9.9"))
        self.btn_ping.configure(state="disabled", text="PROBANDO...")
        def worker():
            ms = DNSChanger.ping_test(ip)
            def done():
                res_txt = f"{ms} ms" if ms >= 0 else "TIEMPO AGOTADO"
                self.ping_res_lbl.configure(text=f"[LATENCIA: {res_txt}]")
                self.btn_ping.configure(state="normal", text="TEST DE PING")
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _build_winget_apps_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(
            frame,
            text="📦 INSTALADOR DE SOFTWARE ESENCIAL EN 1 CLIC (WINGET)",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_PURPLE
        ).pack(anchor="w", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            frame,
            text="Descarga e instala aplicaciones oficiales y seguras directamente de sus repositorios oficiales sin adware ni instaladores molestos.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        ).pack(anchor="w", padx=18, pady=(0, 10))

        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(fill="x", padx=18, pady=(0, 14))
        grid.columnconfigure((0, 1, 2, 3), weight=1)

        apps = WingetAppInstaller.ESSENTIAL_APPS[:8]
        for i, a in enumerate(apps):
            r = i // 4
            c = i % 4

            box = ctk.CTkFrame(grid, fg_color="#090E1A", corner_radius=6, border_width=1, border_color=Theme.BORDER)
            box.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

            ctk.CTkLabel(box, text=a["name"], font=(Theme.FONT_FAMILY, 11, "bold"), text_color=Theme.TEXT_PRIMARY).pack(anchor="w", padx=10, pady=(8, 2))
            ctk.CTkLabel(box, text=f"// {a['cat'].upper()}", font=(Theme.FONT_CODE, 9), text_color=Theme.TEXT_MUTED).pack(anchor="w", padx=10, pady=(0, 6))

            app_id = a["id"]
            btn = ctk.CTkButton(
                box,
                text="INSTALAR",
                height=22,
                font=(Theme.FONT_CODE, 9, "bold"),
                fg_color=Theme.NEON_PURPLE,
                hover_color=Theme.SECONDARY_HOVER,
                text_color="#FFFFFF",
                command=lambda aid=app_id: WingetAppInstaller.install_app(aid)
            )
            btn.pack(fill="x", padx=10, pady=(0, 8))

    def _build_runtimes_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(
            frame,
            text="🎮 LIBRERÍAS & RUNTIMES // SOLUCIÓN DE ERRORES .DLL EN JUEGOS Y APPS",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_GOLD
        ).pack(anchor="w", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            frame,
            text="Instalación todo-en-uno de Visual C++ Redistributable (x64 y x86) y DirectX para evitar bloqueos y errores de librerías faltantes.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        ).pack(anchor="w", padx=18, pady=(0, 10))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=(0, 14))

        ctk.CTkButton(
            row,
            text="INSTALAR VISUAL C++ AIO (x64 y x86)",
            height=32,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_GOLD,
            hover_color="#CC9300",
            text_color="#04060A",
            command=lambda: RuntimesInstaller.install_vc_redist()
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            row,
            text="INSTALAR DIRECTX RUNTIME",
            height=32,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=lambda: RuntimesInstaller.install_directx()
        ).pack(side="left")

    def _build_power_tools_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=(6, 16))

        ctk.CTkLabel(
            frame,
            text="⚡ ATAJOS ADMINISTRATIVOS & POWER TOOLS",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.NEON_CYAN
        ).pack(anchor="w", padx=18, pady=(14, 4))

        # Atajos
        shortcuts = ctk.CTkFrame(frame, fg_color="transparent")
        shortcuts.pack(fill="x", padx=18, pady=(0, 12))

        tools_list = [
            ("MODO DIOS", "godmode"),
            ("ADMIN TAREAS", "taskmgr"),
            ("DISPOSITIVOS", "devmgmt"),
            ("REGISTRO", "regedit"),
            ("SERVICIOS", "services")
        ]
        for name, key in tools_list:
            ctk.CTkButton(
                shortcuts,
                text=name,
                height=26,
                font=(Theme.FONT_CODE, 10, "bold"),
                fg_color="#0F1728",
                hover_color=Theme.BG_CARD_HOVER,
                text_color=Theme.TEXT_SECONDARY,
                border_width=1,
                border_color=Theme.BORDER,
                command=lambda k=key: PowerTools.launch_tool(k)
            ).pack(side="left", padx=(0, 6))

        # Fila de Licencia y Apagado
        bottom_row = ctk.CTkFrame(frame, fg_color="#090E1A", corner_radius=6, border_width=1, border_color=Theme.BORDER)
        bottom_row.pack(fill="x", padx=18, pady=(0, 14))

        ctk.CTkLabel(bottom_row, text="CLAVE DE WINDOWS:", font=(Theme.FONT_CODE, 10, "bold"), text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(12, 4), pady=10)
        self.key_lbl = ctk.CTkLabel(bottom_row, text="[CLIC PARA CONSULTAR]", font=(Theme.FONT_CODE, 10), text_color=Theme.NEON_CYAN)
        self.key_lbl.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            bottom_row,
            text="VER CLAVE",
            width=80,
            height=22,
            font=(Theme.FONT_CODE, 9, "bold"),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self._fetch_key
        ).pack(side="left", padx=(0, 20))

        # Apagado programado
        ctk.CTkLabel(bottom_row, text="APAGADO PROGRAMADO (MIN):", font=(Theme.FONT_CODE, 10, "bold"), text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 4))
        self.shutdown_min = ctk.CTkEntry(bottom_row, width=45, height=22, font=(Theme.FONT_CODE, 10))
        self.shutdown_min.insert(0, "60")
        self.shutdown_min.pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            bottom_row,
            text="PROGRAMAR",
            width=80,
            height=22,
            font=(Theme.FONT_CODE, 9, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._set_shutdown
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            bottom_row,
            text="CANCELAR",
            width=70,
            height=22,
            font=(Theme.FONT_CODE, 9, "bold"),
            fg_color="#3B0D18",
            hover_color=Theme.DANGER,
            text_color=Theme.NEON_RED,
            border_width=1,
            border_color="#7F1D1D",
            command=PowerTools.cancel_shutdown
        ).pack(side="left", padx=(0, 12))

    def _fetch_key(self):
        def worker():
            key = PowerTools.get_windows_product_key()
            self.after(0, lambda: self.key_lbl.configure(text=f"[{key}]"))
        threading.Thread(target=worker, daemon=True).start()

    def _set_shutdown(self):
        try:
            m = int(self.shutdown_min.get().strip())
            PowerTools.schedule_shutdown(m)
        except ValueError:
            pass
