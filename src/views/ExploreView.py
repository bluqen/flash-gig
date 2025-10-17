import flet as ft

class ExploreView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        
        self.content = ft.Column(
            [
                ft.Text("Explore View", size=32, font_family="Roboto-Bold"),
                ft.Text("Discover new opportunities", size=16),
                ft.Container(height=20),
                ft.GridView(
                    expand=True,
                    runs_count=3,
                    spacing=10,
                    run_spacing=10,
                    child_aspect_ratio=1.5,
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                content=ft.Text(f"Item {i+1}"),
                                padding=20,
                                alignment=ft.alignment.center,
                            )
                        )
                        for i in range(9)
                    ],
                ),
            ],
        )