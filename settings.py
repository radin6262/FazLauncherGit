import json
from pathlib import Path
import flet as ft

BACKGROUND_SETS_JSON = """
{
  "Set 1: FNAF 1": {
    "Animated": "bg/fnaf1.gif",
    "Freddy(1)": "bg/1.png",
    "Freddy Endo": "bg/endo.png"
  },
  "Set 2: FNAF 2": {
    "Animated": "bg/fnaf2.gif",
    "All Toys": "bg/fnaf2toys.png",
    "All Toys With Wither Bonnie": "bg/wb.png",
    "All Toys With Wither Chica": "bg/wc.png"
  },
  "Set 3: FNAF 3": {
    "Animated": "bg/fnaf3.gif",
    "SpringTrap": "bg/sp1.png"
  },
  "Set 4: Default": {
    "Static Noise": "bg/background.gif"
  }
}
"""

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


def save_config(config_data):
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
    except Exception as err:
        print(f"Error saving config: {err}")


def settings_page(page: ft.Page):
    bg_data = json.loads(BACKGROUND_SETS_JSON)
    config = load_config()

    saved_set = config.get("launcher_background_set", "")
    saved_option = config.get("launcher_background_option", "")
    saved_bg_path = config.get("launcher_background", "")

    def go_back(e):
        page.go("/")

    status_text = ft.Text(
        value=f"Saved: {saved_option}" if saved_option else "",
        size=14,
        color=ft.Colors.GREEN_400,
    )

    # Initial options setup
    initial_options = []
    is_disabled = True
    if saved_set in bg_data:
        initial_options = [ft.dropdown.Option(k) for k in bg_data[saved_set].keys()]
        is_disabled = False

    # Image preview control
    preview_image = ft.Image(
        src=saved_bg_path if saved_bg_path else "",
        width=300,
        height=170,
        fit=ft.BoxFit.COVER,
        border_radius=8,
        visible=True if saved_bg_path else False,
    )

    option_dropdown = ft.Dropdown(
        label="Select Background",
        width=300,
        options=initial_options,
        value=saved_option if saved_option in bg_data.get(saved_set, {}) else None,
        disabled=is_disabled,
        hint_text="Select a Set First" if is_disabled else None,
    )

    set_dropdown = ft.Dropdown(
        label="Select Background Set",
        width=300,
        options=[ft.dropdown.Option(s) for s in bg_data.keys()],
        value=saved_set if saved_set in bg_data else None,
    )

    def on_set_changed(e):
        selected_set = set_dropdown.value
        if not selected_set or selected_set not in bg_data:
            option_dropdown.options = []
            option_dropdown.value = None
            option_dropdown.disabled = True
            option_dropdown.hint_text = "Select a Set First"
            status_text.value = ""
            preview_image.visible = False
        else:
            opts = bg_data[selected_set]
            keys = list(opts.keys())

            first_key = keys[0]
            img_path = opts[first_key]

            option_dropdown.options = [ft.dropdown.Option(k) for k in keys]
            option_dropdown.value = first_key
            option_dropdown.disabled = False
            option_dropdown.hint_text = None

            # Update preview image
            preview_image.src = img_path
            preview_image.visible = True

            config["launcher_background_set"] = selected_set
            config["launcher_background_option"] = first_key
            config["launcher_background"] = img_path
            save_config(config)

            status_text.value = f"Saved: {first_key}"

        page.update()

    def on_option_changed(e):
        selected_set = set_dropdown.value
        selected_option = option_dropdown.value

        if selected_set in bg_data and selected_option in bg_data[selected_set]:
            img_path = bg_data[selected_set][selected_option]

            # Update preview image
            preview_image.src = img_path
            preview_image.visible = True

            config["launcher_background_set"] = selected_set
            config["launcher_background_option"] = selected_option
            config["launcher_background"] = img_path
            save_config(config)

            status_text.value = f"Saved: {selected_option}"
            page.update()

    set_dropdown.on_select = on_set_changed
    option_dropdown.on_select = on_option_changed

    return ft.View(
        route="/settings",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                padding=20,
                content=ft.Column(
                    [
                        ft.Text(
                            "Settings",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Divider(height=20, color=ft.Colors.GREY_800),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Launcher Background",
                                        size=20,
                                        weight=ft.FontWeight.W_600,
                                        color=ft.Colors.WHITE,
                                    ),
                                    set_dropdown,
                                    option_dropdown,
                                    preview_image,  # Displayed here
                                    status_text,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15,
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
                    spacing=10,
                    expand=True,
                ),
            )
        ],
    )