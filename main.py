import asyncio
import sys

import flet as ft
import platform
import os
import subprocess
import requests
import zipfile
import shutil
import time
import threading
from pathlib import Path
from proghandler import ProgressHandler
import loading

import logging

# Disable Flet's noisy logging
logging.getLogger("flet").setLevel(logging.WARNING)

logger = logging.getLogger("FNAFLauncher")
logger.setLevel(logging.INFO)

handler = ProgressHandler()
handler.setFormatter(
    logging.Formatter("[%(levelname)s] %(message)s")
)

logger.addHandler(handler)

logger.info("Launcher started")

# ============================================
# GAME LIST - Add your games here!
# ============================================
GAMES = [
    {
        "id": "fnaf1",
        "name": "Five Nights at Freddy's",
        "windows_url": "https://abrehamrahi.ir/o/public/bN3sGN75/",
        "image": "assets/images/fnaf1.png",
    },
    {
        "id": "fnaf2",
        "name": "Five Nights at Freddy's 2",
        "windows_url": "https://s100.picofile.com/d/jatUrak18g2vvRVBOpN0a5c9l3eYtviu4FeWr3sfRfMarUdnuOu8vwbibvVDbeGJHkRXBI0k221j2qntfALjgP7SrPccPRY9sGx7gg/FiveNightsatFreddys2.zip",
        "image": "assets/images/fnaf2.png",
    },
    {
        "id": "fnaf3",
        "name": "Five Nights at Freddy's 3",
        "windows_url": "https://s100.picofile.com/d/X4oKa9gTL8CSW0YUX8QGqd7ucYKZ9uPEWAQ1B7spXLfKc3hifrliotpj_N3oLdLGC8NBpqpiGWmRLNXIH8f-nK3WzHVEqe4FDKWKqQ/FiveNightsatFreddys3.zip",
        "image": "assets/images/fnaf3.png",
    },
    {
        "id": "fnaf4",
        "name": "Five Nights at Freddy's 4",
        "windows_url": "https://s100.picofile.com/d/PsbfnllqoqJclb0UDNYe9kU30jHesirZ9M6rsBogGidl1C7eqN808Y0YOkMHYEzuwpXwGEY-P6JWxjlh-B_r-MlH4G_xBmYz_uOqRw/FiveNightsatFreddys4.zip",
        "image": "assets/images/fnaf4.png",
    },
]


class FNAFLauncher:
    def __init__(self):
        self.page = None
        self.game_name = "Five Nights at Freddy's"

        self.system = platform.system()
        self.is_windows = self.system == "Windows"

        # Use Downloads folder for Windows
        self.download_dir = Path.home() / "Downloads" / "FNAF_Launcher"

        self.download_dir.mkdir(parents=True, exist_ok=True)

        # Use first game as default
        self.current_game = GAMES[0] if GAMES else None
        self.current_index = 0
        self.total_games = len(GAMES)

        self.links = {
            "windows": self.current_game["windows_url"] if self.current_game else ""
        }

        self.get_local_path()
        self.download_running = False
        self.stop_download = False  # Flag to stop download
        self.progress = 0.0
        self.status = "Ready"

    def get_local_path(self):
        """Dynamic file path based on current game ID"""
        if self.current_game is None:
            return None

        game_id = self.current_game["id"]
        self.local_file = self.download_dir / f"{game_id}.zip"
        return self.local_file

    def check_file_exists(self):
        return self.local_file is not None and self.local_file.exists() and self.local_file.stat().st_size > 0

    def download_game(self):
        url = self.links["windows"]
        self.stop_download = False  # Reset stop flag
        try:
            self.status = "Connecting..."
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()
            self.download_dir.mkdir(parents=True, exist_ok=True)

            total_mb = total_size / (1024 * 1024) if total_size > 0 else 0
            if total_mb > 0:
                self.status = f"Downloading: 0.0 MB / {total_mb:.1f} MB (0%)"
            else:
                self.status = "Downloading... (size unknown)"

            with open(self.local_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        # Check if stop flag is set
                        if self.stop_download:
                            f.close()
                            # Delete the partial file
                            if self.local_file.exists():
                                self.local_file.unlink()
                            self.status = "Download stopped"
                            return False

                        f.write(chunk)
                        downloaded += len(chunk)
                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed / (1024 * 1024) if elapsed > 0 else 0

                        if total_size > 0:
                            self.progress = downloaded / total_size
                            downloaded_mb = downloaded / (1024 * 1024)
                            self.status = f"Downloading: {downloaded_mb:.1f} MB / {total_mb:.1f} MB ({self.progress * 100:.1f}%) - {speed:.1f} MB/s"
                        else:
                            downloaded_mb = downloaded / (1024 * 1024)
                            self.status = f"Downloading: {downloaded_mb:.1f} MB downloaded - {speed:.1f} MB/s"
                            self.progress = 0.5

            self.status = "Download complete!"
            return True

        except Exception as e:
            self.status = f"Error: {str(e)}"
            print(f"Download error: {e}")
            return False

    def stop_download_impl(self):
        """Stop the current download"""
        self.stop_download = True

    def launch_with_loading(self, page):
        """Launch the game with a loading screen."""

        game_id = self.current_game["id"]
        game_name = self.current_game["name"]

        def launch_func():
            return self.launch_windows_game()

        loading.launch_with_loading(
            page,
            launch_func,
            loading_message=f"Launching {game_name}...",
            game_name=game_name,
            game_id=game_id,
            minimum_time=5.0,
        )

        return True

        thread.start()

        return thread

    def launch_windows_game(self):
        if not self.local_file.exists():
            return False

        if self.local_file.suffix == '.zip':
            # Use current game ID for extract directory
            game_id = self.current_game["id"] if self.current_game else "fnaf1"
            extract_dir = self.download_dir / game_id
            extract_dir.mkdir(exist_ok=True)

            # Only extract if not already extracted
            exe_files = list(extract_dir.rglob("*.exe"))
            if not exe_files:
                with zipfile.ZipFile(self.local_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                exe_files = list(extract_dir.rglob("*.exe"))

            if exe_files:
                # Launch game (non-blocking)
                subprocess.Popen([str(exe_files[0])], shell=True, cwd=str(extract_dir))
                return True
            return False
        else:
            # Launch game (non-blocking)
            subprocess.Popen([str(self.local_file)], shell=True)
            return True

    def install_or_play(self):
        # Windows flow
        if self.check_file_exists():
            return "launched" if self.launch_windows_game() else "launch_failed"
        else:
            return "download_needed"

    def get_storage_info(self):
        if self.download_dir.exists():
            size = sum(f.stat().st_size for f in self.download_dir.rglob("*") if f.is_file())
            return size
        return 0

    def clear_game(self):
        deleted = False

        # Delete the ZIP file
        if self.local_file is not None and self.local_file.exists():
            try:
                self.local_file.unlink()
                deleted = True
            except Exception as e:
                print(f"Error deleting {self.local_file}: {e}")

        # Delete the extracted game folder
        if self.current_game is not None:
            game_id = self.current_game["id"]
            extract_dir = self.download_dir / game_id
            if extract_dir.exists():
                try:
                    shutil.rmtree(extract_dir)
                    deleted = True
                except Exception as e:
                    print(f"Error deleting extracted folder: {e}")

        # If the download directory is empty, remove it
        try:
            if self.download_dir.exists() and not any(self.download_dir.iterdir()):
                self.download_dir.rmdir()
        except Exception as e:
            print(f"Could not remove empty directory: {e}")

        return deleted

    def select_game(self, index):
        """Select a game by index"""
        if 0 <= index < self.total_games:
            self.current_index = index
            self.current_game = GAMES[index]
            self.links["windows"] = self.current_game["windows_url"]
            self.local_file = self.get_local_path()
            return True
        return False


def settings_page(page: ft.Page):
    """Settings page content"""
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

    logger.info("CWD: %s", Path.cwd())
    logger.info("Background exists: %s", Path("assets/images/background.gif").exists())

    background = ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src="images/background.gif",
            fit=ft.BoxFit.COVER,
        ),
        content=ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            content=settings_container,
        ),
    )


def main(page: ft.Page):
    page.title = "Five Nights at Freddy's Launcher"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = True

    launcher = FNAFLauncher()

    # Create spinner
    spinner = ft.ProgressRing(
        visible=False,
        width=30,
        height=30,
        stroke_width=3,
        color=ft.Colors.RED_400,
    )

    status_text = ft.Text("Ready", color=ft.Colors.GREY_400, size=14)
    progress_bar = ft.ProgressBar(width=300, visible=False, color=ft.Colors.RED)
    file_status = ft.Text("Checking...", size=12, color=ft.Colors.GREY_400)
    storage_text = ft.Text("", size=12, color=ft.Colors.GREY_500)
    btn_text = ft.Text("Play")

    cards_section = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    def update_file_status():
        if launcher.check_file_exists():
            file_status.value = "Downloaded"
            file_status.color = ft.Colors.GREEN
        else:
            file_status.value = "Not downloaded"
            file_status.color = ft.Colors.RED

        size = launcher.get_storage_info()
        storage_text.value = f"{size / (1024 * 1024):.1f} MB" if size > 0 else "0 MB"
        page.update()

    def update_button_state():
        if launcher.check_file_exists():
            btn_text.value = "Play"
        else:
            btn_text.value = "Download"
        page.update()

    def create_game_card(game, index, is_selected=False):
        """Create a styled game card with 768x1024 aspect ratio"""
        # Different sizes for selected vs non-selected
        if is_selected:
            width = 240
            height = 320  # 240 * 4/3
            font_size = 18
            button_size = 28  # Match the clear button size
            border_width = 2
        else:
            width = 200
            height = 267  # 200 * 4/3 rounded
            font_size = 14
            button_size = 22  # Match the clear button size
            border_width = 1

        # Flat card with animation
        card = ft.Container(
            width=width,
            height=height,
            bgcolor=ft.Colors.BLACK,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e, idx=index: on_card_hover(e, idx),
            on_click=lambda e, idx=index: select_game(idx),
            content=ft.Stack(
                [
                    # Background image - fits 768x1024
                    ft.Container(
                        width=width,
                        height=height,
                        image=ft.DecorationImage(
                            src=game["image"],
                            fit=ft.BoxFit.COVER,
                        ),
                    ),
                    # Dark overlay (lighter for selected)
                    ft.Container(
                        width=width,
                        height=height,
                        bgcolor=ft.Colors.with_opacity(0.3 if is_selected else 0.6, ft.Colors.BLACK),
                    ),
                    # Selected border with animation
                    ft.Container(
                        width=width,
                        height=height,
                        border=ft.Border.all(
                            border_width,
                            ft.Colors.WHITE if is_selected else ft.Colors.TRANSPARENT
                        ),
                    ),
                    # Glow effect for selected card
                    ft.Container(
                        width=width,
                        height=height,
                        bgcolor=ft.Colors.with_opacity(0.1 if is_selected else 0, ft.Colors.WHITE),
                        animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                    ),
                    # Play button (top-left corner, shown only for selected card)
                    ft.Container(
                        content=ft.ElevatedButton(
                            "▶",
                            on_click=lambda e, idx=index: play_game(idx),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_900,
                                color=ft.Colors.WHITE,
                                padding=ft.Padding(8, 2, 8, 2),
                            ),
                            width=button_size,
                            height=button_size * 0.875,
                        ),
                        top=8,
                        left=8,
                        visible=is_selected,
                        animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
                    ),
                    # Clear button (top-right corner, shown only for selected card)
                    ft.Container(
                        content=ft.ElevatedButton(
                            "✕",
                            on_click=lambda e, idx=index: on_clear_from_card(idx),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.GREY_800),
                                color=ft.Colors.WHITE,
                                padding=ft.Padding(8, 2, 8, 2),
                            ),
                            width=button_size,
                            height=button_size * 0.875,
                        ),
                        top=8,
                        right=8,
                        visible=is_selected,
                        animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
                    ),
                ]
            ),
        )
        return card

    def rebuild_carousel():
        """Rebuild the carousel with current selection"""
        cards_section.controls.clear()

        # Show all games with selected one bigger
        for idx, game in enumerate(GAMES):
            is_selected = (idx == launcher.current_index)
            card = create_game_card(game, idx, is_selected)
            cards_section.controls.append(card)

        page.update()

    def select_game(index):
        """Select a game and update the carousel"""
        if launcher.select_game(index):
            update_file_status()
            update_button_state()
            rebuild_carousel()
            status_text.value = f"Selected: {launcher.current_game['name']}"
            status_text.color = ft.Colors.GREEN
            page.update()

    def on_card_hover(e, index):
        """Handle card hover"""
        pass

    def stop_download(e):
        """Stop the current download"""
        launcher.stop_download_impl()
        status_text.value = "Stopping download..."
        status_text.color = ft.Colors.ORANGE
        btn_text.value = "Download"
        page.update()

    def update_ui():
        """Update UI with current progress and status"""
        progress_bar.value = launcher.progress
        status_text.value = launcher.status
        page.update()

    def download_loop():
        """Background download loop that updates UI periodically"""
        progress_bar.visible = True
        progress_bar.value = 0.0
        stop_button.visible = True

        # Start the download in a separate thread
        success = launcher.download_game()

        # Hide stop button
        stop_button.visible = False

        if success:
            status_text.value = "Download complete! Launching..."
            status_text.color = ft.Colors.GREEN

            if launcher.launch_with_loading(page):
                status_text.value = "Game launched!"
                status_text.color = ft.Colors.GREEN
                btn_text.value = "Launched"
            else:
                status_text.value = "Failed to launch game."
                status_text.color = ft.Colors.RED
                btn_text.value = "Play"
        else:
            # Check if it was stopped or failed
            if launcher.stop_download:
                status_text.value = "Download stopped."
                status_text.color = ft.Colors.ORANGE
                btn_text.value = "Download"
            else:
                status_text.value = "Download failed."
                status_text.color = ft.Colors.RED
                btn_text.value = "Retry"

        progress_bar.visible = False
        update_file_status()
        launcher.download_running = False

    def play_game(index):
        """Play or download the selected game"""
        if launcher.download_running:
            return

        if launcher.check_file_exists():
            status_text.value = "Launching game..."
            status_text.color = ft.Colors.ORANGE
            page.update()

            if launcher.launch_with_loading(page):
                status_text.value = "Game launched!"
                status_text.color = ft.Colors.GREEN
            else:
                status_text.value = "Failed to launch game."
                status_text.color = ft.Colors.RED

            page.update()
            return

        # Start download
        launcher.progress = 0.0
        launcher.status = "Starting download..."
        status_text.value = launcher.status
        status_text.color = ft.Colors.ORANGE
        btn_text.value = "Downloading..."
        progress_bar.visible = True
        progress_bar.value = 0.0
        stop_button.visible = True
        page.update()

        launcher.download_running = True

        # Start a thread for UI updates
        async def ui_updater():
            last_status = None
            last_progress = None

            while launcher.download_running:
                progress = launcher.progress
                status = launcher.status

                progress_changed = (
                        progress != last_progress or
                        status != last_status
                )

                if progress_changed:
                    bar_width = 30
                    filled = int(bar_width * progress)
                    bar = "━" * filled + "─" * (bar_width - filled)

                    percent = progress * 100

                    logger.info(
                        f"{status} {bar} {percent:6.2f}%",
                        extra={"progress": True},
                    )

                    last_progress = progress
                    last_status = status

                progress_bar.value = progress
                status_text.value = status

                page.update()

                await asyncio.sleep(0.1)

            logger.info("Download finished!")



        page.run_task(ui_updater)

        # Start download in a separate thread
        def download_wrapper():
            download_loop()

        threading.Thread(target=download_wrapper, daemon=True).start()

    def on_clear_click(e):
        if launcher.clear_game():
            status_text.value = "Game files cleared"
            status_text.color = ft.Colors.ORANGE
            btn_text.value = "Download"
            update_file_status()
            rebuild_carousel()
            page.update()
        else:
            status_text.value = "Nothing to clear"
            status_text.color = ft.Colors.GREY_400
            page.update()

    def on_clear_from_card(index):
        """Clear the selected game from the card"""
        if launcher.current_index == index:
            if launcher.clear_game():
                status_text.value = "Game files cleared"
                status_text.color = ft.Colors.ORANGE
                btn_text.value = "Download"
                update_file_status()
                rebuild_carousel()
                page.update()
            else:
                status_text.value = "Nothing to clear"
                status_text.color = ft.Colors.GREY_400
                page.update()

    def open_settings(e):
        """Open the settings page"""
        page.go("/settings")

    def route_change(e):
        """Handle route changes"""
        if page.route == "/settings":
            page.clean()
            page.add(settings_page(page))
        else:
            page.clean()
            page.add(main_content)
        page.update()

    # Build the UI
    header = ft.Row(
        [
            ft.Container(expand=True),
            ft.Image(
                src="assets/images/launcher-title.png",
                width=200,
                height=200,
                fit=ft.BoxFit.CONTAIN,
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    "Settings",
                    on_click=open_settings,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
                        color=ft.Colors.WHITE,
                        padding=ft.Padding(15, 8, 15, 8),
                    ),
                ),
                padding=ft.Padding(0, 0, 20, 0),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Game counter
    game_counter = ft.Text(
        f"{launcher.current_index + 1} / {launcher.total_games}",
        color=ft.Colors.GREY_400,
        size=14,
    )

    # Stop button (hidden by default)
    stop_button = ft.ElevatedButton(
        "STOP",
        on_click=stop_download,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ORANGE_900,
            color=ft.Colors.WHITE,
            padding=ft.Padding(30, 15, 30, 15),
        ),
        width=150,
        visible=False,
    )

    # Control buttons
    control_buttons = ft.Row(
        [
            ft.ElevatedButton(
                "PLAY",
                on_click=lambda e: play_game(launcher.current_index),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED_900,
                    color=ft.Colors.WHITE,
                    padding=ft.Padding(30, 15, 30, 15),
                ),
                width=150,
            ),
            stop_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # Status bar
    status_bar = ft.Row(
        [
            file_status,
            ft.Text("|", color=ft.Colors.GREY_600),
            storage_text,
            ft.Text("|", color=ft.Colors.GREY_600),
            status_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Main content
    main_content = ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src="assets/images/background.gif",
            fit=ft.BoxFit.COVER,
        ),
        content=ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            content=ft.Column(
                [
                    ft.Container(height=20),
                    header,
                    ft.Container(height=20),
                    ft.Container(
                        content=cards_section,
                        height=420,
                        margin=ft.Margin(0, 10, 0, 10),
                    ),
                    control_buttons,
                    ft.Container(height=10),
                    ft.Row(
                        [progress_bar],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=10),
                    status_bar,
                    ft.Container(height=10),
                    spinner,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
        ),
    )

    # Initial setup
    page.on_route_change = route_change

    # Show main content directly
    page.add(main_content)

    # Initial setup for the main page
    select_game(0)
    update_file_status()




ft.run(main, assets_dir="assets")