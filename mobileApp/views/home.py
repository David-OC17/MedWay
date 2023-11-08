
import flet as ft

from styles.s_home import SHome
from other.nav_bar import NavBar


def Home(page: ft.Page, date_time: ft.Text) -> ft.Column:
    """
    Home page of the app.

    Shows the logo of the company, a welcome message, and the navigation bar.

    Uses the controls defined in the class :class:`SHome` from the file :file:`s_home.py`

    - Parameters:
        - page (ft.Page): The page to add the home page to.

    - Returns:
        - ft.Container: The home page.
    """

    # Navigation bar
    nav_bar: ft.Card = NavBar().nav_bar(page)

    # Title of the home page
    title: ft.Container = SHome.title(date_time)

    # Properties of the home page
    view: ft.Column = ft.Column(
        spacing = 25,
        # Composed by:
        # - Title of the home page
        # - Welcome message
        controls = [
            ft.Container(
                expand = True,
                content = ft.Column(
                    alignment = ft.MainAxisAlignment.CENTER,
                    controls = [
                        # Title of the home page
                        ft.Row(
                            alignment = ft.MainAxisAlignment.CENTER,
                            controls = [
                                nav_bar,
                                title
                            ]
                        )
                    ]
                )
            )
        ]
    )

    return view
