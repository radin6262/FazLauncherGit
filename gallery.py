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
    # 1. Dataset mapping sets to image arrays
    IMAGE_SETS = {
        "FNAF 1": [
            "gallery/Freddy_Fazbear (3).png",
            "gallery/Bonnie_Rabbit (1).png",
            "gallery/Chica (1).png",
            "gallery/foxy.png",
            "gallery/goldenfreddy.png",
        ],

        "FNAF 2": [
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

        "Extras": [
            "gallery/BareEndoClean.png",
            "gallery/Extra_BB.png",
            "gallery/Extra_Chica.png",
            "gallery/Extra_Puppet.png",
            "gallery/E0CA2759-4875-4D4C-A559-990401C9432E.png",
        ],
    }

    # State tracking selected image and set
    default_set = list(IMAGE_SETS.keys())[0]
    selected_set = default_set
    selected_image = IMAGE_SETS[default_set][0]

    def go_back(e):
        page.go("/")

    # Big preview image control
    preview_img = ft.Image(
        src=selected_image,
        fit=ft.BoxFit.CONTAIN,
        expand=True,
    )

    # Container for rendering small thumbnail items
    thumbnails_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
        wrap=True,
    )

    def select_image(img_path):
        nonlocal selected_image
        selected_image = img_path
        preview_img.src = img_path
        update_thumbnails()
        page.update()

    def update_thumbnails():
        thumbnails_row.controls.clear()
        images = IMAGE_SETS.get(selected_set, [])

        for img_path in images:
            is_selected = img_path == selected_image

            # Small image container item
            thumb_container = ft.Container(
                width=110,
                height=160,
                border_radius=8,
                border=ft.Border.all(
                    width=2,
                    color=ft.Colors.RED_600 if is_selected else ft.Colors.GREY_700,
                ),
                content=ft.Image(
                    src=img_path,
                    fit=ft.BoxFit.COVER,
                    border_radius=6,
                ),
                ink=True,
                on_click=lambda e, path=img_path: select_image(path),
            )
            thumbnails_row.controls.append(thumb_container)

    def on_set_change(e):
        nonlocal selected_set, selected_image
        selected_set = e.control.value
        images = IMAGE_SETS.get(selected_set, [])
        if images:
            selected_image = images[0]
            preview_img.src = selected_image
        update_thumbnails()
        page.update()

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

    # Initialize thumbnail list
    update_thumbnails()

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

                        # Small Thumbnails Row
                        thumbnails_row,

                        ft.Divider(height=15, color=ft.Colors.GREY_800),

                        # Large Preview Container Centered Below
                        ft.Container(
                            expand=True,
                            width=250,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(1, ft.Colors.GREY_800),
                            border_radius=10,
                            padding=10,
                            bgcolor=ft.Colors.GREY_900,
                            content=preview_img,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    expand=True,
                ),
            )
        ],
    )