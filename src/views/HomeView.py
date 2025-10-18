import flet as ft
from components.OverviewCards import OverviewCard
from api_client import server_get, APIClientError


class HomeView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        
        # Loading indicator
        self.loading_text = ft.Text("Loading projects...", color=ft.Colors.ON_SURFACE)
        
        # Container for project cards
        self.projects_row = ft.Row([], scroll=ft.ScrollMode.AUTO)
        
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Overview", size=32, font_family="Roboto-Bold", color=ft.Colors.ON_SURFACE),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Refresh",
                            on_click=lambda e: self._load_projects(),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.projects_row,
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    
    def did_mount(self):
        """Called after the view is added to the page"""
        self._load_projects()
    
    def _load_projects(self):
        """Load projects from API"""
        self.projects_row.controls = [self.loading_text]
        if self.page:  # Only update if added to page
            self.update()
        
        # Check if user is logged in
        if not hasattr(self.page, 'session_username') or not self.page.session_username:
            self.projects_row.controls = [
                ft.Container(
                    content=ft.Text("Please log in to view projects", color=ft.Colors.ON_SURFACE),
                    padding=50,
                )
            ]
            if self.page:
                self.update()
            return
        
        try:
            username = self.page.session_username
            projects = server_get(f"/projects?user={username}")
            
            if not projects:
                self.projects_row.controls = [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.FOLDER_OPEN, size=64, color=ft.Colors.ON_SURFACE),
                                ft.Text("No projects yet", size=20, color=ft.Colors.ON_SURFACE),
                                ft.Text(
                                    "Create a connection and start collaborating!",
                                    size=14,
                                    color=ft.Colors.ON_SURFACE,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        padding=50,
                    )
                ]
            else:
                # Create cards for each project
                cards = []
                for project in projects:
                    # Use placeholder images for now
                    images = [
                        "https://images.unsplash.com/photo-1557821552-17105176677c",
                        "https://images.unsplash.com/photo-1563986768609-322da13575f3",
                        "https://images.unsplash.com/photo-1677442136019-21780ecad995",
                        "https://images.unsplash.com/photo-1460925895917-afdab827c52f",
                    ]
                    
                    card = OverviewCard(
                        self.page,
                        title=project["title"],
                        subtitle=project.get("description", "No description"),
                        image=images[len(cards) % len(images)],
                        connection_data={"name": "Connection", "role": project.get("status", "in_progress")},
                        on_open=lambda e, p=project: self._open_project(p),
                    )
                    cards.append(card)
                
                self.projects_row.controls = cards
            
            if self.page:  # Only update if added to page
                self.update()
            
        except APIClientError as ex:
            self.projects_row.controls = [
                ft.Text(f"Failed to load projects: {ex}", color="error")
            ]
            if self.page:  # Only update if added to page
                self.update()
    
    def _open_project(self, project):
        """Open project detail view"""
        print(f"Opening project: {project['title']}")
        # TODO: Navigate to project detail view
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Project view coming soon: {project['title']}"),
        )
        self.page.snack_bar.open = True
        self.page.update()