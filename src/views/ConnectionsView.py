import flet as ft
from styles import AppColors


class ConnectionDetailModal(ft.Container):
    """Modal that shows detailed connection information"""
    
    def __init__(self, page: ft.Page, connection_data: dict, on_close):
        super().__init__()
        self.page = page
        self.colors = AppColors(page)
        self.on_close = on_close
        
        # Status badge
        if connection_data["status"] == "approved":
            status_badge = ft.Container(
                content=ft.Text("Approved", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                bgcolor=ft.Colors.GREEN,
                border_radius=20,
            )
        else:
            status_badge = ft.Container(
                content=ft.Text("Pending", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                bgcolor=ft.Colors.AMBER,
                border_radius=20,
            )
        
        # Modal content
        modal_content = ft.Container(
            content=ft.Column(
                [
                    # Header with close button
                    ft.Row(
                        [
                            ft.Text(
                                "Connection Details",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=self.colors["text"],
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=self.colors["text"],
                                on_click=lambda e: on_close(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    
                    ft.Divider(color=self.colors["border"]),
                    
                    # Connection info
                    ft.Column(
                        [
                            self._create_info_row("Name", connection_data["name"]),
                            self._create_info_row("Project", connection_data["project"]),
                            self._create_info_row("Deadline", connection_data["deadline"]),
                            ft.Row(
                                [
                                    ft.Text("Status:", size=16, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
                                    status_badge,
                                ],
                                spacing=10,
                            ),
                            
                            ft.Divider(color=self.colors["border"]),
                            
                            # Additional details
                            ft.Text("Project Description", size=18, weight=ft.FontWeight.BOLD, color=self.colors["text"]),
                            ft.Text(
                                "This is a detailed description of the project. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                                size=14,
                                color=self.colors["text"],
                            ),
                            
                            ft.Divider(color=self.colors["border"]),
                            
                            # Action buttons
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Send Message",
                                        icon=ft.Icons.MESSAGE,
                                        on_click=lambda e: print(f"Message {connection_data['name']}"),
                                    ),
                                    ft.ElevatedButton(
                                        "View Profile",
                                        icon=ft.Icons.PERSON,
                                        on_click=lambda e: print(f"View profile of {connection_data['name']}"),
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=15,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=500,
            bgcolor=self.colors["card_bg"],
            border_radius=12,
            padding=30,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            ),
        )
        
        # Animation
        modal_content.opacity = 0
        modal_content.scale = 0.9
        
        self.modal_content = modal_content
        self.content = modal_content
    
    def _create_info_row(self, label: str, value: str):
        """Helper to create info rows"""
        return ft.Row(
            [
                ft.Text(f"{label}:", size=16, weight=ft.FontWeight.BOLD, color=self.colors["text"], width=100),
                ft.Text(value, size=16, color=self.colors["text"]),
            ],
            spacing=10,
        )
    
    def animate_in(self):
        """Animate modal entrance"""
        self.modal_content.opacity = 1
        self.modal_content.scale = 1.0
        self.page.update()


class ConnectionCard(ft.Container):
    def __init__(self, page: ft.Page, connection_data: dict, on_click):
        super().__init__()
        self.page = page
        self.colors = AppColors(page)
        self.connection_data = connection_data
        self.on_click_handler = on_click

        # Status badge
        if connection_data["status"] == "approved":
            self.status = ft.Container(
                content=ft.Text(
                    "Approved",
                    color=ft.Colors.WHITE,
                    font_family="Roboto-Bold",
                    size=12,
                ),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                bgcolor=ft.Colors.GREEN,
                border_radius=15,
                alignment=ft.alignment.center,
            )
        else:
            self.status = ft.Container(
                content=ft.Text(
                    "Pending",
                    color=ft.Colors.WHITE,
                    font_family="Roboto-Bold",
                    size=12,
                ),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                bgcolor=ft.Colors.AMBER,
                border_radius=15,
                alignment=ft.alignment.center,
            )

        self.content = ft.Row(
            [
                ft.Container(
                    content=ft.Text(
                        connection_data["name"],
                        color=self.colors["text"],
                        weight=ft.FontWeight.W_500,
                    ),
                    expand=2,
                ),
                ft.Container(
                    content=ft.Text(
                        connection_data["project"],
                        color=self.colors["text"],
                    ),
                    expand=2,
                ),
                ft.Container(
                    content=ft.Text(
                        connection_data["deadline"],
                        color=self.colors["text"],
                    ),
                    expand=1,
                ),
                ft.Container(
                    content=self.status,
                    expand=1,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Make card interactive
        self.padding = 15
        self.border_radius = 10
        self.ink = True
        self.on_click = self._handle_click
        self.on_hover = self._on_hover
        self.animate = ft.Animation(150, ft.AnimationCurve.EASE)
    
    def _on_hover(self, e):
        """Handle hover effect"""
        if e.data == "true":
            self.bgcolor = self.colors["base_button_hover"]
            self.elevation = 2
        else:
            self.bgcolor = None
            self.elevation = 0
        self.update()
    
    def _handle_click(self, e):
        """Handle card click"""
        if self.on_click_handler:
            self.on_click_handler(self.connection_data)

    def before_update(self):
        self.colors = AppColors(self.page)
        super().before_update()


class ConnectionsView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.colors = AppColors(page)
        self.expand = True

        # Sample data for connections
        self.connections_data = [
            {"name": "Alice Johnson", "project": "E-commerce Platform", "deadline": "2024-08-15", "status": "approved"},
            {"name": "Bob Williams", "project": "Mobile Banking App", "deadline": "2024-09-01", "status": "pending"},
            {"name": "Charlie Brown", "project": "AI Chatbot Integration", "deadline": "2024-07-30", "status": "approved"},
            {"name": "Diana Miller", "project": "Cloud Migration", "deadline": "2024-10-10", "status": "pending"},
            {"name": "Ethan Davis", "project": "Data Analytics Dashboard", "deadline": "2024-08-22", "status": "approved"},
            {"name": "Fiona Garcia", "project": "Social Media Campaign", "deadline": "2024-09-18", "status": "approved"},
            {"name": "George Rodriguez", "project": "Website Redesign", "deadline": "2024-11-05", "status": "pending"},
            {"name": "Hannah Wilson", "project": "Inventory Management", "deadline": "2024-07-25", "status": "approved"},
            {"name": "Ian Martinez", "project": "CRM Overhaul", "deadline": "2024-08-05", "status": "pending"},
            {"name": "Jessica Anderson", "project": "User Authentication Service", "deadline": "2024-09-25", "status": "approved"},
            {"name": "Kevin Thomas", "project": "API Development", "deadline": "2024-10-01", "status": "pending"},
            {"name": "Laura Taylor", "project": "Logo & Brand Guide", "deadline": "2024-08-12", "status": "approved"},
            {"name": "Michael Moore", "project": "Video Ad Production", "deadline": "2024-09-09", "status": "pending"},
            {"name": "Nancy Jackson", "project": "SEO Optimization", "deadline": "2024-11-20", "status": "approved"},
            {"name": "Oscar White", "project": "Internal Wiki Setup", "deadline": "2024-07-28", "status": "approved"},
        ]

        # Create cards with click handler
        cards = [
            ConnectionCard(page, item, self._show_connection_detail)
            for item in self.connections_data
        ]

        # Add dividers between cards
        cards_with_dividers = []
        for i, card in enumerate(cards):
            cards_with_dividers.append(card)
            if i < len(cards) - 1:
                cards_with_dividers.append(ft.Divider(color=self.colors["border"], height=1))

        self.content = ft.Column(
            [
                ft.Text(
                    "Connections",
                    size=32,
                    font_family="Roboto-Bold",
                    color=self.colors["text"],
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            cards_with_dividers,
                            spacing=5,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        padding=20,
                    ),
                    expand=True,
                ),
            ],
        )
    
    def _show_connection_detail(self, connection_data: dict):
        """Show connection detail modal"""
        # Create backdrop
        backdrop = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            on_click=lambda e: self._close_modal(),
            animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE),
        )
        
        # Create modal
        modal = ConnectionDetailModal(self.page, connection_data, self._close_modal)
        
        # Position modal in center
        modal_positioned = ft.Container(
            content=modal,
            alignment=ft.alignment.center,
        )
        
        # Create overlay stack
        self.modal_stack = ft.Stack(
            [backdrop, modal_positioned],
            expand=True,
        )
        
        # Add to page overlay
        self.page.overlay.append(self.modal_stack)
        self.page.update()
        
        # Animate in
        modal.animate_in()
    
    def _close_modal(self):
        """Close the modal"""
        if hasattr(self, 'modal_stack') and self.modal_stack in self.page.overlay:
            self.page.overlay.remove(self.modal_stack)
            self.page.update()
    
    def before_update(self):
        self.colors = AppColors(self.page)
        super().before_update()