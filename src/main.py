import flet as ft
from components.TopBar import TopBar
from components.SideBar import SideBar
from views.HomeView import HomeView
from views.ExploreView import ExploreView
from views.ConnectionsView import ConnectionsView


class ContentRouter:
    """Manages content switching based on navigation"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = None

        # Map route names to view classes
        self.routes = {
            "home": HomeView,
            "explore": ExploreView,
            "settings": ConnectionsView,
        }

        # Container that holds the current view
        self.content_container = ft.Container(
            expand=True,
            bgcolor=ft.Colors.SURFACE,
            padding=20,
        )

    def navigate(self, route_name: str):
        """Switch to a different view"""
        print(f"Router navigate called with: {route_name}")  # Debug

        if route_name in self.routes:
            # Create new view instance
            view_class = self.routes[route_name]
            self.current_view = view_class(self.page)

            print(f"Created view: {self.current_view}")  # Debug

            # Update content container
            self.content_container.content = self.current_view

            # Only update if container is already on the page
            if self.content_container.page:
                print("Updating container")  # Debug
                self.content_container.update()
            else:
                print("Container not on page yet")  # Debug
        else:
            print(f"Route '{route_name}' not found in routes")  # Debug

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
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE, font_family="Roboto")
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


ft.app(main, assets_dir="assets")
