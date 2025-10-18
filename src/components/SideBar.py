import flet as ft
from components.GradientText import GradientText


class SideBarLink(ft.Container):
    """Single clickable sidebar item with icon and label."""

    def __init__(
        self,
        page: ft.Page,
        text: str,
        icon: str,
        active: bool = False,
        on_click_callback=None,
        route: str = None,
    ):
        super().__init__()

        self.page = page
        self.text = text
        self.icon = icon
        self.active = active
        self.on_click_callback = on_click_callback
        self.route = route

        self.padding = ft.padding.symmetric(vertical=10, horizontal=15)
        self.border_radius = 8
        # Use semantic colors that update automatically
        self.bgcolor = ft.Colors.TERTIARY if active else ft.Colors.TRANSPARENT
        self.cursor = ft.MouseCursor.CLICK
        self.ink = True
        
        self.on_click = self._handle_click
        self.on_hover = self._handle_hover

        # Create text with opacity animation - use semantic color
        self.text_widget = ft.Text(
            self.text,
            size=14,
            weight=ft.FontWeight.W_500,
            color="white",  # Semantic color
            opacity=1,
            animate_opacity=300,
        )

        self.icon_widget = ft.Icon(
            self.icon, 
            size=20, 
            color="white"  # Semantic color
        )

        self.content = ft.Row(
            [
                self.icon_widget,
                self.text_widget,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _handle_click(self, e):
        """Handle click event."""
        print(f"Link clicked: {self.text}, route: {self.route}")
        
        self.active = True
        self.toggle_active(True)
        
        if self.on_click_callback:
            print(f"Calling callback for {self.text}")
            self.on_click_callback(self)
        else:
            print(f"No callback for {self.text}")

    def _handle_hover(self, e):
        """Handle hover effect."""
        if e.data == "true":
            if not self.active:
                self.bgcolor = ft.Colors.TERTIARY_CONTAINER
                self.update()
        else:
            if not self.active:
                self.bgcolor = ft.Colors.TRANSPARENT
                self.update()

    def toggle_active(self, active: bool):
        """Update active state color."""
        self.active = active
        self.bgcolor = ft.Colors.TERTIARY if active else ft.Colors.TRANSPARENT
        self.update()

    def set_collapsed(self, collapsed: bool):
        """Update the link's appearance for the collapsed state with smooth animation."""
        if collapsed:
            self.text_widget.opacity = 0
            self.text_widget.visible = False
            self.content.alignment = ft.MainAxisAlignment.CENTER
            self.padding = ft.padding.symmetric(vertical=10, horizontal=10)
        else:
            self.text_widget.visible = True
            self.text_widget.opacity = 1
            self.content.alignment = ft.MainAxisAlignment.START
            self.padding = ft.padding.symmetric(vertical=10, horizontal=15)
        
        self.update()


class SideBar(ft.Container):
    """Main sidebar container with gradient title and link list."""

    def __init__(self, page: ft.Page, on_navigate=None):
        super().__init__()

        self.page = page
        self.collapsed = False
        self.on_navigate = on_navigate

        self.expanded_width = 220
        self.collapsed_width = 80

        self.width = self.expanded_width
        self.height = None
        self.padding = 20
        self.bgcolor = ft.Colors.SURFACE_TINT  # Semantic color
        self.animate = ft.Animation(300, ft.AnimationCurve.EASE_OUT)

        self.title_text = GradientText(
            "Flash Gig",
            size=22,
            colors=[ft.Colors.BLUE, "#CCCBCB"], 
            font="Funnel-Bold"
        )
        self.title_text.opacity = 1
        self.title_text.animate_opacity = 300

        logo = ft.Image(
            src="icon.png",
            width=24,
            height=24,
            fit=ft.ImageFit.CONTAIN,
        )

        self.logo_container = ft.Container(
            content=logo, 
            width=24, 
            height=24
        )

        self.title_row = ft.Row(
            [self.logo_container, self.title_text],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.title_container = ft.Container(
            content=self.title_row,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            height=40,
        )

        # Create divider with semantic color
        self.divider = ft.Divider(height=15, color=ft.Colors.OUTLINE)

        # Create sidebar links
        self.links = [
            SideBarLink(page, "Home", ft.Icons.HOME, active=True, 
                       on_click_callback=self._handle_link_click, route="home"),
            SideBarLink(page, "Connections", ft.Icons.PEOPLE, 
                       on_click_callback=self._handle_link_click, route="connections"),
        ]

        # Layout
        self.content = ft.Column(
            [
                self.title_container,
                self.divider,
                *self.links,
            ],
            spacing=8,
            alignment="start",
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

    def _handle_link_click(self, clicked_link):
        """Handle when a sidebar link is clicked - deactivate others and navigate."""
        for link in self.links:
            if link != clicked_link:
                link.toggle_active(False)
        
        if self.on_navigate and hasattr(clicked_link, 'route'):
            print(f"Navigating to: {clicked_link.route}")
            self.on_navigate(clicked_link.route)
        else:
            print(f"No navigation callback or route not found")

    def toggle_collapse(self):
        """Public method to toggle the sidebar's collapsed state with smooth animations."""
        self.collapsed = not self.collapsed

        self.width = self.collapsed_width if self.collapsed else self.expanded_width
        self.padding = 10 if self.collapsed else 20

        if self.collapsed:
            self.title_text.opacity = 0
            self.title_text.visible = False
            self.title_row.alignment = ft.MainAxisAlignment.CENTER
        else:
            self.title_text.visible = True
            self.title_text.opacity = 1
            self.title_row.alignment = ft.MainAxisAlignment.START

        for link in self.links:
            link.set_collapsed(self.collapsed)

        self.update()


class SideMenuButton(ft.IconButton):
    """Button to toggle the collapse state of the SideBar."""

    def __init__(self, sidebar_ref: SideBar):
        super().__init__()
        self.sidebar_ref = sidebar_ref
        self.icon = ft.Icons.MENU
        self.icon_size = 24
        self.tooltip = "Toggle Sidebar"
        self.on_click = self._handle_click

    def _handle_click(self, e: ft.ControlEvent):
        """Calls the public method on the referenced sidebar."""
        self.sidebar_ref.toggle_collapse()