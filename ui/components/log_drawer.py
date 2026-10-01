import customtkinter as ctk
from ui.theme import Theme
from core.logger import logger

class LogDrawer(ctk.CTkFrame):
    """Consola HUD Gamer en tiempo real estilo terminal cibernética en español."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=Theme.BG_CARD_ALT,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER,
            **kwargs
        )

        self.is_expanded = True

        # Barra de cabecera de la terminal
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=12, pady=7)

        # Indicador de estado terminal
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="⚡ CONSOLA EN VIVO // REGISTRO DE OPERACIONES",
            font=(Theme.FONT_CODE, 11, "bold"),
            text_color=Theme.NEON_CYAN
        )
        self.title_label.pack(side="left")

        # Botones de control HUD
        self.btn_clear = ctk.CTkButton(
            self.header_frame,
            text="LIMPIAR",
            width=65,
            height=22,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color="#121829",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            border_width=1,
            border_color=Theme.BORDER,
            command=self.clear_logs
        )
        self.btn_clear.pack(side="right", padx=(6, 0))

        self.btn_toggle = ctk.CTkButton(
            self.header_frame,
            text="PLEGAR ▼",
            width=70,
            height=22,
            font=(Theme.FONT_CODE, 10, "bold"),
            fg_color="#121829",
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.NEON_CYAN,
            border_width=1,
            border_color=Theme.BORDER,
            command=self.toggle_expand
        )
        self.btn_toggle.pack(side="right")

        # Área de texto estilo consola de gamer
        self.textbox = ctk.CTkTextbox(
            self,
            font=(Theme.FONT_CODE, 10),
            fg_color="#04060A",
            text_color=Theme.TEXT_PRIMARY,
            wrap="word",
            height=120
        )
        self.textbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self._setup_tags()
        logger.subscribe(self._on_new_log)

    def _setup_tags(self):
        try:
            self.textbox._textbox.tag_config("INFO", foreground="#7DD3FC")
            self.textbox._textbox.tag_config("SUCCESS", foreground=Theme.NEON_GREEN)
            self.textbox._textbox.tag_config("WARNING", foreground=Theme.NEON_GOLD)
            self.textbox._textbox.tag_config("ERROR", foreground=Theme.NEON_RED)
        except Exception:
            pass

    def _on_new_log(self, formatted_message: str, level: str):
        def append():
            try:
                self.textbox._textbox.insert("end", f"> {formatted_message}\n", level)
                self.textbox._textbox.see("end")
            except Exception:
                pass
        self.after(0, append)

    def clear_logs(self):
        self.textbox.delete("1.0", "end")

    def toggle_expand(self):
        if self.is_expanded:
            self.textbox.pack_forget()
            self.btn_toggle.configure(text="EXPANDIR ▲")
            self.is_expanded = False
        else:
            self.textbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))
            self.btn_toggle.configure(text="PLEGAR ▼")
            self.is_expanded = True
