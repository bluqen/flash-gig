import flet as ft
from styles import AppColors

class BaseButton(ft.TextButton):
    """Simple clickable button with icon and label using Flet's ButtonStyle."""

    def __init__(
        self,
        text: str,
        icon: str,
        colors: AppColors,
        active: bool = False,
        on_click_callback=None,
    ):
        self.colors = colors
        self.active = active
        self.on_click_callback = on_click_callback

        super().__init__(
            text=text,
            icon=icon,
            style=ft.ButtonStyle(
                color=colors["text"],
                bgcolor={
                    ft.ControlState.HOVERED: colors["base_button_hover"],
                    ft.ControlState.PRESSED: colors["base_button_active"],
                    ft.ControlState.DEFAULT: colors["base_button_active"] if active else colors["base_button"],
                },
                overlay_color={
                    ft.ControlState.PRESSED: colors.get("base_button_active", ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                },
                padding=ft.padding.symmetric(vertical=10, horizontal=15),
                shape=ft.RoundedRectangleBorder(radius=8),
                animation_duration=200,
            ),
            on_click=self._handle_click,
        )

    def _handle_click(self, e):
        """Handle button click."""
        if self.on_click_callback:
            self.on_click_callback(self)

    def set_active(self, active: bool):
        """Set active state (for navigation buttons)."""
        self.active = active
        self.style.bgcolor = {
            ft.ControlState.HOVERED: self.colors["base_button_hover"],
            ft.ControlState.PRESSED: self.colors["base_button_active"],
            "": self.colors["base_button_active"] if active else ft.Colors.TRANSPARENT,
        }
        self.update()

    def before_update(self):
        """Refresh colors when theme updates."""
        self.style.color = self.colors["text"]
        self.style.bgcolor = {
            ft.ControlState.HOVERED: self.colors["base_button_hover"],
            ft.ControlState.PRESSED: self.colors["base_button_active"],
            ft.ControlState.DEFAULT: self.colors["base_button_active"] if self.active else self.colors["base_button"],
        }
        self.style.overlay_color = {
            ft.ControlState.PRESSED: self.colors.get("base_button_active", ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
        }
        super().before_update()