import threading
import customtkinter as ctk
from ui.theme import Theme
from modules.analyzer.health_score import HealthScoreCalculator
from modules.optimizer.cleaner import SystemCleaner
from modules.optimizer.ram import RAMOptimizer
from modules.repair.restore_point import RestorePointManager
from modules.repair.sfc_dism import SystemFileRepair
from modules.repair.network_fix import NetworkRepair
from modules.repair.wupdate_fix import WindowsUpdateRepair
from modules.repair.chkdsk_fix import DiskRepair

class RepairView(ctk.CTkScrollableFrame):
    """Vista unificada de Diagnóstico de Salud y Reparación Profunda del Sistema."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._build_header()
        self._build_health_score_section()
        self._build_recommendations_section()
        self._build_smart_disks_section()
        self._build_restore_point_card()
        self._build_system_files_card()
        self._build_network_and_update_card()
        self._build_disk_repair_card()

        # Iniciar diagnóstico inicial
        self.after(500, self._run_health_evaluation)

    def _build_header(self):
        banner = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        banner.pack(fill="x", padx=16, pady=(16, 10))

        title = ctk.CTkLabel(
            banner,
            text="🛠️ SALUD & REPARACIÓN DEL SISTEMA",
            font=(Theme.FONT_FAMILY_TITLE, 20, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=20, pady=(14, 2))

        sub = ctk.CTkLabel(
            banner,
            text="Auditoría de integridad, estado SMART de discos, reparación de componentes Windows (DISM/SFC), red y Windows Update.",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY
        )
        sub.pack(anchor="w", padx=20, pady=(0, 14))

    def _build_health_score_section(self):
        card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        card.pack(fill="x", padx=16, pady=4)

        box = ctk.CTkFrame(card, fg_color="transparent")
        box.pack(fill="x", padx=18, pady=14)

        self.score_display = ctk.CTkLabel(
            box,
            text="-- / 100",
            font=(Theme.FONT_CODE, 32, "bold"),
            text_color=Theme.NEON_CYAN
        )
        self.score_display.pack(side="left", padx=(0, 18))

        details = ctk.CTkFrame(box, fg_color="transparent")
        details.pack(side="left", fill="both", expand=True)

        self.score_title = ctk.CTkLabel(
            details,
            text="[ESTADO DE SALUD: EVALUANDO...]",
            font=(Theme.FONT_CODE, 13, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        )
        self.score_title.pack(fill="x")

        self.score_desc = ctk.CTkLabel(
            details,
            text="Examinando almacenamiento, memoria, servicios y seguridad de Windows...",
            font=(Theme.FONT_FAMILY, 11),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w"
        )
        self.score_desc.pack(fill="x", pady=(2, 0))

        self.btn_run_scan = ctk.CTkButton(
            box,
            text="RE-EVALUAR SALUD",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._run_health_evaluation
        )
        self.btn_run_scan.pack(side="right")

    def _build_recommendations_section(self):
        self.recs_frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        self.recs_frame.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(
            self.recs_frame,
            text="💡 RECOMENDACIONES & PROBLEMAS DETECTADOS",
            font=(Theme.FONT_CODE, 12, "bold"),
            text_color=Theme.NEON_CYAN
        ).pack(anchor="w", padx=18, pady=(12, 6))

        self.recs_container = ctk.CTkFrame(self.recs_frame, fg_color="transparent")
        self.recs_container.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkLabel(self.recs_container, text="Analizando sistema...", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_MUTED).pack(anchor="w")

    def _build_smart_disks_section(self):
        frame = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        frame.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(
            frame,
            text="💾 SALUD FÍSICA DE UNIDADES (SMART) // SSD & HDD",
            font=(Theme.FONT_CODE, 12, "bold"),
            text_color=Theme.NEON_GOLD
        ).pack(anchor="w", padx=18, pady=(12, 6))

        self.disks_container = ctk.CTkFrame(frame, fg_color="transparent")
        self.disks_container.pack(fill="x", padx=18, pady=(0, 12))

    def _build_restore_point_card(self):
        card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        card.pack(fill="x", padx=16, pady=4)

        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=12)

        left = ctk.CTkFrame(head, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(left, text="🛡️ PUNTO DE RESTAURACIÓN DEL SISTEMA", font=(Theme.FONT_CODE, 12, "bold"), text_color=Theme.NEON_GREEN).pack(anchor="w")
        self.restore_lbl = ctk.CTkLabel(left, text="Crea un respaldo de configuración antes de realizar modificaciones profundas.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_SECONDARY)
        self.restore_lbl.pack(anchor="w", pady=(2, 0))

        self.btn_create_rp = ctk.CTkButton(
            head,
            text="CREAR PUNTO DE CONTROL",
            width=180,
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=self._create_restore_point
        )
        self.btn_create_rp.pack(side="right")

    def _create_restore_point(self):
        self.btn_create_rp.configure(state="disabled", text="CREANDO...")
        def worker():
            ok = RestorePointManager.create_restore_point("OptiCore_Checkpoint")
            def done():
                msg = "[OK] ¡Punto de restauración creado con éxito!" if ok else "[AVISO] No se pudo crear. Verifica que Protección del Sistema esté activa."
                self.restore_lbl.configure(text=msg)
                self.btn_create_rp.configure(state="normal", text="CREAR PUNTO DE CONTROL")
            self.after(0, done)
        threading.Thread(target=worker, daemon=True).start()

    def _build_system_files_card(self):
        card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        card.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(card, text="🩺 INTEGRIDAD DE ARCHIVOS // DISM & SFC SCANNOW", font=(Theme.FONT_CODE, 12, "bold"), text_color=Theme.NEON_CYAN).pack(anchor="w", padx=18, pady=(12, 4))
        ctk.CTkLabel(card, text="Comprueba y repara los archivos de sistema corruptos en tiempo real mediante la consola inferior.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=18, pady=(0, 8))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 12))

        self.btn_full_repair = ctk.CTkButton(
            btn_row,
            text="⚡ REPARACIÓN COMPLETA (DISM + SFC)",
            height=30,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_GREEN,
            hover_color=Theme.SUCCESS_HOVER,
            text_color="#04060A",
            command=self._run_full_repair
        )
        self.btn_full_repair.pack(side="left", padx=(0, 8))

        btn_style = {
            "height": 30,
            "font": (Theme.FONT_CODE, 10),
            "fg_color": "#0F1728",
            "hover_color": Theme.BG_CARD_HOVER,
            "text_color": Theme.TEXT_SECONDARY,
            "border_width": 1,
            "border_color": Theme.BORDER
        }

        ctk.CTkButton(btn_row, text="SOLO SFC", command=lambda: SystemFileRepair.run_sfc_scan(), width=90, **btn_style).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="SOLO DISM", command=lambda: SystemFileRepair.run_dism_repair(), width=90, **btn_style).pack(side="left")

    def _run_full_repair(self):
        self.btn_full_repair.configure(state="disabled", text="REPARANDO...")
        def on_done(ok):
            self.after(0, lambda: self.btn_full_repair.configure(state="normal", text="⚡ REPARACIÓN COMPLETA (DISM + SFC)"))
        SystemFileRepair.run_full_repair(on_finish=on_done)

    def _build_network_and_update_card(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="x", padx=16, pady=4)
        grid.columnconfigure((0, 1), weight=1, uniform="net_upd")

        # Red
        net_card = ctk.CTkFrame(grid, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        net_card.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        ctk.CTkLabel(net_card, text="🌐 RESTABLECIMIENTO TOTAL DE RED", font=(Theme.FONT_CODE, 12, "bold"), text_color=Theme.NEON_PURPLE).pack(anchor="w", padx=16, pady=(12, 4))
        ctk.CTkLabel(net_card, text="Reinicia Winsock, TCP/IP, vacía DNS y renueva IP.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=16, pady=(0, 8))

        ctk.CTkButton(
            net_card,
            text="REPARAR RED AHORA",
            height=28,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_PURPLE,
            hover_color=Theme.SECONDARY_HOVER,
            text_color="#FFFFFF",
            command=lambda: threading.Thread(target=NetworkRepair.fix_network, daemon=True).start()
        ).pack(anchor="w", padx=16, pady=(0, 12))

        # Windows Update
        wu_card = ctk.CTkFrame(grid, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        wu_card.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        ctk.CTkLabel(wu_card, text="🔄 REPARADOR DE WINDOWS UPDATE", font=(Theme.FONT_CODE, 12, "bold"), text_color=Theme.NEON_GOLD).pack(anchor="w", padx=16, pady=(12, 4))
        ctk.CTkLabel(wu_card, text="Purga SoftwareDistribution corrupta y reinicia servicios.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=16, pady=(0, 8))

        ctk.CTkButton(
            wu_card,
            text="REPARAR WINDOWS UPDATE",
            height=28,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_GOLD,
            hover_color="#CC9300",
            text_color="#04060A",
            command=lambda: threading.Thread(target=WindowsUpdateRepair.fix_windows_update, daemon=True).start()
        ).pack(anchor="w", padx=16, pady=(0, 12))

    def _build_disk_repair_card(self):
        card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=12, border_width=1, border_color=Theme.BORDER)
        card.pack(fill="x", padx=16, pady=(4, 16))

        ctk.CTkLabel(card, text="💾 COMPROBACIÓN DE DISCO (CHKDSK)", font=(Theme.FONT_CODE, 12, "bold"), text_color=Theme.NEON_CYAN).pack(anchor="w", padx=18, pady=(12, 4))
        ctk.CTkLabel(card, text="Verifica sectores defectuosos e inconsistencias en la tabla de particiones del disco C:.", font=(Theme.FONT_FAMILY, 11), text_color=Theme.TEXT_SECONDARY).pack(anchor="w", padx=18, pady=(0, 8))

        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkButton(
            btns,
            text="COMPROBACIÓN ONLINE (C:)",
            height=28,
            font=(Theme.FONT_CODE, 10),
            fg_color="#0F1728",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=lambda: threading.Thread(target=DiskRepair.run_online_scan, daemon=True).start()
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btns,
            text="PROGRAMAR REPARACIÓN AL REINICIAR",
            height=28,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color=Theme.NEON_CYAN,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#04060A",
            command=lambda: threading.Thread(target=DiskRepair.schedule_boot_repair, daemon=True).start()
        ).pack(side="left")

    def _run_health_evaluation(self):
        self.btn_run_scan.configure(state="disabled", text="ANALIZANDO...")
        def worker():
            res = HealthScoreCalculator.evaluate()
            def done():
                self.score_display.configure(text=f"{res['score']} / 100", text_color=res["color"])
                self.score_title.configure(text=f"[CALIFICACIÓN DE SALUD: {res['status_text'].upper()}]")
                self.score_desc.configure(
                    text=f"Caché residual: {res['junk_mb']} MB // Apps arranque: {res['startup_count']} // Problemas detectados: {len(res['recommendations'])}"
                )

                # Discos SMART
                for w in self.disks_container.winfo_children():
                    w.destroy()

                for d in res["disks"]:
                    d_row = ctk.CTkFrame(self.disks_container, fg_color="#090E1A", height=30, corner_radius=6, border_width=1, border_color=Theme.BORDER)
                    d_row.pack(fill="x", pady=2)

                    status_col = Theme.NEON_GREEN if d.get("is_ok", True) else Theme.NEON_RED
                    ctk.CTkLabel(d_row, text=f"📀 {d['name']}", font=(Theme.FONT_FAMILY, 11, "bold"), text_color=Theme.TEXT_PRIMARY, width=280, anchor="w").pack(side="left", padx=10)
                    ctk.CTkLabel(d_row, text=f"TIPO: {d['type']} ({d['size_gb']} GB)", font=(Theme.FONT_CODE, 10), text_color=Theme.TEXT_MUTED, width=160, anchor="w").pack(side="left")
                    ctk.CTkLabel(d_row, text=f"[SMART: {d['health'].upper()}]", font=(Theme.FONT_CODE, 10, "bold"), text_color=status_col).pack(side="right", padx=12)

                # Recomendaciones
                for w in self.recs_container.winfo_children():
                    w.destroy()

                if not res["recommendations"]:
                    ctk.CTkLabel(self.recs_container, text="🎉 [100% SALUDABLE] No se detectaron fallos críticos en el sistema.", font=(Theme.FONT_CODE, 11, "bold"), text_color=Theme.NEON_GREEN).pack(anchor="w", pady=4)
                else:
                    for rec in res["recommendations"]:
                        r_card = ctk.CTkFrame(self.recs_container, fg_color="#090E1A", corner_radius=6, border_width=1, border_color=Theme.BORDER)
                        r_card.pack(fill="x", pady=3)

                        r_top = ctk.CTkFrame(r_card, fg_color="transparent")
                        r_top.pack(fill="x", padx=12, pady=(6, 2))

                        p_col = Theme.NEON_RED if rec["priority"] == "ALTA" else Theme.NEON_GOLD
                        ctk.CTkLabel(r_top, text=f"[{rec['priority']}]", font=(Theme.FONT_CODE, 10, "bold"), text_color=p_col, width=60).pack(side="left")
                        ctk.CTkLabel(r_top, text=rec["title"], font=(Theme.FONT_FAMILY, 11, "bold"), text_color=Theme.TEXT_PRIMARY).pack(side="left", padx=6)

                        act_id = rec["id"]
                        ctk.CTkButton(
                            r_top,
                            text=f"⚡ {rec['action_label'].upper()}",
                            width=120,
                            height=22,
                            font=(Theme.FONT_CODE, 9, "bold"),
                            fg_color=Theme.NEON_CYAN,
                            hover_color=Theme.PRIMARY_HOVER,
                            text_color="#04060A",
                            command=lambda a_id=act_id: self._execute_recommendation(a_id)
                        ).pack(side="right")

                        ctk.CTkLabel(r_card, text=rec["desc"], font=(Theme.FONT_FAMILY, 10), text_color=Theme.TEXT_SECONDARY, anchor="w").pack(fill="x", padx=12, pady=(0, 6))

                self.btn_run_scan.configure(state="normal", text="RE-EVALUAR SALUD")

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
        self._run_health_evaluation()
