import flet as ft


class GradientText(ft.Container):
    def __init__(
        self,
        text: str,
        colors: list[str] = [ft.Colors.PINK, ft.Colors.PURPLE],
        size: int = 24,
        font="Roboto-Bold",
        gradient_direction: str = "horizontal",  # "horizontal" or "vertical"
    ):
        super().__init__()

        if gradient_direction == "horizontal":
            begin = ft.alignment.center_left
            end = ft.alignment.center_right
        else:
            begin = ft.alignment.top_center
            end = ft.alignment.bottom_center

        self.content = ft.ShaderMask(
            shader=ft.LinearGradient(
                begin=begin,
                end=end,
                colors=colors,
            ),
            blend_mode=ft.BlendMode.SRC_IN,
            content=ft.Text(
                text,
                size=size,
                font_family=font,
                color=ft.Colors.WHITE,  # required for mask blending
            ),
        )
