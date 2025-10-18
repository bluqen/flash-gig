import flet as ft


class OverviewCard(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        title: str,
        subtitle: str,
        image: str,
        connection_data: dict = {},
        on_open=None,
        width: int = 350,
    ):
        super().__init__()
        self.page = page
        self.on_open_handler = on_open
        self.width = width

        # Image at the top - fills full width
        card_image = ft.Container(
            content=ft.Image(
                src=image, fit=ft.ImageFit.COVER, width=float("inf"), height=200
            ),
            height=200,
            border_radius=ft.border_radius.only(top_left=12, top_right=12),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        # Title, subtitle and link section
        text_section = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        title,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE,  # Semantic color
                    ),
                    ft.Text(
                        subtitle,
                        size=14,
                        opacity=0.7,
                        color=ft.Colors.ON_SURFACE,  # Semantic color
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                padding=ft.padding.only(bottom=2),
                                border=ft.border.only(
                                    bottom=ft.border.BorderSide(1, ft.Colors.ON_SURFACE)
                                ),
                                content=ft.Text(
                                    connection_data.get("name", ""), 
                                    size=12,
                                    color=ft.Colors.ON_SURFACE,
                                ),
                            ),
                            ft.Text("•", color=ft.Colors.ON_SURFACE),
                            ft.Text(
                                connection_data.get("role", ""), 
                                size=12,
                                color=ft.Colors.ON_SURFACE,
                            ),
                        ], 
                        spacing=15
                    ),
                ],
                spacing=8,
                tight=True,
            ),
            padding=ft.padding.only(left=20, right=20, top=16, bottom=12),
        )

        # Open button
        open_button = ft.Container(
            content=ft.ElevatedButton(
                "Open",
                icon=ft.Icons.OPEN_IN_NEW,
                on_click=self._handle_open,
                style=ft.ButtonStyle(
                    bgcolor={
                        ft.ControlState.DEFAULT: ft.Colors.SECONDARY,
                        ft.ControlState.HOVERED: ft.Colors.TERTIARY_CONTAINER,
                        ft.ControlState.PRESSED: ft.Colors.TERTIARY,
                    },
                    color=ft.Colors.ON_SURFACE,
                ),
            ),
            padding=ft.padding.only(left=20, right=20, bottom=16),
        )

        # Set container properties
        self.content = ft.Column(
            [
                card_image,
                text_section,
                open_button,
            ],
            spacing=0,
            tight=True,
        )

        self.bgcolor = "surfacevariant"  # Semantic color
        self.border_radius = 12
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        )

        # Hover animation
        self.animate_scale = ft.Animation(200, ft.AnimationCurve.EASE)
        self.scale = 1.0

    def _handle_open(self, e):
        """Handle open button click"""
        if self.on_open_handler:
            self.on_open_handler(e)