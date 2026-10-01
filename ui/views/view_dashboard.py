import threading
import customtkinter as ctk
from ui.theme import Theme
from ui.components.metric_card import MetricCard
from modules.telemetry.monitor import SystemMonitor
from modules.telemetry.processes import ProcessManager
from modules.analyzer.health_score import HealthScoreCalculator
from modules.optimizer.ram import RAMOptimizer
from modules.optimizer.cleaner import SystemCleaner
from modules.optimizer.power import PowerPlanManager
from modules.optimizer.latency import LatencyTweaks
from core.logger import logger

class DashboardView(ctk.CTkScrollableFrame):
    """Vista principal de telemetría y optimización con diseño oscuro minimalista."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.monitor = SystemMonitor()
        self.is_active = True

        self._build_header()
        self._build_rig_info_bar()
        self._build_metric_grid()
        self._build_processes_section()

        # Iniciar ciclo de telemetría y diagnóstico
        self.after(500, self.evaluate_initial_health)
        self.after(800, self._tick_telemetry)

    def _build_header(self):
        banner = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        banner.pack(fill="x", padx=16, pady=(16, 8))

        left_f = ctk.CTkFrame(banner, fg_color="transparent")
        left_f.pack(side="left", padx=18, pady=16)

        title_box = ctk.CTkFrame(left_f, fg_color="transparent")
        title_box.pack(anchor="w")

        title = ctk.CTkLabel(
            title_box,
            text="Panel Principal",
            font=(Theme.FONT_FAMILY_TITLE, 20, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(side="left")

        self.system_status_badge = ctk.CTkLabel(
            title_box,
            text="Sistema Listo",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            text_color=Theme.SUCCESS,
            fg_color="#064E3B",
            corner_radius=4,
            padx=8,
            pady=2
        )
        self.system_status_badge.pack(side="left", padx=(12, 0))

        subtitle = ctk.CTkLabel(
            left_f,
            text="Supervisión de recursos en tiempo real, latencia y optimización del equipo",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # Indicador de salud minimalista
        self.score_badge = ctk.CTkLabel(
            banner,
            text="Salud: Evaluando...",
            font=(Theme.FONT_FAMILY, 11, "bold"),
            fg_color="#1E2230",
            text_color=Theme.PRIMARY,
            corner_radius=6,
            border_width=1,
            border_color=Theme.BORDER,
            padx=12,
            pady=6
        )
        self.score_badge.pack(side="right", padx=16)

        # Botón de Optimización Rápida
        self.btn_overdrive = ctk.CTkButton(
            banner,
            text="⚡ Optimización Rápida",
            font=(Theme.FONT_FAMILY, 11, "bold"),
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#FFFFFF",
            height=32,
            corner_radius=6,
            command=self._on_overdrive
        )
        self.btn_overdrive.pack(side="right", padx=(0, 10))

    def _build_rig_info_bar(self):
        """Barra de hardware del equipo (GPU & CPU)."""
        bar = ctk.CTkFrame(
            self,
            fg_color="#12141C",
            corner_radius=8,
            border_width=1,
            border_color=Theme.BORDER
        )
        bar.pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkLabel(
            bar,
            text="Adaptador Gráfico:",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            text_color=Theme.TEXT_MUTED
        ).pack(side="left", padx=(14, 6), pady=6)

        metrics = self.monitor.get_metrics()
        gpu_name = metrics["gpu"]["name"]
        self.gpu_lbl = ctk.CTkLabel(
            bar,
            text=gpu_name,
            font=(Theme.FONT_FAMILY, 10, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        self.gpu_lbl.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            bar,
            text="Procesador:",
            font=(Theme.FONT_FAMILY, 10, "bold"),
            text_color=Theme.TEXT_MUTED
        ).pack(side="left", padx=(0, 6))

        cpu = metrics["cpu"]
        self.cpu_spec_lbl = ctk.CTkLabel(
            bar,
            text=f"{cpu['cores_logical']} Hilos / {cpu['cores_physical']} Núcleos @ {cpu['freq_ghz']} GHz",
            font=(Theme.FONT_FAMILY, 10),
            text_color=Theme.TEXT_SECONDARY
        )
        self.cpu_spec_lbl.pack(side="left")

    def _build_metric_grid(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=4)
        grid.columnconfigure((0, 1, 2, 3), weight=1, uniform="metric_cols")

        # 1. CPU
        self.card_cpu = MetricCard(
            grid,
            title="Carga de CPU",
            value="--",
            subtext="Calculando frecuencia...",
            accent_color=Theme.PRIMARY
        )
        self.card_cpu.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        # 2. RAM
        self.card_ram = MetricCard(
            grid,
            title="Memoria RAM",
            value="--",
            subtext="Calculando memoria...",
            accent_color=Theme.SUCCESS
        )
        self.card_ram.grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

        # 3. Disco
        self.card_disk = MetricCard(
            grid,
            title="Almacenamiento (C:)",
            value="--",
            subtext="Calculando espacio...",
            accent_color=Theme.WARNING
        )
        self.card_disk.grid(row=0, column=2, padx=4, pady=4, sticky="nsew")

        # 4. Red
        self.card_net = MetricCard(
            grid,
            title="Tráfico de Red",
            value="↓ 0 KB/s",
            subtext="↑ 0 KB/s",
            accent_color="#818CF8",
            show_progress=False
        )
        self.card_net.grid(row=0, column=3, padx=4, pady=4, sticky="nsew")

    def _build_processes_section(self):
        frame = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER
        )
        frame.pack(fill="x", padx=16, pady=(6, 16))

        top_row = ctk.CTkFrame(frame, fg_color="transparent")
        top_row.pack(fill="x", padx=18, pady=(14, 8))

        ctk.CTkLabel(
            top_row,
            text="Procesos con Mayor Consumo de Memoria",
            font=(Theme.FONT_FAMILY, 12, "bold"),
            text_color=Theme.TEXT_PRIMARY
        ).pack(side="left")

        ctk.CTkButton(
            top_row,
            text="Actualizar Lista",
            font=(Theme.FONT_FAMILY, 10),
            height=24,
            width=100,
            fg_color="#1E293B",
            hover_color="#334155",
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=4,
            command=self._refresh_processes
        ).pack(side="right")

        self.procs_container = ctk.CTkFrame(frame, fg_color="transparent")
        self.procs_container.pack(fill="x", padx=18, pady=(0, 14))

        self._refresh_processes()

    def _refresh_processes(self):
        def worker():
            procs = ProcessManager.get_top_processes(limit=6, sort_by="memory")
            self.after(0, lambda: self._render_processes(procs))
        threading.Thread(target=worker, daemon=True).start()

    def _render_processes(self, procs: list):
        for widget in self.procs_container.winfo_children():
            widget.destroy()

        head_row = ctk.CTkFrame(self.procs_container, fg_color="#12141C", height=26, corner_radius=4)
        head_row.pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(head_row, text="NOMBRE DEL PROCESO", font=(Theme.FONT_FAMILY, 10, "bold"), text_color=Theme.TEXT_MUTED, width=220, anchor="w").pack(side="left", padx=12)
        ctk.CTkLabel(head_row, text="PID", font=(Theme.FONT_FAMILY, 10, "bold"), text_color=Theme.TEXT_MUTED, width=80, anchor="w").pack(side="left")
        ctk.CTkLabel(head_row, text="CONSUMO RAM", font=(Theme.FONT_FAMILY, 10, "bold"), text_color=Theme.TEXT_MUTED, width=120, anchor="w").pack(side="left")
        ctk.CTkLabel(head_row, text="ACCIÓN", font=(Theme.FONT_FAMILY, 10, "bold"), text_color=Theme.TEXT_MUTED, width=90, anchor="e").pack(side="right", padx=12)

        for p in procs:
            row = ctk.CTkFrame(self.procs_container, fg_color="transparent", height=30)
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=p['name'], font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_PRIMARY, width=220, anchor="w").pack(side="left", padx=12)
            ctk.CTkLabel(row, text=str(p["pid"]), font=(Theme.FONT_CODE, 10), text_color=Theme.TEXT_MUTED, width=80, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"{p['mem_mb']} MB", font=(Theme.FONT_CODE, 10, "bold"), text_color=Theme.PRIMARY, width=120, anchor="w").pack(side="left")

            pid = p["pid"]
            btn_kill = ctk.CTkButton(
                row,
                text="Finalizar",
                width=75,
                height=22,
                font=(Theme.FONT_FAMILY, 10),
                fg_color="#3B1822",
                hover_color=Theme.DANGER,
                text_color="#FCA5A5",
                border_width=1,
                border_color="#7F1D1D",
                corner_radius=4,
                command=lambda target_pid=pid: self._kill_proc(target_pid)
            )
            btn_kill.pack(side="right", padx=12)

    def _kill_proc(self, pid: int):
        ProcessManager.kill_process(pid)
        self._refresh_processes()

    def _tick_telemetry(self):
        if not self.winfo_exists():
            return

        def fetch():
            metrics = self.monitor.get_metrics()
            self.after(0, lambda: self._apply_telemetry(metrics))

        threading.Thread(target=fetch, daemon=True).start()
        self.after(2000, self._tick_telemetry)

    def _apply_telemetry(self, m: dict):
        try:
            # CPU
            cpu = m["cpu"]
            self.card_cpu.update_data(
                value=f"{cpu['percent']}%",
                subtext=f"{cpu['cores_logical']} Hilos @ {cpu['freq_ghz']} GHz",
                percent=cpu["percent"]
            )

            # RAM
            ram = m["ram"]
            self.card_ram.update_data(
                value=f"{ram['percent']}%",
                subtext=f"{ram['used_gb']} GB / {ram['total_gb']} GB en uso",
                percent=ram["percent"]
            )

            # Disco
            disk = m["disk"]
            self.card_disk.update_data(
                value=f"{disk['percent']}%",
                subtext=f"{disk['free_gb']} GB libres de {disk['total_gb']} GB",
                percent=disk["percent"]
            )

            # Red
            net = m["network"]
            self.card_net.update_data(
                value=f"↓ {net['download_speed']}",
                subtext=f"↑ {net['upload_speed']}"
            )
        except Exception:
            pass

    def evaluate_initial_health(self):
        def calc():
            res = HealthScoreCalculator.evaluate()
            def update():
                if self.winfo_exists():
                    self.score_badge.configure(
                        text=f"Salud: {res['score']}/100 [{res['status_text']}]",
                        text_color=res["color"]
                    )
            self.after(0, update)
        threading.Thread(target=calc, daemon=True).start()

    def _on_overdrive(self):
        """Optimización rápida: Purga RAM, limpia temporales, activa Máximo Rendimiento y ajusta latencia."""
        self.btn_overdrive.configure(state="disabled", text="Optimizando...")
        def worker():
            logger.info("=== Iniciando Optimización Rápida del Sistema ===")
            RAMOptimizer.optimize_ram()
            SystemCleaner.clean()
            PowerPlanManager.set_ultimate_performance()
            LatencyTweaks.apply_latency_tweaks()
            logger.success("¡Optimización rápida completada con éxito!")
            self.after(0, lambda: self.btn_overdrive.configure(state="normal", text="⚡ Optimización Rápida"))
            self._refresh_processes()
            self.evaluate_initial_health()
        threading.Thread(target=worker, daemon=True).start()
