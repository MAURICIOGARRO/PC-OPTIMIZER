import threading
import customtkinter as ctk
from ui.theme import Theme
from modules.analyzer.health_score import HealthScoreCalculator
from modules.optimizer.cleaner import SystemCleaner
from modules.optimizer.ram import RAMOptimizer
from modules.optimizer.startup import StartupManager
from core.logger import logger

class AnalyzerView(ctk.CTkScrollableFrame):
    """Vista HUD Gamer de análisis profundo del sistema, salud SMART y recomendaciones en español."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._build_header()
        self._build_score_overview()
        self._build_disks_section()
        self._build_recommendations_section()

    def _build_header(self):
        banner = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        banner.pack(fill="x", padx=16, pady=(16, 10))

        left = ctk.CTkFrame(banner, fg_color="transparent")
        left.pack(side="left", padx=18, pady=16)

        title = ctk.CTkLabel(
            left,
            text="🔍 DIAGNÓSTICO PROFUNDO // SALUD DEL SISTEMA & SMART",
            font=(Theme.FONT_FAMILY_TITLE, 20, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(anchor="w")

        sub = ctk.CTkLabel(
            left,
            text="Auditoría profunda de sectores de almacenamiento, telemetría SMART, defensas activas y corrección guiada.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        sub.pack(anchor="w", pady=(2, 0))

        self.btn_run_scan = ctk.CTkButton(
            banner,
            text="⚡ INICIAR ANÁLISIS COMPLETO",
            height=34,
            font=(Theme.FONT_CODE, 11, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._run_deep_scan
        )
        self.btn_run_scan.pack(side="right", padx=16)

    def _build_score_overview(self):
        self.score_card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        self.score_card.pack(fill="x", padx=16, pady=6)

        box = ctk.CTkFrame(self.score_card, fg_color="transparent")
        box.pack(fill="x", padx=20, pady=16)

        self.score_display = ctk.CTkLabel(
            box,
            text="-- / 100",
            font=(Theme.FONT_CODE, 36, "bold"),
            text_color=Theme.NEON_CYAN
        )
        self.score_display.pack(side="left", padx=(0, 20))

        details = ctk.CTkFrame(box, fg_color="transparent")
        details.pack(side="left", fill="both", expand=True)

        self.score_title = ctk.CTkLabel(
            details,
            text="[ESTADO DEL EQUIPO: PENDIENTE DE ESCANEO]",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        )
        self.score_title.pack(fill="x")

        self.score_desc = ctk.CTkLabel(
            details,
            text="Presiona 'INICIAR ANÁLISIS COMPLETO' para evaluar el hardware y software de este PC.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w"
        )
        self.score_desc.pack(fill="x", pady=(2, 0))

    def _build_disks_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(
            frame,
            text="💾 SALUD FÍSICA DE UNIDADES (SMART) // SSD & HDD",
            font=(Theme.FONT_CODE, 12, "bold"),
            text_color=Theme.NEON_GOLD
        ).pack(anchor="w", padx=18, pady=(12, 6))

        self.disks_container = ctk.CTkFrame(frame, fg_color="transparent")
        self.disks_container.pack(fill="x", padx=18, pady=(0, 14))

        ctk.CTkLabel(self.disks_container, text="Inicia el análisis para consultar la telemetría SMART de tus discos.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_MUTED).pack(anchor="w")

    def _build_recommendations_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=(6, 16))

        ctk.CTkLabel(
            frame,
            text="💡 RECOMENDACIONES & PROBLEMAS DETECTADOS",
            font=(Theme.FONT_CODE, 12, "bold"),
            text_color=Theme.NEON_CYAN
        ).pack(anchor="w", padx=18, pady=(12, 6))

        self.recs_container = ctk.CTkFrame(frame, fg_color="transparent")
        self.recs_container.pack(fill="x", padx=18, pady=(0, 14))

        ctk.CTkLabel(self.recs_container, text="No hay advertencias activas en este momento.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_MUTED).pack(anchor="w")

    def _run_deep_scan(self):
        self.btn_run_scan.configure(state="disabled", text="ESCANEANDO EQUIPO...")
        self.score_title.configure(text="[ANALIZANDO TELEMETRÍA, DISCOS Y SEGURIDAD...]")

        def worker():
            res = HealthScoreCalculator.evaluate()
            def done():
                self.score_display.configure(text=f"{res['score']} / 100", text_color=res["color"])
                self.score_title.configure(text=f"[CALIFICACIÓN DE SALUD: {res['status_text'].upper()}]")
                self.score_desc.configure(
                    text=f"Caché residual: {res['junk_mb']} MB // Apps arranque: {res['startup_count']} // Problemas detectados: {len(res['recommendations'])}"
                )

                # Discos
                for w in self.disks_container.winfo_children():
                    w.destroy()

                for d in res["disks"]:
                    d_row = ctk.CTkFrame(self.disks_container, fg_color="#090E1A", height=32, corner_radius=6, border_width=1, border_color=Theme.BORDER)
                    d_row.pack(fill="x", pady=2)

                    status_col = Theme.NEON_GREEN if d.get("is_ok", True) else Theme.NEON_RED
                    ctk.CTkLabel(d_row, text=f"📀 {d['name']}", font=(Theme.FONT_FAMILY, 11, "bold"), text_color=Theme.TEXT_PRIMARY, width=280, anchor="w").pack(side="left", padx=10)
                    ctk.CTkLabel(d_row, text=f"TIPO: {d['type']} ({d['size_gb']} GB)", font=(Theme.FONT_CODE, 10), text_color=Theme.TEXT_MUTED, width=160, anchor="w").pack(side="left")
                    ctk.CTkLabel(d_row, text=f"[SMART: {d['health'].upper()}]", font=(Theme.FONT_CODE, 10, "bold"), text_color=status_col).pack(side="right", padx=12)

                # Recomendaciones
                for w in self.recs_container.winfo_children():
                    w.destroy()

                if not res["recommendations"]:
                    ctk.CTkLabel(self.recs_container, text="🎉 [100% SALUDABLE] ¡Tu equipo está en condiciones óptimas de rendimiento!", font=(Theme.FONT_CODE, 11, "bold"), text_color=Theme.NEON_GREEN).pack(anchor="w", pady=4)
                else:
                    for rec in res["recommendations"]:
                        r_card = ctk.CTkFrame(self.recs_container, fg_color="#090E1A", corner_radius=6, border_width=1, border_color=Theme.BORDER)
                        r_card.pack(fill="x", pady=4)

                        r_top = ctk.CTkFrame(r_card, fg_color="transparent")
                        r_top.pack(fill="x", padx=12, pady=(8, 2))

                        p_col = Theme.NEON_RED if rec["priority"] == "ALTA" else Theme.NEON_GOLD
                        p_badge = ctk.CTkLabel(r_top, text=f"[{rec['priority']}]", font=(Theme.FONT_CODE, 10, "bold"), text_color=p_col, width=60)
                        p_badge.pack(side="left")

                        t_lbl = ctk.CTkLabel(r_top, text=rec["title"], font=(Theme.FONT_FAMILY, 11, "bold"), text_color=Theme.TEXT_PRIMARY)
                        t_lbl.pack(side="left", padx=6)

                        act_id = rec["id"]
                        btn_act = ctk.CTkButton(
                            r_top,
                            text=f"⚡ {rec['action_label'].upper()}",
                            width=125,
                            height=24,
                            font=(Theme.FONT_CODE, 10, "bold"),
                            fg_color=Theme.NEON_CYAN,
                            hover_color=Theme.PRIMARY_HOVER,
                            text_color="#04060A",
                            command=lambda a_id=act_id: self._execute_recommendation(a_id)
                        )
                        btn_act.pack(side="right")

                        d_lbl = ctk.CTkLabel(r_card, text=rec["desc"], font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_SECONDARY, anchor="w")
                        d_lbl.pack(fill="x", padx=12, pady=(0, 8))

                self.btn_run_scan.configure(state="normal", text="⚡ INICIAR ANÁLISIS COMPLETO")

            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    def _execute_recommendation(self, action_id: str):
        if action_id == "clean_junk":
            SystemCleaner.clean()
        elif action_id == "optimize_ram":
            RAMOptimizer.optimize_ram()
        elif action_id in ("fix_defender", "fix_firewall"):
            import subprocess
            subprocess.Popen(["explorer.exe", "windowsdefender:"])
        self._run_deep_scan()
