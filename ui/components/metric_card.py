import customtkinter as ctk
from ui.theme import Theme

class MetricCard(ctk.CTkFrame):
    """Tarjeta de telemetría moderna y minimalista con diseño sobrio y limpio."""

    def __init__(
        self,
        master,
        title: str,
        value: str = "--",
        subtext: str = "",
        accent_color: str = Theme.PRIMARY,
        show_progress: bool = True,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=Theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=Theme.BORDER,
            **kwargs
        )
        self.accent_color = accent_color

        # Contenedor interno
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=14)

        # Fila superior: Indicador sutil y título
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 4))

        # Dot indicador de color suave
        dot = ctk.CTkFrame(
            top_row,
            width=8,
            height=8,
            corner_radius=4,
            fg_color=accent_color
        )
        dot.pack(side="left", padx=(0, 8))

        self.title_label = ctk.CTkLabel(
            top_row,
            text=title,
            font=(Theme.FONT_FAMILY, 11, "bold"),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w"
        )
        self.title_label.pack(side="left", fill="x", expand=True)

        # Valor métrico
        self.value_label = ctk.CTkLabel(
            content,
            text=value,
            font=(Theme.FONT_FAMILY_TITLE, 26, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        )
        self.value_label.pack(fill="x", pady=(2, 6))

        self.show_progress = show_progress
        if show_progress:
            self.progress_bar = ctk.CTkProgressBar(
                content,
                height=4,
                progress_color=accent_color,
                fg_color="#1E2230",
                corner_radius=2
            )
            self.progress_bar.set(0)
            self.progress_bar.pack(fill="x", pady=(0, 6))

        # Subtexto informativo
        self.subtext_label = ctk.CTkLabel(
            content,
            text=subtext,
            font=(Theme.FONT_CODE, 10),
            text_color=Theme.TEXT_MUTED,
            anchor="w"
        )
        self.subtext_label.pack(fill="x")

    def update_data(self, value: str, subtext: str = None, percent: float = None):
        self.value_label.configure(text=value)
        if subtext is not None:
            self.subtext_label.configure(text=subtext)
        if self.show_progress and percent is not None:
            clamped = max(0.0, min(1.0, percent / 100.0))
            self.progress_bar.set(clamped)
