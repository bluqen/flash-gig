import flet as ft
import json, os
import urllib.request
import urllib.error

from components.TopBar import TopBar
from components.SideBar import SideBar
from components.LoginOverlay import show_login_overlay
from views.HomeView import HomeView
from views.ConnectionsView import ConnectionsView

from api_client import server_post

class ContentRouter:
    """Manages content switching based on navigation"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = None
        self.current_route = "home"

        # Map route names to view classes
        self.routes = {
            "home": HomeView,
            "connections": ConnectionsView,
        }

        # Container that holds the current view
        self.content_container = ft.Container(
            expand=True,
            bgcolor=ft.Colors.SURFACE,  # Use semantic color
            padding=20,
        )

    def navigate(self, route_name: str):
        """Switch to a different view"""
        print(f"Router navigate called with: {route_name}")

        if route_name in self.routes:
            self.current_route = route_name
            view_class = self.routes[route_name]
            self.current_view = view_class(self.page)
            print(f"Created view: {self.current_view}")

            self.content_container.content = self.current_view

            if self.content_container.page:
                print("Updating container")
                self.content_container.update()
            else:
                print("Container not on page yet")
        else:
            print(f"Route '{route_name}' not found in routes")
    
    def reload_current_view(self):
        """Reload the current view - useful after login"""
        if self.current_route:
            self.navigate(self.current_route)

    def get_container(self):
        """Returns the content container"""
        return self.content_container


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "Roboto": "fonts/Roboto-Regular.ttf",
        "Roboto-Medium": "fonts/Roboto-Medium.ttf",
        "Roboto-Bold": "fonts/Roboto-Bold.ttf",
        "Boldonse": "fonts/Boldonse-Regular.ttf",
        "Funnel-Bold": "fonts/FunnelDisplay-ExtraBold.ttf",
    }
    
    # Light theme with your custom colors
    page.theme = ft.Theme(
        font_family="Roboto",
        color_scheme=ft.ColorScheme(
            primary="#2196f3",                  # accent light
            on_primary="#ffffff",
            secondary="#e0e0e0",                # base_button light
            on_secondary="#000000",
            surface="#ffffff",                  # topbar_bg light
            on_surface="#000000",               # text light
            surface_variant="#f5f5f5",         # card_bg light
            on_surface_variant="#000000",
            outline="#e0e0e0",                 # border light
            surface_tint="#1b1b2b",            # sidebar_bg
            tertiary="#3682c0",                # button_active
            on_tertiary="#ffffff",
            tertiary_container="#C7C7C7",      # button_hover light
            inverse_surface="#1b1b2b",
            inverse_primary="#202236",
        ),
    )
    
    # Dark theme with your custom colors
    page.dark_theme = ft.Theme(
        font_family="Roboto",
        color_scheme=ft.ColorScheme(
            primary="#64b5f6",                  # accent dark
            on_primary="#000000",
            secondary="#1b1b2b",                # base_button dark
            on_secondary="#ffffff",
            surface="#111519",                  # topbar_bg dark
            on_surface="#ffffff",               # text dark
            surface_variant="#252525",         # card_bg dark
            on_surface_variant="#ffffff",
            outline="#404040",                 # border dark
            surface_tint="#1b1b2b",            # sidebar_bg
            tertiary="#3682c0",                # button_active
            on_tertiary="#ffffff",
            tertiary_container="#202236",      # button_hover dark
            inverse_surface="#ffffff",
            inverse_primary="#000000",
        ),
    )
    
    page.title = "Flash Gig"
    page.padding = 0
    page.spacing = 0
    page.window.icon = "icon.ico"

    # Create router
    router = ContentRouter(page)

    # Create sidebar with navigation callback
    sidebar = SideBar(page, on_navigate=router.navigate)

    # Main layout
    page.add(
        ft.Row(
            [
                # Sidebar - fixed width, full height
                ft.Container(
                    content=sidebar,
                    expand=False,
                ),
                # Right side content area
                ft.Container(
                    content=ft.Column(
                        [
                            TopBar(page, sidebar),
                            # Dynamic content area
                            router.get_container(),
                        ],
                        spacing=0,
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
    )

    # Set initial view AFTER adding to page
    router.navigate("home")

    # Show blocking login overlay once at app start
    # Pass callback to reload views after login
    def on_login_success():
        """Called after successful login"""
        print("Login successful, reloading views...")
        router.reload_current_view()
    
    show_login_overlay(page, on_success=on_login_success)


ft.app(main, assets_dir="assets")