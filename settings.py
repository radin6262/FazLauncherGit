import flet as ft


def settings_page(page: ft.Page):
    async def go_back(e):
        await page.push_route("/")

    return ft.View(
        route="/settings",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                content=ft.Column(
                    [
                        ft.Text(
                            "Settings",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),

                        ft.Divider(
                            height=20,
                            color=ft.Colors.GREY_800,
                        ),

                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Coming soon...",
                                        size=20,
                                        color=ft.Colors.GREY_400,
                                    ),
                                    ft.Text(
                                        "Settings will be available in future updates.",
                                        size=14,
                                        color=ft.Colors.GREY_500,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            alignment=ft.Alignment(0, 0),
                            expand=True,
                        ),

                        ft.ElevatedButton(
                            "Back",
                            on_click=go_back,
                            width=150,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    expand=True,
                ),
            )
        ],
    )