# settings.py
import flet as ft


def settings_page(page: ft.Page):
    # Create a container for the settings
    settings_container = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLACK,
        content=ft.Column(
            [
                ft.Container(height=20),
                ft.Row(
                    [
                        ft.Text("Settings", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(height=20, color=ft.Colors.GREY_800),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Coming soon...", size=20, color=ft.Colors.GREY_400),
                            ft.Text("Settings will be available in future updates.", size=14, color=ft.Colors.GREY_500),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Back",
                    on_click=lambda e: page.go("/"),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_800,
                        color=ft.Colors.WHITE,
                        padding=ft.Padding(30, 15, 30, 15),
                    ),
                    width=150,
                ),
                ft.Container(height=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
    )

    # Add background
    background = ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src="assets/images/background.gif",
            fit=ft.BoxFit.COVER,
        ),
        content=ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            content=settings_container,
        ),
    )

    return background