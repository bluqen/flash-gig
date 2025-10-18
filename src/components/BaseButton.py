import flet as ft


class BaseButton(ft.TextButton):
    """Simple clickable button with icon and label using Flet's ButtonStyle."""

    def __init__(
        self,
        page: ft.Page,
        text: str,
        icon: str,
        active: bool = False,
        on_click_callback=None,
    ):
        self.page = page
        self.active = active
        self.on_click_callback = on_click_callback

        super().__init__(
            text=text,
            icon=icon,
            style=ft.ButtonStyle(
                color=ft.Colors.ON_SURFACE,  # Semantic color
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.TERTIARY_CONTAINER,
                    ft.ControlState.PRESSED: ft.Colors.TERTIARY,
                    ft.ControlState.DEFAULT: ft.Colors.TERTIARY if active else ft.Colors.SECONDARY,
                },
                overlay_color={
                    ft.ControlState.PRESSED: ft.Colors.TERTIARY,
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
            ft.ControlState.HOVERED: ft.Colors.TERTIARY_CONTAINER,
            ft.ControlState.PRESSED: ft.Colors.TERTIARY,
            ft.ControlState.DEFAULT: ft.Colors.TERTIARY if active else ft.Colors.TRANSPARENT,
        }
        self.update()