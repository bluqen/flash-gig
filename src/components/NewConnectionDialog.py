import flet as ft
from api_client import server_post, APIClientError


class NewConnectionOverlay(ft.Container):
    """Overlay for creating a new connection request - same pattern as LoginOverlay"""
    
    def __init__(self, page: ft.Page, on_success=None):
        super().__init__()
        self.page = page
        self.on_success = on_success
        
        # Input fields
        self.username_field = ft.TextField(
            label="Their Username",
            hint_text="Enter username",
            width=400,
        )
        
        self.project_field = ft.TextField(
            label="Project Name",
            hint_text="What are you working on?",
            width=400,
        )
        
        self.error_text = ft.Text("", color="error", visible=False)
        
        # Buttons
        self.send_button = ft.ElevatedButton(
            "Send Request",
            icon=ft.Icons.SEND,
            on_click=self._send_request,
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
                        "New Connection Request",
                        color="blue",
                        font_family="Roboto-Bold",
                        size=24
                    ),
                    ft.Divider(height=20),
                    ft.Text(
                        "Connect with a client or freelancer",
                        size=14,
                        color=ft.Colors.ON_SURFACE_VARIANT
                    ),
                    self.username_field,
                    self.project_field,
                    self.error_text,
                    ft.Row(
                        [
                            self.cancel_button,
                            self.send_button,
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
    
    def hide(self):
        """Hide the overlay"""
        if self in self.page.overlay:
            self.page.overlay.remove(self)
            self.page.update()
    
    def _send_request(self, e):
        # Clear error
        self.error_text.visible = False
        self.update()
        
        # Check if logged in
        if not hasattr(self.page, 'session_username') or not self.page.session_username:
            self.error_text.value = "Please log in first!"
            self.error_text.visible = True
            self.update()
            return
        
        # Get values
        to_username = self.username_field.value.strip() if self.username_field.value else ""
        project_name = self.project_field.value.strip() if self.project_field.value else ""
        from_username = self.page.session_username
        
        # Validate
        if not to_username or not project_name:
            self.error_text.value = "Please fill in all fields"
            self.error_text.visible = True
            self.update()
            return
        
        if to_username == from_username:
            self.error_text.value = "You cannot connect with yourself"
            self.error_text.visible = True
            self.update()
            return
        
        # Disable button
        self.send_button.disabled = True
        self.send_button.text = "Sending..."
        self.update()
        
        # Send request
        try:
            result = server_post("/requests", {
                "from_username": from_username,
                "to_username": to_username,
                "project_name": project_name,
            })
            
            print(f"Connection request sent: {result}")
            
            # Close overlay and call success callback
            self.hide()
            if self.on_success:
                self.on_success()
                
        except APIClientError as ex:
            error_str = str(ex).lower()
            if "404" in error_str:
                self.error_text.value = "User not found. Check the username."
            elif "400" in error_str:
                self.error_text.value = "Invalid request. Please check your inputs."
            else:
                self.error_text.value = f"Failed to send request: {ex}"
            
            self.error_text.visible = True
            self.send_button.disabled = False
            self.send_button.text = "Send Request"
            self.update()


def show_new_connection_dialog(page: ft.Page, on_success=None):
    """Helper function to show the overlay"""
    overlay = NewConnectionOverlay(page, on_success)
    overlay.display()