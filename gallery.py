import json
from pathlib import Path
import flet as ft

# Target directory: C:\Users\<Username>\Downloads\FNAF_Launcher
CONFIG_DIR = Path.home() / "Downloads" / "FNAF_Launcher"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "launcher_background_set": "",
        "launcher_background_option": "",
        "launcher_background": "",
    }


def gallery_page(page: ft.Page):
    IMAGE_SETS = {
        "FNAF 1": [
            "gallery/BareEndoClean.png",
            "gallery/Freddy_Fazbear (3).png",
            "gallery/Bonnie_Rabbit (1).png",
            "gallery/Chica (1).png",
            "gallery/foxy.png",
            "gallery/goldenfreddy.png",
        ],
        "FNAF 2": [
            "gallery/fnaf2endo.png",
            "gallery/Toy_freddy.png",
            "gallery/Toy_bonnie.png",
            "gallery/Toy_Chica_OfficialRender.png",
            "gallery/Mangle.png",
            "gallery/FNAF2BB.png",
            "gallery/JJ_UCN.png",
            "gallery/Withered_Chica (1).png",
            "gallery/Withered_foxy.png",
            "gallery/WitheredBonnie_Office.png",
            "gallery/OldFreddyTransparent.png",
            "gallery/FNAF2SlumpedGoldenFreddy (1).png",
        ],
        "FNAF 3": [
            "gallery/Extra_Springtrap_1 (1).png",
            "gallery/FNAF3ShadowFreddy.png",
            "gallery/Phantom_Fred_UCN.png",
            "gallery/PhantomFoxyOffice.png",
            "gallery/PhantomMangle_Infobox.png",
            "gallery/Extra_BB.png",
            "gallery/Extra_Chica.png",
            "gallery/Extra_Puppet.png",
        ],
        "FNAF 4": [
            "gallery/Nightmare_Bonnie.png",
            "gallery/Nightmare_Chica.png",
            "gallery/Nightmare_Foxy.png",
            "gallery/Nightmare_Freddy.png",
            "gallery/NightmareBB.png",
            "gallery/NightmareMangle.png",
            "gallery/Nightmareextra (1).png",
            "gallery/Nightmarefredbearextra.png",
            "gallery/FNaF4_-_Extra_%28Nightmarionne%29.png",
            "gallery/Plushtrap_UCN.png",
        ],
        "Halloween": [
            "gallery/BonnieJACK-O.png",
            "gallery/Jack-O-Chica.png",
        ],
        "Shadows": [
            "gallery/ShadowFreddy.png",
            "gallery/ShadowBonnie_UCN.png",
        ],
    }

    # Tracking selected state
    default_set = list(IMAGE_SETS.keys())[0]
    selected_set = default_set
    current_index = 0

    def go_back(e):
        page.go("/")

    # Preview image control
    preview_img = ft.Image(
        width=200,
        src=IMAGE_SETS[selected_set][current_index],
        fit=ft.BoxFit.CONTAIN,
        expand=True,
    )

    def update_view():
        images = IMAGE_SETS.get(selected_set, [])
        if images:
            preview_img.src = images[current_index]
            page.update()

    def navigate_left(e):
        nonlocal current_index
        images = IMAGE_SETS.get(selected_set, [])
        if images:
            current_index = (current_index - 1) % len(images)
            update_view()

    def navigate_right(e):
        nonlocal current_index
        images = IMAGE_SETS.get(selected_set, [])
        if images:
            current_index = (current_index + 1) % len(images)
            update_view()

    def on_set_change(e):
        nonlocal selected_set, current_index
        selected_set = e.control.value
        current_index = 0
        update_view()

    # Dropdown setup
    set_dropdown = ft.Dropdown(
        value=selected_set,
        width=220,
        options=[ft.dropdown.Option(s) for s in IMAGE_SETS.keys()],
        on_select=on_set_change,
        border_color=ft.Colors.GREY_700,
        color=ft.Colors.WHITE,
        focused_border_color=ft.Colors.RED_600,
    )

    return ft.View(
        route="/gallery",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                padding=20,
                content=ft.Column(
                    [
                        # Header with Back Button and Title
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Back",
                                    on_click=go_back,
                                    width=100,
                                ),
                                ft.Text(
                                    "Animatronic Gallery",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        ft.Divider(height=15, color=ft.Colors.GREY_800),

                        # Set Selector Dropdown
                        ft.Row(
                            [
                                ft.Text("Select Set:", color=ft.Colors.GREY_400, size=16),
                                set_dropdown,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),

                        # Main Display Area with Left/Right Navigation Arrows
                        ft.Container(
                            expand=True,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(1, ft.Colors.GREY_800),
                            border_radius=10,
                            padding=15,
                            bgcolor=ft.Colors.GREY_900,
                            width=400,
                            content=ft.Row(
                                [
                                    # Previous Image Button
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK_IOS_NEW,
                                        icon_color=ft.Colors.RED_600,
                                        icon_size=36,
                                        tooltip="Previous Image",
                                        on_click=navigate_left,
                                    ),
                                    # Single Preview Image
                                    preview_img,
                                    # Next Image Button
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_FORWARD_IOS,
                                        icon_color=ft.Colors.RED_600,
                                        icon_size=36,
                                        tooltip="Next Image",
                                        on_click=navigate_right,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True,
                            ),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    expand=True,
                ),
            )
        ],
    )