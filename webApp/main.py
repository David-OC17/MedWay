
import flet as ft

from views.router import Router


def main(page: ft.Page):
    # Page properties
    page.title: str = "MedWay Dashboard"
    page.bgcolor: str = "#FFFFFF"
    page.fonts: dict[str] = {
        "Arimo" : "/fonts/Arimo-VariableFont_wght.ttf",
        "Roboto Regular" : "/fonts/Roboto-Regular.ttf",
        "Roboto Bold" : "/fonts/Roboto-Bold.ttf",
    }

    # Declares the router from the Router class to handle the navigation
    # between the pages.
    router: Router = Router(page)

    # Assignment of the route to which the user will be redirected by default.
    page.on_route_change = router.route_change

    # Adds the home page to the page.
    page.add(router.view)

    # Access to the app's home screen.
    page.go("/")


if __name__ == "__main__":
    ft.app(
        target = main, view = ft.AppView.FLET_APP_WEB,
        web_renderer = ft.WebRenderer.CANVAS_KIT, assets_dir = "webApp/assets"
    )