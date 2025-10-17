import flet as ft

class SettingsView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        
        self.content = ft.Column(
            [
                ft.Text("Settings View", size=32, font_family="Roboto-Bold"),
                ft.Text("Configure your preferences", size=16),
                ft.Container(height=20),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Appearance", font_family="Roboto-Bold"),
                            ft.Switch(label="Dark Mode", value=True),
                            ft.Divider(),
                            ft.Text("Notifications", font_family="Roboto-Bold"),
                            ft.Switch(label="Email Notifications", value=True),
                            ft.Switch(label="Push Notifications", value=False),
                        ]),
                        padding=20,
                    )
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )