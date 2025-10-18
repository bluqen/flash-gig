import flet as ft
from api_client import server_get, server_patch, APIClientError


class ConnectionCard(ft.Container):
    def __init__(self, page: ft.Page, connection_data: dict, on_action=None):
        super().__init__()
        self.page = page
        self.connection_data = connection_data
        self.on_action = on_action
        
        # Determine if this is incoming or outgoing
        current_user = page.session_username
        is_incoming = connection_data["to_username"] == current_user
        other_user = connection_data["from_username"] if is_incoming else connection_data["to_username"]
        
        # Status badge
        status = connection_data["status"]
        if status == "accepted":
            status_badge = ft.Container(
                content=ft.Text("Accepted", color=ft.Colors.WHITE, size=12),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                bgcolor=ft.Colors.GREEN,
                border_radius=15,
            )
        else:
            status_badge = ft.Container(
                content=ft.Text("Pending", color=ft.Colors.WHITE, size=12),
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                bgcolor=ft.Colors.AMBER,
                border_radius=15,
            )
        
        # Action buttons (only show for incoming pending requests)
        action_buttons = ft.Row([], spacing=5)
        if is_incoming and status == "requested":
            action_buttons.controls = [
                ft.IconButton(
                    icon=ft.Icons.CHECK,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Accept",
                    on_click=lambda e: self._accept_request(),
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=ft.Colors.RED,
                    tooltip="Reject",
                    on_click=lambda e: self._reject_request(),
                ),
            ]
        
        # Direction indicator
        direction = "← From" if is_incoming else "To →"
        
        self.content = ft.Row(
            [
                ft.Container(
                    content=ft.Text(direction, size=12, color=ft.Colors.ON_SURFACE),
                    expand=1,
                ),
                ft.Container(
                    content=ft.Text(other_user, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE),
                    expand=2,
                ),
                ft.Container(
                    content=ft.Text(connection_data["project_name"], color=ft.Colors.ON_SURFACE),
                    expand=2,
                ),
                ft.Container(
                    content=status_badge,
                    expand=1,
                ),
                ft.Container(
                    content=action_buttons,
                    expand=1,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        self.padding = 15
        self.border_radius = 10
        self.on_hover = self._on_hover
        self.animate = ft.Animation(150, ft.AnimationCurve.EASE)
    
    def _on_hover(self, e):
        if e.data == "true":
            self.bgcolor = ft.Colors.TERTIARY_CONTAINER
        else:
            self.bgcolor = None
        self.update()
    
    def _accept_request(self):
        """Accept the connection request"""
        try:
            server_patch(f"/requests/{self.connection_data['id']}", {"status": "accepted"})
            print(f"Accepted request from {self.connection_data['from_username']}")
            if self.on_action:
                self.on_action()
        except APIClientError as ex:
            print(f"Failed to accept request: {ex}")
    
    def _reject_request(self):
        """Reject the connection request (for now, just mark as rejected in UI)"""
        print(f"Rejected request from {self.connection_data['from_username']}")
        # In a real app, you'd have a DELETE endpoint or status="rejected"
        if self.on_action:
            self.on_action()


class ConnectionsView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        
        # Loading state
        self.loading_text = ft.Text("Loading connections...", color=ft.Colors.ON_SURFACE)
        
        # Container for cards
        self.cards_container = ft.Column([], spacing=5, scroll=ft.ScrollMode.AUTO)
        
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Connections", size=32, font_family="Roboto-Bold", color=ft.Colors.ON_SURFACE),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Refresh",
                            on_click=lambda e: self._load_connections(),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Card(
                    content=ft.Container(
                        content=self.cards_container,
                        padding=20,
                    ),
                    expand=True,
                ),
            ],
        )
    
    def did_mount(self):
        """Called after the view is added to the page"""
        self._load_connections()
    
    def _load_connections(self):
        """Load connections from API"""
        self.cards_container.controls = [self.loading_text]
        self.update()
        
        try:
            username = self.page.session_username
            connections = server_get(f"/requests?user={username}")
            
            if not connections:
                self.cards_container.controls = [
                    ft.Text("No connections yet. Click 'New' to create one!", color=ft.Colors.ON_SURFACE)
                ]
            else:
                # Create cards
                cards = []
                for conn in connections:
                    cards.append(ConnectionCard(self.page, conn, on_action=self._load_connections))
                    cards.append(ft.Divider(color=ft.Colors.OUTLINE, height=1))
                
                self.cards_container.controls = cards
            
            self.update()
            
        except APIClientError as ex:
            self.cards_container.controls = [
                ft.Text(f"Failed to load connections: {ex}", color="error")
            ]
            self.update()