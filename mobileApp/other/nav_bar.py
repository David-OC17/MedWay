
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


    def _home_button_on_hover(self, _: ft.HoverEvent) -> None:
        """
        Elevates the home button on hover.

        Parameters:
            - :param:`_` (ft.HoverEvent): The hover event.

        Returns:
            - No return value.
        """

        if _.data == "true":
            for __ in range(20):
                self._nav_bar.content.controls[1].elevation += 1
                self._nav_bar.content.controls[1].update()

        else:
            for __ in range(20):
                self._nav_bar.content.controls[1].elevation -= 1
                self._nav_bar.content.controls[1].update()


    def _home_button_on_click(self, _: ft.ControlEvent, page: ft.Page) -> None:
        """
        Changes the route of the page on click.

        Parameters:
            - :param:`_` (ft.ControlEvent): The click event.
            - :param:`page` (ft.Page): The current page of the app.

        Returns:
            - No return value.
        """

        self._nav_bar.content.controls[1].elevation = 0

        page.go("/")


    def _week_reports_button_on_hover(self, _: ft.HoverEvent) -> None:
        """
        Elevates the week reports button on hover.

        Parameters:
            - :param:`_` (ft.HoverEvent): The hover event.

        Returns:
            - No return value.
        """

        if _.data == "true":
            for __ in range(20):
                self._nav_bar.content.controls[2].elevation += 1
                self._nav_bar.content.controls[2].update()

        else:
            for __ in range(20):
                self._nav_bar.content.controls[2].elevation -= 1
                self._nav_bar.content.controls[2].update()


    def _week_reports_button_on_click(self, _: ft.ControlEvent, page: ft.Page) -> None:
        """
        Changes the route of the page on click.

        Parameters:
            - :param:`_` (ft.ControlEvent): The click event.
            - :param:`page` (ft.Page): The current page of the app.

        Returns:
            - No return value.
        """

        self._nav_bar.content.controls[2].elevation = 0

        page.go("/week_reports")


    def _general_reports_button_on_hover(self, _: ft.HoverEvent) -> None:
        """
        Elevates the general reports button on hover.

        Parameters:
            - :param:`_` (ft.HoverEvent): The hover event.

        Returns:
            - No return value.
        """

        if _.data == "true":
            for __ in range(20):
                self._nav_bar.content.controls[3].elevation += 1
                self._nav_bar.content.controls[3].update()

        else:
            for __ in range(20):
                self._nav_bar.content.controls[3].elevation -= 1
                self._nav_bar.content.controls[3].update()


    def _general_reports_button_on_click(self, _: ft.ControlEvent, page: ft.Page) -> None:
        """
        Changes the route of the page on click.

        Parameters:
            - :param:`_` (ft.ControlEvent): The click event.
            - :param:`page` (ft.Page): The current page of the app.

        Returns:
            - No return value.
        """

        self._nav_bar.content.controls[3].elevation = 0

        page.go("/general_reports")


    def _analytics_button_on_hover(self, _: ft.HoverEvent) -> None:
        """
        Elevates the analytics button on hover.

        Parameters:
            - :param:`_` (ft.HoverEvent): The hover event.

        Returns:
            - No return value.
        """

        if _.data == "true":
            for __ in range(20):
                self._nav_bar.content.controls[4].elevation += 1
                self._nav_bar.content.controls[4].update()

        else:
            for __ in range(20):
                self._nav_bar.content.controls[4].elevation -= 1
                self._nav_bar.content.controls[4].update()


    def _analytics_button_on_click(self, _: ft.ControlEvent, page: ft.Page) -> None:
        """
        Changes the route of the page on click.

        Parameters:
            - :param:`_` (ft.ControlEvent): The click event.
            - :param:`page` (ft.Page): The current page of the app.

        Returns:
            - No return value.
        """

        self._nav_bar.content.controls[4].elevation = 0

        page.go("/analytics")


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
                on_hover = lambda _: self._home_button_on_hover(_),
                on_click = lambda _: self._home_button_on_click(_, page)
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
                on_hover = lambda _: self._week_reports_button_on_hover(_),
                on_click = lambda _: self._week_reports_button_on_click(_, page)
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
                on_hover = lambda _: self._general_reports_button_on_hover(_),
                on_click = lambda _: self._general_reports_button_on_click(_, page)
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
                on_hover = lambda _: self._analytics_button_on_hover(_),
                on_click = lambda _: self._analytics_button_on_click(_, page)
            )
        )

        self._nav_bar = ft.Container(
            width = styles["nav_bar"]["width"],
            height = styles["nav_bar"]["height"],
            bgcolor = styles["nav_bar"]["bgcolor"], 
            alignment = ft.alignment.center,
            content = ft.Column(
                spacing = 35,
                alignment = ft.MainAxisAlignment.START,
                controls = [
                    # Initial spacing
                    ft.Container(width = 75, height = 15),
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
