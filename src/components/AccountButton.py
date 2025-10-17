import flet as ft
from styles import AppColors


class AccountMenu(ft.Container):
    """Popup menu that shows account info and actions"""
    
    def __init__(self, page: ft.Page, account_info: dict, on_logout=None, on_close=None):
        super().__init__()
        self.page = page
        self.colors = AppColors(page)
        self.on_logout = on_logout
        self.on_close = on_close
        
        self.width = 280
        self.bgcolor = self.colors["card_bg"]
        self.border_radius = 12
        self.padding = 16
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        )
        
        # Smooth animations
        self.animate_opacity = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        self.animate_scale = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        self.animate_offset = ft.Animation(200, ft.AnimationCurve.EASE_OUT)
        
        # Profile section
        profile_section = ft.Row(
            [
                ft.Container(
                    content=ft.Image(
                        src=account_info["image"],
                        width=48,
                        height=48,
                        fit=ft.ImageFit.COVER,
                        border_radius=ft.border_radius.all(24),
                    ),
                    width=48,
                    height=48,
                    border_radius=24,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
                ft.Column(
                    [
                        ft.Text(
                            account_info["name"],
                            size=16,
                            font_family="Roboto-Bold",
                            color=self.colors["text"],
                        ),
                        ft.Text(
                            account_info["email"],
                            size=12,
                            color=self.colors["text"],
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Menu items
        menu_items = ft.Column(
            [
                self._create_menu_item("Profile", ft.Icons.PERSON, self._on_profile_click),
                self._create_menu_item("Settings", ft.Icons.SETTINGS, self._on_settings_click),
                ft.Divider(height=1, color=self.colors["border"]),
                self._create_menu_item("Logout", ft.Icons.LOGOUT, self._on_logout_click),
            ],
            spacing=4,
        )
        
        self.content = ft.Column(
            [profile_section, ft.Divider(height=1, color=self.colors["border"]), menu_items],
            spacing=12,
        )
    
    def _create_menu_item(self, text: str, icon: str, on_click):
        """Helper to create menu items with hover animation"""
        container = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=self.colors["text"]),
                    ft.Text(text, size=14, color=self.colors["text"]),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=8, vertical=10),
            border_radius=8,
            ink=True,
            on_click=on_click,
            on_hover=self._on_hover,
            animate=ft.Animation(150, ft.AnimationCurve.EASE),
        )
        return container
    
    def _on_hover(self, e):
        if e.data == "true":
            e.control.bgcolor = self.colors["base_button_hover"]
        else:
            e.control.bgcolor = None
        e.control.update()
    
    def _on_profile_click(self, e):
        print("Profile clicked")
        if self.on_close:
            self.on_close()
    
    def _on_settings_click(self, e):
        print("Settings clicked")
        if self.on_close:
            self.on_close()
    
    def _on_logout_click(self, e):
        print("Logout clicked")
        if self.on_close:
            self.on_close()
        if self.on_logout:
            self.on_logout()
    
    def before_update(self):
        self.colors = AppColors(self.page)
        self.bgcolor = self.colors["card_bg"]
        super().before_update()


class AccountButton(ft.Container):
    """Account button with animated dropdown menu"""
    
    def __init__(self, page: ft.Page, account_info: dict):
        super().__init__()
        self.page = page
        self.colors = AppColors(page)
        self.account_info = account_info
        self.menu_open = False
        
        # Avatar button with circular image
        self.avatar_button = ft.Container(
            content=ft.Container(
                content=ft.Image(
                    src=account_info["image"],
                    width=40,
                    height=40,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(20),
                ),
                width=40,
                height=40,
                border_radius=20,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            ),
            border=ft.border.all(2, self.colors["accent"]),
            border_radius=20,
            ink=True,
            on_click=self._toggle_menu,
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE),
        )
        
        self.content = self.avatar_button
    
    def _toggle_menu(self, e):
        """Show/hide the menu with animation"""
        if not self.menu_open:
            self._show_menu()
        else:
            self._hide_menu()
        
        # Subtle scale effect on avatar click
        self.avatar_button.scale = 0.95
        self.avatar_button.update()
        
        # Reset scale
        import time
        time.sleep(0.05)
        self.avatar_button.scale = 1.0
        self.avatar_button.update()
    
    def _show_menu(self):
        """Display menu in overlay with animation"""
        self.menu_open = True
        
        # Create menu
        menu = AccountMenu(
            self.page, 
            self.account_info, 
            on_logout=self._handle_logout,
            on_close=self._hide_menu
        )
        
        # Set initial animation state (hidden)
        menu.opacity = 0
        menu.scale = 0.95
        menu.offset = ft.Offset(0, -0.1)
        
        # Create backdrop that closes menu when clicked
        backdrop = ft.Container(
            expand=True,
            on_click=lambda e: self._hide_menu(),
            bgcolor=ft.Colors.with_opacity(0, ft.Colors.BLACK),
            animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE),
        )
        
        # Position menu in top-right
        menu_positioned = ft.Container(
            content=menu,
            top=70,
            right=20,
        )
        
        # Create overlay stack
        self.overlay_stack = ft.Stack(
            [backdrop, menu_positioned],
            expand=True,
        )
        
        # Add to page overlay
        self.page.overlay.append(self.overlay_stack)
        self.page.update()
        
        # Trigger animations after adding to DOM
        menu.opacity = 1
        menu.scale = 1.0
        menu.offset = ft.Offset(0, 0)
        backdrop.bgcolor = ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
        self.page.update()
    
    def _hide_menu(self):
        """Remove menu from overlay with animation"""
        if self.menu_open and hasattr(self, 'overlay_stack'):
            self.menu_open = False
            
            # Get the menu and backdrop for animation
            if len(self.overlay_stack.controls) >= 2:
                backdrop = self.overlay_stack.controls[0]
                menu_container = self.overlay_stack.controls[1]
                menu = menu_container.content
                
                # Animate out
                menu.opacity = 0
                menu.scale = 0.95
                menu.offset = ft.Offset(0, -0.1)
                backdrop.bgcolor = ft.Colors.with_opacity(0, ft.Colors.BLACK)
                self.page.update()
                
                # Remove after animation completes
                import time
                time.sleep(0.2)
            
            if self.overlay_stack in self.page.overlay:
                self.page.overlay.remove(self.overlay_stack)
                self.page.update()
    
    def _handle_logout(self):
        """Handle logout action"""
        self._hide_menu()
        print("User logged out")
        # Add your logout logic here
    
    def before_update(self):
        self.colors = AppColors(self.page)
        super().before_update()