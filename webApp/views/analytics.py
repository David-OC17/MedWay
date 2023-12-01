
import flet as ft

from styles.s_analytics import SAnalytics
from other.nav_bar import NavBar


def Analytics(page: ft.Page) -> ft.Column:
    """
    Analytics page of the app.

    Shows the company name, the title of the page, navigation bar, and the analytics.

    Uses the controls defined in the class :class:`SAnalytics` from the file :file:`s_analytics.py`

    - Parameters:
        - page (ft.Page): The page to add the analytics page to.

    - Returns:
        - ft.Column: The analytics page.
    """

    # Navigation bar
    nav_bar: ft.Container = NavBar().nav_bar(page)

    # Refresh button for the data table
    page.floating_action_button: ft.FloatingActionButton = SAnalytics().refresh_button(page)

    # Title of the analytics page
    title: ft.Container = SAnalytics.title()
    # Table with the last batch of data
    table: ft.Container = SAnalytics().last_data_batch_table()

    # Properties of the analytics page
    view: ft.Column = ft.Column(
        spacing = 25,
        # Composed by:
        # - Navigation bar
        # - Title of the analytics page
        # - Analytics
        controls = [
            ft.Container(
                expand = True,
                content = ft.Row(
                    controls = [
                        # Navigation bar
                        nav_bar,
                        # Container with the title of the analytics page
                        ft.Container(
                            expand = True,
                            padding = ft.Padding(top = 25, bottom = 25, left = 35, right = 50),
                            alignment = ft.alignment.center,
                            content = ft.Column(
                                controls = [
                                    # Title of the analytics page
                                    title,
                                    # Table with the last batch of data
                                    table
                                ]
                            )
                        )
                    ]
                )
            ),
        ],
    )

    return view
