import flet as ft
from api_client import server_post, server_get, APIClientError


class CreateProjectOverlay(ft.Container):
    """Overlay for creating a project - same pattern as LoginOverlay"""
    
    def __init__(self, page: ft.Page, on_success=None):
        super().__init__()
        self.page = page
        self.on_success = on_success
        
        # Dropdown for selecting connection
        self.connection_dropdown = ft.Dropdown(
            label="Select Connection",
            hint_text="Choose an accepted connection",
            width=400,
        )
        
        # Input fields
        self.title_field = ft.TextField(
            label="Project Title",
            hint_text="Enter project name",
            width=400,
        )
        
        self.description_field = ft.TextField(
            label="Description",
            hint_text="What's this project about?",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=400,
        )
        
        self.error_text = ft.Text("", color="error", visible=False)
        self.loading_text = ft.Text("Loading connections...", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        
        # Buttons
        self.create_button = ft.ElevatedButton(
            "Create Project",
            icon=ft.Icons.ADD,
            on_click=self._create_project,
        )
        
        self.cancel_button = ft.TextButton(
            "Cancel",
            on_click=lambda e: self.hide(),
        )
        
        # Dialog card - same style as LoginOverlay
        dialog_card = ft.Container(
            width=480,
            height=480,
            bgcolor="surfacevariant",
            border_radius=12,
            padding=ft.padding.symmetric(vertical=30, horizontal=40),
            border=ft.border.all(1, "outline"),
            content=ft.Column(
                [
                    ft.Text(
                        "Create New Project",
                        color="blue",
                        font_family="Roboto-Bold",
                        size=24
                    ),
                    ft.Divider(height=20),
                    ft.Text(
                        "Create a project from an accepted connection",
                        size=14,
                        color=ft.Colors.ON_SURFACE_VARIANT
                    ),
                    self.loading_text,
                    self.connection_dropdown,
                    self.title_field,
                    self.description_field,
                    self.error_text,
                    ft.Row(
                        [
                            self.cancel_button,
                            self.create_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10,
                    ),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        
        # Container properties - same as LoginOverlay
        self.content = dialog_card
        self.bgcolor = ft.Colors.with_opacity(0.5, "black")
        self.expand = True
        self.alignment = ft.alignment.center
        self.animate_opacity = ft.Animation(200, ft.AnimationCurve.EASE)
    
    def display(self):
        """Show the overlay"""
        self.page.overlay.append(self)
        self.page.update()
        # Load connections after showing
        self._load_connections()
    
    def hide(self):
        """Hide the overlay"""
        if self in self.page.overlay:
            self.page.overlay.remove(self)
            self.page.update()
    
    def _load_connections(self):
        """Load accepted connections"""
        # Check if logged in
        if not hasattr(self.page, 'session_username') or not self.page.session_username:
            self.loading_text.visible = False
            self.error_text.value = "Please log in first!"
            self.error_text.visible = True
            self.create_button.disabled = True
            self.update()
            return
        
        try:
            username = self.page.session_username
            connections = server_get(f"/requests?user={username}")
            
            # Filter only accepted connections
            accepted = [c for c in connections if c.get("status") == "accepted"]
            
            self.loading_text.visible = False
            
            if not accepted:
                self.error_text.value = "No accepted connections. Accept a connection first!"
                self.error_text.visible = True
                self.create_button.disabled = True
            else:
                # Create dropdown options
                self.connection_dropdown.options = [
                    ft.dropdown.Option(
                        key=c["id"],
                        text=f"{c['project_name']} - with {c['from_username'] if c['to_username'] == username else c['to_username']}"
                    )
                    for c in accepted
                ]
            
            self.update()
            
        except APIClientError as ex:
            self.loading_text.visible = False
            self.error_text.value = f"Failed to load connections: {ex}"
            self.error_text.visible = True
            self.update()
    
    def _create_project(self, e):
        # Clear error
        self.error_text.visible = False
        self.update()
        
        # Get values
        request_id = self.connection_dropdown.value
        title = self.title_field.value.strip() if self.title_field.value else ""
        description = self.description_field.value.strip() if self.description_field.value else ""
        
        # Validate
        if not request_id:
            self.error_text.value = "Please select a connection"
            self.error_text.visible = True
            self.update()
            return
        
        if not title:
            self.error_text.value = "Please enter a project title"
            self.error_text.visible = True
            self.update()
            return
        
        # Disable button
        self.create_button.disabled = True
        self.create_button.text = "Creating..."
        self.update()
        
        # Create project
        try:
            result = server_post("/projects", {
                "request_id": request_id,
                "title": title,
                "description": description,
            })
            
            print(f"Project created: {result}")
            
            # Close overlay and call success callback
            self.hide()
            if self.on_success:
                self.on_success()
                
        except APIClientError as ex:
            self.error_text.value = f"Failed to create project: {ex}"
            self.error_text.visible = True
            self.create_button.disabled = False
            self.create_button.text = "Create Project"
            self.update()


def show_create_project_dialog(page: ft.Page, on_success=None):
    """Helper function to show the overlay"""
    overlay = CreateProjectOverlay(page, on_success)
    overlay.display()