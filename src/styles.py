import flet as ft

class AppColors:
    """Define your own color names with clean dictionary syntax"""
    
    COLORS = {
        "text": {"light": "#000000", "dark": "#ffffff"},
        "text-white": {"light": "#ffffff", "dark": "#000000"},
        "topbar_bg": {"light": "#ffffff", "dark": "#111519"},
        "topbar_text": {"light": "#000000", "dark": "#ffffff"},
        "topbar_button": {"light": "#e0e0e0", "dark": "#1b1b2b"},
        "card_bg": {"light": "#f5f5f5", "dark": "#252525"},
        "accent": {"light": "#2196f3", "dark": "#64b5f6"},
        "border": {"light": "#e0e0e0", "dark": "#404040"},
        "sidebar_bg": {"light": "#1b1b2b", "dark": "#1b1b2b"},
        "sidebar_button_active": {"light": "#3682c0", "dark": "#3682c0"},
        "sidebar_button_hover": {"light": "#202236", "dark": "#202236"},
        "base_button": {"light": "#e0e0e0", "dark": "#1b1b2b"},
        "base_button_active": {"light": "#3682c0", "dark": "#3682c0"},
        "base_button_hover": {"light": "#202236", "dark": "#202236"},
    }
    
    def __init__(self, page: ft.Page):
        self.page = page
    
    def __getitem__(self, color_name: str) -> str:
        """Get color based on current theme mode"""
        mode = "dark" if self.page.theme_mode == ft.ThemeMode.DARK else "light"
        return self.COLORS[color_name][mode]
    
    def get(self, color_name: str, default: str = None):
        if color_name in self.COLORS.keys():
            return self.__getitem__(color_name)
        return default