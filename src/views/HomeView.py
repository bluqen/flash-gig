import flet as ft

class HomeView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        
        self.content = ft.Column(
            [
                ft.Text("Home View", size=32, font_family="Roboto-Bold"),
                ft.Text("Welcome to Flash Gig!", size=16),
                ft.Container(height=20),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Dashboard", font_family="Roboto-Bold"),
                            ft.Text("Your recent activity will appear here", font_family="Roboto"),
                        ]),
                        padding=20,
                    )
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )