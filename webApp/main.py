
import flet as ft


def main(page: ft.Page):
    # Page properties
    page.title: str = "MedWay Dashboard"
    page.bgcolor: str = "#FFFFFF"
    page.fonts: dict[str] = {
        "Arimo" : "/fonts/Arimo-VariableFont_wght.ttf",
        "Roboto Regular" : "/fonts/Roboto-Regular.ttf",
        "Roboto Bold" : "/fonts/Roboto-Bold.ttf",
    }

    text: ft.Text = ft.Text(
        "MedWay Solutions", 
        font_family = "Roboto Bold", 
        size = 70, 
        color = "#000000"
    )

    text_2: ft.Text = ft.Text(
        "Sept. 20 - Sept. 26",
        font_family = "Arimo",
        size = 20,
        color = "#000000"
    )

    page.add(text)
    page.add(text_2)
    page.update()


if __name__ == "__main__":
    ft.app(
        target = main, view = ft.AppView.FLET_APP_WEB,
        web_renderer = ft.WebRenderer.CANVAS_KIT, assets_dir = "webApp/assets"
    )