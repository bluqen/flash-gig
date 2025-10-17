import flet as ft
from styles import AppColors
from components.BaseButton import BaseButton


class NewButton(BaseButton):
    """A 'New' button with custom styling."""

    def __init__(self, page, on_click_callback=None):
        self.page = page
        colors = AppColors(page)

        super().__init__(
            text="New",
            icon=ft.Icons.ADD,
            colors=colors,
            on_click_callback=on_click_callback,
        )

        # Custom styling for topbar
        self.style.bgcolor = {
            ft.ControlState.HOVERED: colors["base_button_hover"],
            ft.ControlState.PRESSED: colors["base_button_active"],
            "": colors["topbar_button"],
        }
        self.style.color = colors["topbar_text"]
        self.style.overlay_color = {
            ft.ControlState.PRESSED: colors.get("base_button_active", ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
        }