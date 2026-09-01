import flet as ft
import threading
import time
import logging
from proghandler import *
# Disable Flet's noisy logging
logging.getLogger("flet").setLevel(logging.WARNING)

logger = logging.getLogger("FNAFLauncher")
logger.setLevel(logging.INFO)

handler = ProgressHandler()
handler.setFormatter(
    logging.Formatter("[%(levelname)s] %(message)s")
)

logger.addHandler(handler)


def create_loading_screen(
    page: ft.Page,
    message: str = "Loading game...",
    game_name: str = "",
    game_id: str = "",
):
    """Create a centered loading dialog covering 80% of the screen."""

    background = f"images/loading/{game_id}.png"
    logger.info(f"bg for dialog: {background}")

    return ft.Stack(
        [
            ft.Container(
                left=0,
                right=0,
                top=0,
                bottom=0,

                image=ft.DecorationImage(
                    src=background,
                    fit=ft.BoxFit.COVER,
                ),

                content=ft.Stack(
                    [
                        # Spinner - bottom right
                        ft.Container(
                            bottom=30,
                            right=30,

                            content=ft.ProgressRing(
                                width=45,
                                height=45,
                                stroke_width=2,
                                color=ft.Colors.GREY_300,
                                value=None,
                            ),
                        ),
                    ],
                ),
            ),
        ],
        expand=True,
    )

def show_loading(
    page: ft.Page,
    message: str = "Loading game...",
    game_name: str = "",
    game_id: str = "",
):
    loading = create_loading_screen(
        page,
        message,
        game_name,
        game_id,
    )

    page.overlay.append(loading)
    page.update()

    return loading


def hide_loading(page: ft.Page, loading_overlay):
    """Hide loading screen overlay."""

    if loading_overlay in page.overlay:
        page.overlay.remove(loading_overlay)
        page.update()


def launch_with_loading(
    page: ft.Page,
    target_function,
    args=(),
    kwargs=None,
    loading_message="Loading game...",
    game_name="",
    game_id="",
    minimum_time=5.0,
):
    """Launch a function with a game-specific loading screen."""

    if kwargs is None:
        kwargs = {}

    # Show loading screen
    loading = show_loading(
        page,
        loading_message,
        game_name,
        game_id,
    )

    def run_with_loading():
        try:
            # Wait at least 5 seconds BEFORE launching
            time.sleep(minimum_time)

            # Launch the game
            target_function(*args, **kwargs)

        except Exception as e:
            print(f"Loading error: {e}")

        finally:
            hide_loading(page, loading)

    thread = threading.Thread(
        target=run_with_loading,
        daemon=True,
    )

    thread.start()

    return thread