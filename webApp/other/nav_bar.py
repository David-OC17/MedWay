
import flet as ft

from styles.styles import Styles


# Style properties for navigation bar
styles: dict[str] = Styles.nav_bar_styles()


class NavBar:
    """
    Contains all the methods for creating the navigation bar of the app.
    """

    def __init__(self) -> None:
        self._nav_bar: ft.Container = ft.Container()


    def _button_on_hover(self, _: ft.HoverEvent, button: ft.Card) -> None:
        """
        Elevates the button on hover.

        Parameters:
            - :param:`_` (ft.HoverEvent): The hover event.
            - :param:`button` (ft.Card): The button to be elevated.

        Returns:
            - No return value.
        """

        if _.data == "true":
            for __ in range(25):
                button.elevation += 1
                button.update()

        else:
            for __ in range(25):
                button.elevation -= 1
                button.update()


    def nav_bar(self, page: ft.Page) -> ft.Container:
        """
        Creates the navigation bar of the app. Displayed as a column of buttons.

        Parameters:
            - :param:`page` (ft.Page): The current page of the app.

        Returns:
            - :return:`nav_bar` (ft.Container): The navigation bar of the app.
        """

        _home_button: ft.Card = ft.Card(
            elevation = 0,
            color = styles["button"]["bgcolor"],
            content = ft.Container(
                width = styles["button"]["width"],
                height = styles["button"]["height"],
                border_radius = styles["button"]["border_radius"],
                alignment = ft.alignment.center,
                content = ft.Image(
                    src = "images/logo.png",
                    fit = ft.ImageFit.FILL
                ),
                on_hover = lambda _: self._button_on_hover(_, _home_button),
            )
        )

        _week_reports_button: ft.Card = ft.Card(
            elevation = 0,
            color = styles["button"]["bgcolor"],
            content = ft.Container(
                width = styles["button"]["width"],
                height = styles["button"]["height"],
                border_radius = styles["button"]["border_radius"],
                alignment = ft.alignment.center,
                content = ft.Icon(
                    name = ft.icons.DESCRIPTION,
                    color = styles["button"]["button_color"],
                    size = styles["button"]["button_size"]
                ),
                on_hover = lambda _: self._button_on_hover(_, _week_reports_button),
            )
        )

        _general_reports_button: ft.Card = ft.Card(
            elevation = 0,
            color = styles["button"]["bgcolor"],
            content = ft.Container(
                width = styles["button"]["width"],
                height = styles["button"]["height"],
                border_radius = styles["button"]["border_radius"],
                alignment = ft.alignment.center,
                content = ft.Icon(
                    name = ft.icons.COLLECTIONS_BOOKMARK,
                    color = styles["button"]["button_color"],
                    size = styles["button"]["button_size"]
                ),
                on_hover = lambda _: self._button_on_hover(_, _general_reports_button),
            )
        )

        _analytics_button: ft.Card = ft.Card(
            elevation = 0,
            color = styles["button"]["bgcolor"],
            content = ft.Container(
                width = styles["button"]["width"],
                height = styles["button"]["height"],
                border_radius = styles["button"]["border_radius"],
                alignment = ft.alignment.center,
                content = ft.Icon(
                    name = ft.icons.QUERY_STATS,
                    color = styles["button"]["button_color"],
                    size = styles["button"]["button_size"]
                ),
                on_hover = lambda _: self._button_on_hover(_, _analytics_button),
            )
        )

        self._nav_bar = ft.Container(
            width = styles["nav_bar"]["width"],
            height = styles["nav_bar"]["height"],
            bgcolor = styles["nav_bar"]["bgcolor"], 
            alignment = ft.alignment.center,
            content = ft.Column(
                spacing = 25,
                alignment = ft.MainAxisAlignment.START,
                controls = [
                    # Home page button
                    _home_button,
                    # Week reports button
                    _week_reports_button,
                    # General reports button
                    _general_reports_button,
                    # Analytics button
                    _analytics_button,
                ]
            )
        )

        return self._nav_bar
