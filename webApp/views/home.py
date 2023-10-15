
import flet as ft

from styles.s_home import SHome
from styles.styles import Styles


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

    # Gets from the class :class:`Styles` from the file :file:`styles.py` the styles
    # for the home page.
    styles: dict[str] = Styles.home_styles()

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
                    alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                    controls = [
                        # Title of the home page
                        ft.Row(
                            alignment = ft.MainAxisAlignment.CENTER,
                            controls = [
                                title
                            ]
                        )
                    ]
                )
            )
        ]
    )

    return view
