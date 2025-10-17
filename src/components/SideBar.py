import flet as ft
from components.GradientText import GradientText
from styles import AppColors


class SideBarLink(ft.Container):
    """Single clickable sidebar item with icon and label."""

    def __init__(
        self,
        text: str,
        icon: str,
        colors: AppColors,
        active: bool = False,
        on_click_callback=None,
        route: str = None,
    ):
        super().__init__()

        self.text = text
        self.icon = icon
        self.colors = colors
        self.active = active
        self.on_click_callback = on_click_callback
        self.route = route  # Store route name

        self.padding = ft.padding.symmetric(vertical=10, horizontal=15)
        self.border_radius = 8
        self.bgcolor = (
            self.colors["sidebar_button_active"] if self.active else "transparent"
        )
        self.cursor = ft.MouseCursor.CLICK
        self.ink = True  # CRITICAL: Makes container clickable with ripple effect
        # Removed: self.animate - no animation on hover
        
        # CRITICAL: Set handlers AFTER super().__init__()
        self.on_click = self._handle_click
        self.on_hover = self._handle_hover
        
        print(f"Created link: {text}, route: {route}, has callback: {on_click_callback is not None}")  # Debug

        # Create text with opacity animation
        self.text_widget = ft.Text(
            self.text,
            size=14,
            weight=ft.FontWeight.W_500,
            color=self.colors["topbar_text"],
            opacity=1,
            animate_opacity=300,  # Smooth fade in/out
        )

        self.icon_widget = ft.Icon(
            self.icon, 
            size=20, 
            color=self.colors["topbar_text"]
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
        print(f"Link clicked: {self.text}, route: {self.route}")  # Debug
        
        self.active = True
        self.toggle_active(True)
        
        # Call the callback with self as argument
        if self.on_click_callback:
            print(f"Calling callback for {self.text}")  # Debug
            self.on_click_callback(self)
        else:
            print(f"No callback for {self.text}")  # Debug

    def _handle_hover(self, e):
        """Handle hover effect."""
        if e.data == "true":  # Mouse entered
            if not self.active:
                self.bgcolor = self.colors["sidebar_button_hover"]
                self.update()
        else:  # Mouse left
            if not self.active:
                self.bgcolor = "transparent"
                self.update()

    def toggle_active(self, active: bool):
        """Update active state color."""
        self.active = active
        self.bgcolor = self.colors["sidebar_button_active"] if active else "transparent"
        self.update()

    def set_collapsed(self, collapsed: bool):
        """Update the link's appearance for the collapsed state with smooth animation."""
        if collapsed:
            # Fade out text, hide it, and center icon
            self.text_widget.opacity = 0
            self.text_widget.visible = False  # Actually remove from layout
            self.content.alignment = ft.MainAxisAlignment.CENTER
            self.padding = ft.padding.symmetric(vertical=10, horizontal=10)
        else:
            # Show text, fade in, and align left
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
        self.colors = AppColors(page)
        self.collapsed = False  # Initial state is expanded
        self.on_navigate = on_navigate  # Navigation callback

        # Define the width properties for the transition
        self.expanded_width = 220
        self.collapsed_width = 80  # Width when collapsed (just enough for icons)

        self.width = self.expanded_width
        self.height = None  # Let it take available height
        self.padding = 20
        self.bgcolor = self.colors["sidebar_bg"]
        self.animate = ft.Animation(300, ft.AnimationCurve.EASE_OUT)

        self.title_text = GradientText(
            "Flash Gig",
            size=22,
            colors=[ft.Colors.BLUE, "#CCCBCB"], font="Funnel-Bold"
        )
        # Add opacity animation to title
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
        
        # Wrap title_row in animated container with fixed height
        self.title_container = ft.Container(
            content=self.title_row,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            height=40,  # Fixed height to prevent size changes
        )

        # Create sidebar links with click handler and route names
        self.links = [
            SideBarLink("Home", ft.Icons.HOME, self.colors, active=True, 
                       on_click_callback=self._handle_link_click, route="home"),
            SideBarLink("Explore", ft.Icons.EXPLORE, self.colors, 
                       on_click_callback=self._handle_link_click, route="explore"),
            SideBarLink("Settings", ft.Icons.SETTINGS, self.colors, 
                       on_click_callback=self._handle_link_click, route="settings"),
        ]

        # Layout
        self.content = ft.Column(
            [
                self.title_container,
                ft.Divider(height=15, color=self.colors["border"]),
                *self.links,
            ],
            spacing=8,
            alignment="start",
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

    def _handle_link_click(self, clicked_link):
        """Handle when a sidebar link is clicked - deactivate others and navigate."""
        # Deactivate all other links
        for link in self.links:
            if link != clicked_link:
                link.toggle_active(False)
        
        # Call navigation callback if provided
        if self.on_navigate and hasattr(clicked_link, 'route'):
            print(f"Navigating to: {clicked_link.route}")  # Debug
            self.on_navigate(clicked_link.route)
        else:
            print(f"No navigation callback or route not found")  # Debug

    def toggle_collapse(self):
        """Public method to toggle the sidebar's collapsed state with smooth animations."""
        self.collapsed = not self.collapsed

        # Update the overall container width
        self.width = self.collapsed_width if self.collapsed else self.expanded_width
        self.padding = 10 if self.collapsed else 20

        # Fade out/in AND hide/show title text
        if self.collapsed:
            self.title_text.opacity = 0
            self.title_text.visible = False  # Remove from layout
            self.title_row.alignment = ft.MainAxisAlignment.CENTER
        else:
            self.title_text.visible = True
            self.title_text.opacity = 1
            self.title_row.alignment = ft.MainAxisAlignment.START

        # Update links with animation
        for link in self.links:
            link.set_collapsed(self.collapsed)

        self.update()

    def before_update(self):
        # Update colors when theme changes
        self.bgcolor = self.colors["sidebar_bg"]
        super().before_update()


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