import flet as ft
from api_client import server_get, server_post, server_patch, APIClientError


class CommentCard(ft.Container):
    """Single comment display"""
    
    def __init__(self, comment_data: dict):
        super().__init__()
        
        timestamp_text = ""
        if comment_data.get("timestamp"):
            timestamp_text = f" @ {comment_data['timestamp']}s"
        
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            comment_data["username"],
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.PRIMARY,
                        ),
                        ft.Text(timestamp_text, size=12, color=ft.Colors.ON_SURFACE),
                    ],
                    spacing=5,
                ),
                ft.Text(comment_data["text"], color=ft.Colors.ON_SURFACE),
                ft.Text(
                    comment_data["created_at"][:10],
                    size=11,
                    color=ft.Colors.ON_SURFACE,
                    opacity=0.6,
                ),
            ],
            spacing=5,
        )
        
        self.padding = 15
        self.border_radius = 8
        self.bgcolor = "surfacevariant"
        self.border = ft.border.all(1, ft.Colors.OUTLINE)


class ProjectView(ft.Container):
    """Project detail and collaboration workspace"""
    
    def __init__(self, page: ft.Page, project_id: str):
        super().__init__()
        self.page = page
        self.project_id = project_id
        self.expand = True
        self.project_data = None
        
        # Comment input
        self.comment_field = ft.TextField(
            hint_text="Add a comment...",
            multiline=True,
            min_lines=2,
            max_lines=4,
            expand=True,
        )
        
        self.timestamp_field = ft.TextField(
            hint_text="Timestamp (optional)",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        self.send_button = ft.IconButton(
            icon=ft.Icons.SEND,
            tooltip="Send comment",
            on_click=self._send_comment,
        )
        
        # Comments container
        self.comments_container = ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        # Status dropdown
        self.status_dropdown = ft.Dropdown(
            label="Project Status",
            width=200,
            options=[
                ft.dropdown.Option("in_progress", "In Progress"),
                ft.dropdown.Option("review", "Review"),
                ft.dropdown.Option("changes_requested", "Changes Requested"),
                ft.dropdown.Option("approved", "Approved"),
                ft.dropdown.Option("completed", "Completed"),
            ],
            on_change=self._update_status,
        )
        
        # Main content
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            tooltip="Back to overview",
                            on_click=self._go_back,
                        ),
                        ft.Text("Loading...", size=24, font_family="Roboto-Bold", color=ft.Colors.ON_SURFACE),
                    ],
                ),
                ft.Divider(),
                # Project info section
                ft.Container(
                    content=ft.Column([], spacing=10),
                    padding=20,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
        
        # Load project data
        self._load_project()
    
    def _load_project(self):
        """Load project details"""
        try:
            self.project_data = server_get(f"/projects/{self.project_id}")
            
            # Update title
            self.content.controls[0].controls[1].value = self.project_data["title"]
            
            # Set status dropdown
            self.status_dropdown.value = self.project_data.get("status", "in_progress")
            
            # Build project info section
            info_section = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Status:", weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE),
                                self.status_dropdown,
                            ],
                            spacing=10,
                        ),
                        ft.Text(
                            "Description:",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ON_SURFACE,
                        ),
                        ft.Text(
                            self.project_data.get("description", "No description"),
                            color=ft.Colors.ON_SURFACE,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
                bgcolor="surfacevariant",
                border_radius=12,
            )
            
            # Comments section
            comments_section = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Comments", size=20, font_family="Roboto-Bold", color=ft.Colors.ON_SURFACE),
                        self.comments_container,
                        ft.Divider(),
                        ft.Row(
                            [
                                self.comment_field,
                                self.timestamp_field,
                                self.send_button,
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
            
            # Update main content
            self.content.controls[2] = ft.Column(
                [info_section, comments_section],
                spacing=20,
            )
            
            # Load comments
            self._load_comments()
            
            self.update()
            
        except APIClientError as ex:
            print(f"Failed to load project: {ex}")
            self.content.controls[0].controls[1].value = "Error loading project"
            self.update()
    
    def _load_comments(self):
        """Load project comments"""
        try:
            comments = server_get(f"/comments?project_id={self.project_id}")
            
            if not comments:
                self.comments_container.controls = [
                    ft.Text("No comments yet. Be the first to comment!", color=ft.Colors.ON_SURFACE)
                ]
            else:
                self.comments_container.controls = [
                    CommentCard(comment) for comment in comments
                ]
            
            self.update()
            
        except APIClientError as ex:
            print(f"Failed to load comments: {ex}")
    
    def _send_comment(self, e):
        """Send a new comment"""
        text = self.comment_field.value.strip()
        if not text:
            return
        
        # Disable button
        self.send_button.disabled = True
        self.update()
        
        try:
            timestamp = None
            if self.timestamp_field.value:
                try:
                    timestamp = int(self.timestamp_field.value)
                except ValueError:
                    pass
            
            server_post("/comments", {
                "project_id": self.project_id,
                "username": self.page.session_username,
                "text": text,
                "timestamp": timestamp,
            })
            
            # Clear fields
            self.comment_field.value = ""
            self.timestamp_field.value = ""
            
            # Reload comments
            self._load_comments()
            
        except APIClientError as ex:
            print(f"Failed to send comment: {ex}")
        
        finally:
            self.send_button.disabled = False
            self.update()
    
    def _update_status(self, e):
        """Update project status"""
        try:
            server_patch(f"/projects/{self.project_id}", {
                "status": self.status_dropdown.value
            })
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Status updated!"),
                bgcolor=ft.Colors.GREEN,
            )
            self.page.snack_bar.open = True
            self.page.update()
            
        except APIClientError as ex:
            print(f"Failed to update status: {ex}")
    
    def _go_back(self, e):
        """Navigate back to home"""
        # This is a placeholder - you'll implement proper routing
        print("Going back to overview")
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Back navigation - implement routing!"),
        )
        self.page.snack_bar.open = True
        self.page.update()