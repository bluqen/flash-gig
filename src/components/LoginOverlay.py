import flet as ft
from api_client import server_post, server_get, APIClientError

from components.ThemeModeButton import ThemeModeButton
from components.GradientText import GradientText


class LoginOverlay(ft.Container):
    def __init__(self, page: ft.Page, on_success=None):
        super().__init__()
        self.page = page
        self.on_success = on_success
        
        # Input fields with modern styling
        self.username = ft.TextField(
            "",
            label="Username",
            width=380,
            on_change=self.show_username_error,
            border_radius=10,
            filled=True,
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            height=50,
        )
        self.password = ft.TextField(
            "",
            label="Password",
            password=True,
            can_reveal_password=True,
            width=380,
            border_radius=10,
            filled=True,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            height=50,
        )
        
        self.username_error_text = ft.Text("", color="error", visible=False, size=11)
        self.error_text = ft.Text("", color="error", visible=False, size=11)
        
        # Modern login button with gradient effect
        self.login_button = ft.Container(
            content=ft.Text(
                "Login",
                size=15,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            width=380,
            height=45,
            border_radius=10,
            bgcolor=ft.Colors.BLUE,
            alignment=ft.alignment.center,
            ink=True,
            on_click=self.login,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        # Divider with text
        self.divider_row = ft.Row(
            [
                ft.Container(
                    content=ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)),
                    expand=True,
                ),
                ft.Text("OR", size=11, color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)),
                ft.Container(
                    content=ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)),
                    expand=True,
                ),
            ],
            spacing=10,
        )
        
        # Social login buttons
        self.google_button = ft.Container(
            content=ft.Row(
                [
                    ft.Image(
                        src="https://cdn.cdnlogo.com/logos/g/35/google-icon.svg",
                        width=18,
                        height=18,
                    ),
                    ft.Text("Continue with Google", size=13, weight=ft.FontWeight.W_500),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            width=380,
            height=42,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)),
            ink=True,
            on_click=self.google_login,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        # Signup text link
        self.signup_text = ft.Row(
            [
                ft.Text("Don't have an account?", size=12, color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)),
                ft.TextButton(
                    "Sign up",
                    on_click=self.show_signup_overlay,
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLUE,
                        overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                        padding=5,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )

        # Animated login card - made responsive with max constraints
        self.login_card = ft.Container(
            width=460,
            height=580,
            border_radius=16,
            blur=10,
            padding=ft.padding.symmetric(vertical=30, horizontal=40),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            shadow=ft.BoxShadow(
                blur_radius=40,
                spread_radius=5,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE),
                offset=ft.Offset(0, 10),
            ),
            animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            scale=ft.Scale(0.9),
            opacity=0,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LOGIN, color=ft.Colors.BLUE, size=24),
                            ft.Text(
                                "Welcome Back",
                                color=ft.Colors.BLUE,
                                font_family="Roboto-Bold",
                                size=24,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    ft.Text(
                        "Login to continue to Flash Gig",
                        size=12,
                        color=ft.Colors.with_opacity(0.6, ft.Colors.ON_SURFACE),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    self.username,
                    self.username_error_text,
                    self.password,
                    ft.Container(height=2),
                    ft.Row(
                        [
                            ft.Checkbox(
                                label="Remember me",
                                value=False,
                                scale=0.85,
                            ),
                            ft.TextButton(
                                "Forgot password?",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.BLUE,
                                    overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                                    padding=5,
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        width=380,
                    ),
                    ft.Container(height=5),
                    self.login_button,
                    self.error_text,
                    ft.Container(height=10),
                    self.divider_row,
                    ft.Container(height=5),
                    self.google_button,
                    ft.Container(height=8),
                    self.signup_text,
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
        )
        
        self.bgcolor = "surfacevariant"
        self.expand = True
        self.alignment = ft.alignment.center
        self.image = ft.DecorationImage(
            "login_background.png",
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.NO_REPEAT,
        )

        # Wrap card in scrollable container for small screens
        self.content = ft.Container(
            content=ft.Column(
                [
                    GradientText(
                        "Flash Gig",
                        ["blue", "bluegrey100"],
                        alignment=ft.alignment.center,
                        size=48,
                        font="Funnel-Bold",
                    ),
                    self.login_card,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
        )

    def display(self):
        self.page.overlay.append(self)
        self.page.update()
        
        # Small delay to ensure element is rendered before animating
        import threading
        def trigger_animation():
            import time
            time.sleep(0.05)
            self.login_card.scale = ft.Scale(1.0)
            self.login_card.opacity = 1
            self.login_card.update()
        
        threading.Thread(target=trigger_animation, daemon=True).start()

    def hide(self):
        # Animate out before hiding
        self.login_card.scale = ft.Scale(0.9)
        self.login_card.opacity = 0
        self.update()
        
        # Remove from overlay after animation completes
        import threading
        def remove_overlay():
            import time
            time.sleep(0.35)
            if self in self.page.overlay:
                self.page.overlay.remove(self)
                self.page.update()
        
        threading.Thread(target=remove_overlay, daemon=True).start()

    def google_login(self, e):
        # Placeholder for Google OAuth integration
        self.show_error("Google login coming soon!")

    def login(self, e):
        # Clear previous errors
        self.error_text.visible = False
        self.update()

        # Update button state
        self.login_button.bgcolor = ft.Colors.BLUE_GREY
        self.login_button.content = ft.Row(
            [
                ft.ProgressRing(width=18, height=18, color=ft.Colors.WHITE, stroke_width=2.5),
                ft.Text("Logging in...", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )
        self.login_button.update()

        username = self.username.value.strip()
        password = self.password.value

        # 1. Client-side validation
        if not username:
            self.show_username_error(None)
            return

        if not password:
            self.show_error("Password cannot be empty.")
            return

        # 2. Server-side validation and login
        try:
            server_get("/health")
            print("Server is online. Attempting to log in...")

            user_data = server_post(
                "/login", {"username": username, "password": password}
            )
            self.page.session_username = user_data.get("username")
            print(f"Login successful for user: {user_data.get('username')}")
            self.hide()

            if self.on_success:
                self.on_success()

        except APIClientError as ex:
            error_str = str(ex).lower()
            if "401" in error_str:
                self.show_error("Incorrect username or password.")
            elif "400" in error_str:
                self.show_error("Invalid login credentials.")
            elif "404" in error_str:
                self.show_error("User not found.")
            else:
                self.show_error(
                    "Cannot connect to the server. Please check your connection."
                )

    def show_username_error(self, e):
        if self.username.value == "":
            self.username_error_text.value = "Username cannot be empty."
            self.username_error_text.visible = True
            self.reset_button()
            self.update()
        else:
            self.username_error_text.visible = False
            self.update()

    def show_error(self, message: str):
        self.error_text.value = message
        self.error_text.visible = True
        self.reset_button()
        self.update()

    def reset_button(self):
        self.login_button.bgcolor = ft.Colors.BLUE
        self.login_button.content = ft.Text(
            "Login",
            size=15,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        self.login_button.update()

    def show_signup_overlay(self, e):
        signup_overlay = SignUpOverlay(self.page)
        signup_overlay.display()
        self.hide()


def show_login_overlay(page: ft.Page, on_success=None):
    login_overlay = LoginOverlay(page, on_success=on_success)
    login_overlay.display()


class SignUpOverlay(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
        # Modern input fields
        self.username = ft.TextField(
            "",
            label="Username",
            width=380,
            border_radius=10,
            filled=True,
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            height=50,
        )
        self.password = ft.TextField(
            "",
            label="Password",
            password=True,
            can_reveal_password=True,
            width=380,
            border_radius=10,
            filled=True,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            height=50,
        )
        self.confirm_password = ft.TextField(
            "",
            label="Confirm Password",
            password=True,
            can_reveal_password=True,
            width=380,
            border_radius=10,
            filled=True,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            height=50,
        )
        
        self.error_text = ft.Text("", color="error", visible=False, size=11)
        
        # Modern signup button
        self.signup_button = ft.Container(
            content=ft.Text(
                "Create Account",
                size=15,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            width=380,
            height=45,
            border_radius=10,
            bgcolor=ft.Colors.BLUE,
            alignment=ft.alignment.center,
            ink=True,
            on_click=self.signup,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        
        # Divider with text
        self.divider_row = ft.Row(
            [
                ft.Container(
                    content=ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)),
                    expand=True,
                ),
                ft.Text("OR", size=11, color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)),
                ft.Container(
                    content=ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)),
                    expand=True,
                ),
            ],
            spacing=10,
        )
        
        # Google signup button
        self.google_button = ft.Container(
            content=ft.Row(
                [
                    ft.Image(
                        src="https://cdn.cdnlogo.com/logos/g/35/google-icon.svg",
                        width=18,
                        height=18,
                    ),
                    ft.Text("Continue with Google", size=13, weight=ft.FontWeight.W_500),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            width=380,
            height=42,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.ON_SURFACE)),
            ink=True,
            on_click=self.google_signup,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

        # Login text link
        self.login_text = ft.Row(
            [
                ft.Text("Already have an account?", size=12, color=ft.Colors.with_opacity(0.7, ft.Colors.ON_SURFACE)),
                ft.TextButton(
                    "Log in",
                    on_click=self.show_login_overlay,
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLUE,
                        overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                        padding=5,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )

        # Animated signup card
        self.signup_card = ft.Container(
            width=460,
            height=600,
            border_radius=16,
            blur=10,
            padding=ft.padding.symmetric(vertical=30, horizontal=40),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            shadow=ft.BoxShadow(
                blur_radius=40,
                spread_radius=5,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE),
                offset=ft.Offset(0, 10),
            ),
            animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            scale=ft.Scale(0.9),
            opacity=0,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON_ADD, color=ft.Colors.BLUE, size=24),
                            ft.Text(
                                "Create Account",
                                color=ft.Colors.BLUE,
                                font_family="Roboto-Bold",
                                size=24,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    ft.Text(
                        "Sign up to get started with Flash Gig",
                        size=12,
                        color=ft.Colors.with_opacity(0.6, ft.Colors.ON_SURFACE),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    self.username,
                    self.password,
                    self.confirm_password,
                    ft.Container(height=2),
                    ft.Row(
                        [
                            ft.Checkbox(
                                label="I agree to Terms & Conditions",
                                value=False,
                                scale=0.85,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        width=380,
                    ),
                    ft.Container(height=5),
                    self.signup_button,
                    self.error_text,
                    ft.Container(height=10),
                    self.divider_row,
                    ft.Container(height=5),
                    self.google_button,
                    ft.Container(height=8),
                    self.login_text,
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self.expand = True
        self.alignment = ft.alignment.center
        self.bgcolor = "surfacevariant"
        self.image = ft.DecorationImage(
            "login_background.png",
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.NO_REPEAT,
        )

        # Wrap card in scrollable container for small screens
        self.content = ft.Container(
            content=ft.Column(
                [
                    GradientText(
                        "Flash Gig",
                        ["blue", "bluegrey100"],
                        alignment=ft.alignment.center,
                        size=48,
                        font="Funnel-Bold",
                    ),
                    self.signup_card,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
        )

    def display(self):
        self.page.overlay.append(self)
        self.page.update()
        
        # Small delay to ensure element is rendered before animating
        import threading
        def trigger_animation():
            import time
            time.sleep(0.05)
            self.signup_card.scale = ft.Scale(1.0)
            self.signup_card.opacity = 1
            self.signup_card.update()
        
        threading.Thread(target=trigger_animation, daemon=True).start()

    def hide(self):
        # Animate out before hiding
        self.signup_card.scale = ft.Scale(0.9)
        self.signup_card.opacity = 0
        self.update()
        
        # Remove from overlay after animation completes
        import threading
        def remove_overlay():
            import time
            time.sleep(0.35)
            if self in self.page.overlay:
                self.page.overlay.remove(self)
                self.page.update()
        
        threading.Thread(target=remove_overlay, daemon=True).start()

    def google_signup(self, e):
        # Placeholder for Google OAuth integration
        self.show_error("Google signup coming soon!")

    def signup(self, e):
        # Clear previous errors
        self.error_text.visible = False
        self.update()

        # Update button state
        self.signup_button.bgcolor = ft.Colors.BLUE_GREY
        self.signup_button.content = ft.Row(
            [
                ft.ProgressRing(width=18, height=18, color=ft.Colors.WHITE, stroke_width=2.5),
                ft.Text("Creating...", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )
        self.signup_button.update()

        username = self.username.value.strip()
        password = self.password.value
        confirm_password = self.confirm_password.value

        # 1. Client-side validation
        if not username or not password:
            self.show_error("Username and password cannot be empty.")
            return
        if password != confirm_password:
            self.show_error("Passwords do not match.")
            return

        # Basic password strength check
        if len(password) < 6:
            self.show_error("Password must be at least 6 characters long.")
            return

        # 2. Server-side registration
        try:
            print(f"Sending registration request for user '{username}'...")
            user_data = server_post(
                "/register", {"username": username, "password": password}
            )

            if user_data:
                print(f"Registration successful for user: {user_data.get('username')}")
                self.hide()
                login_overlay = LoginOverlay(self.page)
                login_overlay.display()
            else:
                self.show_error("Received an empty response from the server.")

        except APIClientError as ex:
            error_str = str(ex).lower()
            if "400" in error_str:
                if "already" in error_str:
                    self.show_error("Username already taken. Please choose another.")
                else:
                    self.show_error("Invalid username or password.")
            else:
                self.show_error("Cannot connect to the server. Please try again later.")

    def show_error(self, message: str):
        self.error_text.value = message
        self.error_text.visible = True
        self.reset_button()
        self.update()

    def reset_button(self):
        self.signup_button.bgcolor = ft.Colors.BLUE
        self.signup_button.content = ft.Text(
            "Create Account",
            size=15,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        self.signup_button.update()

    def show_login_overlay(self, e):
        login_overlay = LoginOverlay(self.page)
        login_overlay.display()
        self.hide()