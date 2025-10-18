import flet as ft
from components.NewConnectionDialog import show_new_connection_dialog
from components.CreateProjectDialog import show_create_project_dialog


class NewButton(ft.Container):
    """A button with custom dropdown menu for creating new items."""
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.menu_open = False
        
        # Main button
        self.button = ft.ElevatedButton(
            text="New",
            icon=ft.Icons.ADD,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: ft.Colors.PRIMARY,
                    ft.ControlState.HOVERED: ft.Colors.PRIMARY_CONTAINER,
                },
                color=ft.Colors.ON_PRIMARY,
            ),
            on_click=self._toggle_menu,
        )
        
        self.content = self.button
    
    def _toggle_menu(self, e):
        """Show/hide the custom dropdown menu"""
        print(f"NewButton clicked, menu_open: {self.menu_open}")  # Debug
        
        if not self.menu_open:
            self._show_menu()
        else:
            self._hide_menu()
    
    def _show_menu(self):
        """Display custom menu in overlay"""
        print("Showing menu...")  # Debug
        self.menu_open = True
        
        # Create menu items
        menu_items = ft.Column(
            [
                self._create_menu_item("New Connection", ft.Icons.PEOPLE_OUTLINE, self._show_connection_dialog),
                ft.Divider(height=1, color=ft.Colors.OUTLINE),
                self._create_menu_item("New Project", ft.Icons.FOLDER_OPEN_OUTLINED, self._show_project_dialog),
            ],
            spacing=0,
            tight=True,
        )
        
        # Menu container with styling
        menu = ft.Container(
            content=menu_items,
            bgcolor="surfacevariant",
            border_radius=8,
            padding=8,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            ),
            width=200,
        )
        
        # Create backdrop
        backdrop = ft.Container(
            expand=True,
            on_click=lambda e: self._hide_menu(),
            bgcolor=ft.Colors.with_opacity(0, ft.Colors.BLACK),
        )
        
        # Position menu below button (adjust 'top' and 'right' as needed)
        menu_positioned = ft.Container(
            content=menu,
            top=70,  # Adjust based on your TopBar height
            right=120,  # Adjust based on button position
        )
        
        # Create overlay stack
        self.overlay_stack = ft.Stack(
            [backdrop, menu_positioned],
            expand=True,
        )
        
        # Add to page overlay
        print("Adding menu to page.overlay")  # Debug
        self.page.overlay.append(self.overlay_stack)
        self.page.update()
        print("Menu added to overlay")  # Debug
    
    def _hide_menu(self):
        """Remove menu from overlay"""
        print("Hiding menu...")  # Debug
        if self.menu_open and hasattr(self, 'overlay_stack'):
            self.menu_open = False
            if self.overlay_stack in self.page.overlay:
                self.page.overlay.remove(self.overlay_stack)
                self.page.update()
                print("Menu removed from overlay")  # Debug
    
    def _create_menu_item(self, text: str, icon: str, on_click):
        """Create a styled menu item"""
        container = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Text(text, size=14, color=ft.Colors.ON_SURFACE_VARIANT),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            border_radius=6,
            ink=True,
            on_click=on_click,
            on_hover=self._on_item_hover,
            animate=ft.Animation(150, ft.AnimationCurve.EASE),
        )
        return container
    
    def _on_item_hover(self, e):
        """Hover effect for menu items"""
        if e.data == "true":
            e.control.bgcolor = ft.Colors.TERTIARY_CONTAINER
        else:
            e.control.bgcolor = None
        e.control.update()
    
    def _show_connection_dialog(self, e):
        """Show new connection dialog"""
        print("Menu item clicked: New Connection")  # Debug
        self._hide_menu()
        print(f"Calling show_new_connection_dialog with page: {self.page is not None}")  # Debug
        show_new_connection_dialog(self.page, on_success=self._on_action_success)
    
    def _show_project_dialog(self, e):
        """Show create project dialog"""
        print("Menu item clicked: New Project")  # Debug
        self._hide_menu()
        print(f"Calling show_create_project_dialog with page: {self.page is not None}")  # Debug
        show_create_project_dialog(self.page, on_success=self._on_action_success)
    
    def _on_action_success(self):
        """Generic success handler for dialogs"""
        print("Action success callback called")  # Debug
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Action completed successfully!"),
            bgcolor=ft.Colors.GREEN,
        )
        self.page.snack_bar.open = True
        self.page.update()