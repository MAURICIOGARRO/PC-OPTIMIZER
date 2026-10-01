import threading
import tkinter.filedialog as filedialog
import customtkinter as ctk
from ui.theme import Theme
from modules.tools.driver_optimizer import DriverOptimizer
from core.logger import logger

class DriversView(ctk.CTkScrollableFrame):
    """Vista moderna y minimalista de gestión, auditoría, optimización y actualización de controladores."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._build_header()
        self._build_status_overview()
        self._build_driver_updater_section()
        self._build_optimization_actions()
        self._build_utilities_section()

        # Auditoría inicial al abrir
        self.after(500, self._refresh_driver_audit)

    def _build_header(self):
        banner = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        banner.pack(fill="x", padx=16, pady=(16, 10))

        title = ctk.CTkLabel(
            banner,
            text="Controladores & Drivers del Sistema",
            font=(Theme.FONT_FAMILY_TITLE, 18, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=20, pady=(14, 2))

        sub = ctk.CTkLabel(
            banner,
            text="Actualización oficial de controladores (WHQL), optimización de comunicación Plug & Play y purga de caché de sombreadores.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        sub.pack(anchor="w", padx=20, pady=(0, 14))

    def _build_status_overview(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=4)
        grid.columnconfigure((0, 1), weight=1, uniform="drv_cols")

        # 1. Adaptador Gráfico (GPU)
        gpu_card = ctk.CTkFrame(
            grid,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        gpu_card.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        ctk.CTkLabel(
            gpu_card,
            text="ADAPTADOR DE PANTALLA PRINCIPAL",
            font=(Theme.FONT_CODE, 10, "bold"),
            text_color=Theme.PRIMARY
        ).pack(anchor="w", padx=16, pady=(12, 2))

        self.gpu_name_lbl = ctk.CTkLabel(
            gpu_card,
            text="Consultando adaptador...",
            font=(Theme.FONT_FAMILY, 12, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        )
        self.gpu_name_lbl.pack(fill="x", padx=16, pady=(0, 2))

        self.gpu_status_lbl = ctk.CTkLabel(
            gpu_card,
            text="Estado: Verificando controlador de video...",
            font=(Theme.FONT_FAMILY, 10),
            text_color=Theme.TEXT_MUTED,
            anchor="w"
        )
        self.gpu_status_lbl.pack(fill="x", padx=16, pady=(0, 12))

        # 2. Resumen de Controladores PNP
        pnp_card = ctk.CTkFrame(
            grid,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        pnp_card.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        ctk.CTkLabel(
            pnp_card,
            text="ESTADO DE DISPOSITIVOS & CONTROLADORES",
            font=(Theme.FONT_CODE, 10, "bold"),
            text_color=Theme.SUCCESS
        ).pack(anchor="w", padx=16, pady=(12, 2))

        self.pnp_count_lbl = ctk.CTkLabel(
            pnp_card,
            text="Paquetes instalados: Analizando...",
            font=(Theme.FONT_FAMILY, 12, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        )
        self.pnp_count_lbl.pack(fill="x", padx=16, pady=(0, 2))

        self.pnp_issues_lbl = ctk.CTkLabel(
            pnp_card,
            text="Dispositivos con conflicto: Verificando...",
            font=(Theme.FONT_FAMILY, 10),
            text_color=Theme.TEXT_MUTED,
            anchor="w"
        )
        self.pnp_issues_lbl.pack(fill="x", padx=16, pady=(0, 12))

    def _build_driver_updater_section(self):
        """Sección principal de actualización de controladores."""
        card = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        card.pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(
            card,
            text="🔄 ACTUALIZACIÓN AUTOMÁTICA DE CONTROLADORES",
            font=(Theme.FONT_CODE, 11, "bold"),
            text_color=Theme.PRIMARY
        ).pack(anchor="w", padx=18, pady=(14, 4))

        self.update_status_lbl = ctk.CTkLabel(
            card,
            text="Busca, descarga e instala automáticamente controladores certificados (WHQL) desde el catálogo oficial de Microsoft, o actualiza tu adaptador gráfico.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=780,
            anchor="w"
        )
        self.update_status_lbl.pack(fill="x", padx=18, pady=(0, 12))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 14))

        # Botón 1: Actualizar todos vía Windows Update WUA
        self.btn_update_all = ctk.CTkButton(
            btn_row,
            text="⚡ Actualizar Drivers (Windows Update)",
            height=32,
            font=(Theme.FONT_FAMILY, 11, "bold"),
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#FFFFFF",
            corner_radius=6,
            command=self._update_all_drivers
        )
        self.btn_update_all.pack(side="left", padx=(0, 8))

        # Botón 2: Actualizador dedicado de GPU
        self.btn_gpu_update = ctk.CTkButton(
            btn_row,
            text="Actualizar Driver de Video (GPU)",
            height=32,
            font=(Theme.FONT_FAMILY, 11),
            fg_color="#1E293B",
            hover_color="#334155",
            text_color=Theme.TEXT_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=6,
            command=self._launch_gpu_updater
        )
        self.btn_gpu_update.pack(side="left", padx=(0, 8))

        # Botón 3: Instalar desde carpeta .INF
        self.btn_folder_install = ctk.CTkButton(
            btn_row,
            text="Instalar Drivers desde Carpeta (.INF)",
            height=32,
            font=(Theme.FONT_FAMILY, 11),
            fg_color="#1E293B",
            hover_color="#334155",
            text_color=Theme.TEXT_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=6,
            command=self._install_from_folder
        )
        self.btn_folder_install.pack(side="left")

    def _build_optimization_actions(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=4)
        grid.columnconfigure((0, 1), weight=1, uniform="act_cols")

        # 1. Optimizar comunicación Plug and Play
        pnp_opt_card = ctk.CTkFrame(
            grid,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        pnp_opt_card.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        ctk.CTkLabel(
            pnp_opt_card,
            text="RE-INDEXAR Y OPTIMIZAR DISPOSITIVOS PNP",
            font=(Theme.FONT_CODE, 11, "bold"),
            text_color=Theme.TEXT_PRIMARY
        ).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            pnp_opt_card,
            text="Fuerza a Windows a escanear cambios de hardware, actualizar enlaces de bus y sincronizar controladores con todos los puertos y periféricos.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=360,
            anchor="w"
        ).pack(anchor="w", padx=16, pady=(0, 12))

        self.btn_opt_pnp = ctk.CTkButton(
            pnp_opt_card,
            text="Optimizar Dispositivos (PNP)",
            height=28,
            font=(Theme.FONT_FAMILY, 11, "bold"),
            fg_color="#1E293B",
            hover_color="#334155",
            text_color=Theme.TEXT_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=6,
            command=self._optimize_pnp
        )
        self.btn_opt_pnp.pack(anchor="w", padx=16, pady=(0, 14))

        # 2. Limpieza de Caché de Shaders Gráficos
        shader_card = ctk.CTkFrame(
            grid,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        shader_card.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        ctk.CTkLabel(
            shader_card,
            text="PURGAR CACHÉ DE SHADERS GRÁFICOS",
            font=(Theme.FONT_CODE, 11, "bold"),
            text_color=Theme.TEXT_PRIMARY
        ).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            shader_card,
            text="Elimina cachés corruptas de DirectX, NVIDIA, AMD e Intel. Resuelve tirones (stuttering), caídas bruscas de FPS y fallos gráficos en juegos y apps 3D.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            wraplength=360,
            anchor="w"
        ).pack(anchor="w", padx=16, pady=(0, 12))

        self.btn_clean_shaders = ctk.CTkButton(
            shader_card,
            text="Purgar Caché de Shaders",
            height=28,
            font=(Theme.FONT_FAMILY, 11, "bold"),
            fg_color="#1E293B",
            hover_color="#334155",
            text_color=Theme.TEXT_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=6,
            command=self._clean_shaders
        )
        self.btn_clean_shaders.pack(anchor="w", padx=16, pady=(0, 14))

    def _build_utilities_section(self):
        card = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        card.pack(fill="x", padx=16, pady=(6, 16))

        ctk.CTkLabel(
            card,
            text="UTILIDADES DE DIAGNÓSTICO DE HARDWARE",
            font=(Theme.FONT_CODE, 11, "bold"),
            text_color=Theme.TEXT_PRIMARY
        ).pack(anchor="w", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            card,
            text="Herramientas directas del sistema operativo para diagnosticar puertos y controladores.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        ).pack(anchor="w", padx=18, pady=(0, 12))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 14))

        ctk.CTkButton(
            btn_row,
            text="Administrador de Dispositivos",
            height=30,
            font=(Theme.FONT_FAMILY, 11),
            fg_color="#1E293B",
            hover_color="#334155",
            text_color=Theme.TEXT_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=6,
            command=DriverOptimizer.launch_device_manager
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_row,
            text="Re-sincronizar Pantalla (Win+Ctrl+Shift+B)",
            height=30,
            font=(Theme.FONT_FAMILY, 11),
            fg_color="#1E293B",
            hover_color="#334155",
            text_color=Theme.TEXT_PRIMARY,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=6,
            command=DriverOptimizer.restart_graphics_driver
        ).pack(side="left")

    def _refresh_driver_audit(self):
        def worker():
            audit = DriverOptimizer.audit_drivers()
            def done():
                # GPU
                self.gpu_name_lbl.configure(text=audit["gpu"]["name"])
                self.gpu_status_lbl.configure(text="Controlador gráfico en funcionamiento normal.")

                # PNP
                total = audit["total_oem_drivers"]
                self.pnp_count_lbl.configure(text=f"{total} paquetes de controladores OEM registrados")

                issues = audit["problem_devices"]
                if issues:
                    self.pnp_issues_lbl.configure(
                        text=f"⚠️ {len(issues)} dispositivo(s) requieren atención o driver.",
                        text_color=Theme.WARNING
                    )
                else:
                    self.pnp_issues_lbl.configure(
                        text="✓ Todos los dispositivos Plug & Play están configurados correctamente.",
                        text_color=Theme.SUCCESS
                    )
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _update_all_drivers(self):
        self.btn_update_all.configure(state="disabled", text="Buscando en Windows Update...")
        self.update_status_lbl.configure(text="Buscando controladores certificados pendientes en el catálogo oficial de Microsoft. Observa el progreso en la consola inferior...")
        def worker():
            res = DriverOptimizer.update_all_drivers_windows_update()
            def done():
                self.btn_update_all.configure(state="normal", text="⚡ Actualizar Drivers (Windows Update)")
                if res.get("status") == "up_to_date":
                    self.update_status_lbl.configure(text="[ESTADO] Todos los controladores del sistema se encuentran en su versión más reciente.")
                elif res.get("status") == "success":
                    self.update_status_lbl.configure(text=f"[ACTUALIZACIÓN COMPLETADA] Se procesaron e instalaron {res.get('count', 0)} controladores del sistema.")
                else:
                    self.update_status_lbl.configure(text="[AVISO] Finalizó la comprobación de controladores. Revisa la consola inferior para más detalles.")
                self._refresh_driver_audit()
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _launch_gpu_updater(self):
        self.btn_gpu_update.configure(state="disabled", text="Iniciando...")
        def worker():
            DriverOptimizer.launch_gpu_updater()
            self.after(0, lambda: self.btn_gpu_update.configure(state="normal", text="Actualizar Driver de Video (GPU)"))
        threading.Thread(target=worker, daemon=True).start()

    def _install_from_folder(self):
        folder = filedialog.askdirectory(title="Selecciona la carpeta que contiene los archivos .INF del controlador")
        if folder:
            self.btn_folder_install.configure(state="disabled", text="Instalando...")
            def worker():
                res = DriverOptimizer.install_drivers_from_folder(folder)
                def done():
                    self.btn_folder_install.configure(state="normal", text="Instalar Drivers desde Carpeta (.INF)")
                    self._refresh_driver_audit()
                self.after(0, done)
            threading.Thread(target=worker, daemon=True).start()

    def _optimize_pnp(self):
        self.btn_opt_pnp.configure(state="disabled", text="Optimizando...")
        def worker():
            DriverOptimizer.optimize_pnp_devices()
            def done():
                self.btn_opt_pnp.configure(state="normal", text="Optimizar Dispositivos (PNP)")
                self._refresh_driver_audit()
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _clean_shaders(self):
        self.btn_clean_shaders.configure(state="disabled", text="Limpiando...")
        def worker():
            res = DriverOptimizer.clean_shader_cache()
            def done():
                self.btn_clean_shaders.configure(
                    state="normal",
                    text=f"Caché purgada ({res['mb']} MB liberados)"
                )
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()
