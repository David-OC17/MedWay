
import flet as ft
from time import strftime, sleep

from views.router import Router


def main(page: ft.Page) -> None:

    # Updates the current date and time on the home page.
    def current_date_time() -> None:
        """
        Updates the current date and time on the home page.

        - Parameters:
            - date_time (ft.Text): The text to update.

        - Returns:
            - No return value.
        """

        while True:
            date_time.value = now()
            date_time.update()
            sleep(1)


    # Page properties
    page.title: str = "MedWay Dashboard"
    page.bgcolor: str = "#FFFFFF"
    page.fonts: dict[str] = {
        "Arimo" : "/fonts/Arimo-VariableFont_wght.ttf",
        "Roboto Regular" : "/fonts/Roboto-Regular.ttf",
        "Roboto Bold" : "/fonts/Roboto-Bold.ttf",
    }

    # Current date and time
    now: str = lambda: strftime("%d/%b/%Y %H:%M:%S")

    # Text control containing the current date and time
    date_time: ft.Text = ft.Text(
        now(),
        font_family = "Roboto Regular",
        size = 70,
        color = "#000000",
        weight = ft.FontWeight.W_300,
        text_align = ft.TextAlign.CENTER
    )

    # Declares the router from the Router class to handle the navigation
    # between the pages.
    router: Router = Router(page, date_time)

    # Assignment of the route to which the user will be redirected by default.
    page.on_route_change = router.route_change

    # Adds the home page to the page.
    page.add(router.view)

    # Access to the app's home screen.
    page.go("/")

    # Updates the current date and time on the home page.
    current_date_time()



if __name__ == "__main__":
    ft.app(
        target = main, view = ft.AppView.WEB_BROWSER,
        web_renderer = ft.WebRenderer.CANVAS_KIT, assets_dir = "webApp/assets"
    )