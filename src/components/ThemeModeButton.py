import flet as ft

class ThemeModeButton(ft.IconButton):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.selected_icon = ft.Icons.DARK_MODE
        self.unselected_icon = ft.Icons.LIGHT_MODE
        self.icon = self.selected_icon if self.page.theme_mode == ft.ThemeMode.DARK else self.unselected_icon
        self.on_click = self.toggle_theme_mode

    def toggle_theme_mode(self, e):
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.icon = self.unselected_icon
        else:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.icon = self.selected_icon
        
        self.update()
        self.page.update()
