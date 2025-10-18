import flet as ft

from .ThemeModeButton import ThemeModeButton
from .SideBar import SideMenuButton
from .NewButton import NewButton
from .AccountButton import AccountButton


class SearchBar(ft.TextField):
    def __init__(self):
        super().__init__()
        self.width = 200
        self.height = 40
        self.hint_text = "Search here..."
        self.border_radius = 10
        self.content_padding = 10
        self.prefix_icon = ft.Icons.SEARCH
        self.border_color = ft.Colors.OUTLINE


class TopBar(ft.Container):
    def __init__(self, page, sidebar_ref):
        super().__init__()
        self.page: ft.Page = page

        self.content = ft.Row(
            [
                ft.Row(
                    [
                        SideMenuButton(sidebar_ref),
                        ft.Row([SearchBar()], spacing=15),
                    ]
                ),
                ft.Row([
                    NewButton(page), 
                    AccountButton(page, {
                        "name": "Bustin Jeiber", 
                        "email": "lifeisacoconut@email.me", 
                        "image": "https://imgs.search.brave.com/CEhgYO16zqblD7dBsDBibAFC9fSWaZ5mkYUm6aOoeB0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLnBp/bmltZy5jb20vb3Jp/Z2luYWxzLzdmLzM4/L2Y1LzdmMzhmNTUz/MjZhNGEzMDkyNmU4/YTY1NjQ2YjczYzdm/LmpwZw"
                    }),
                    ThemeModeButton(page)
                ], spacing=10)
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        self.height = 60
        self.bgcolor = ft.Colors.SURFACE
        self.padding = ft.padding.symmetric(horizontal=20)
        # CRITICAL: Allow menu to overflow outside TopBar bounds
        self.clip_behavior = ft.ClipBehavior.NONE