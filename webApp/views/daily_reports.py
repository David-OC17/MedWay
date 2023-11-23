
import flet as ft

from styles.s_daily_reports import SDailyReports
from other.nav_bar import NavBar


def DailyReports(page: ft.Page) -> ft.Column:
    """
    Daily reports page of the app.

    Shows the company name, the title of the page, navigation bar, and the daily reports.

    Uses the controls defined in the class :class:`SDailyReports` from the file :file:`s_daily_reports.py`

    - Parameters:
        - page (ft.Page): The page to add the daily reports page to.

    - Returns:
        - ft.Container: The daily reports page.
    """

    # Navigation bar
    nav_bar: ft.Container = NavBar().nav_bar(page)

    # Title of the daily reports page
    title: ft.Container = SDailyReports.title()
    # Daily reports
    daily_reports: ft.Container = SDailyReports().daily_reports(page)

    # Properties of the daily reports page
    view: ft.Column = ft.Column(
        spacing = 25,
        # Composed by:
        # - Navigation bar
        # - Title of the daily reports page
        # - Daily reports
        controls = [
            ft.Container(
                expand = True,
                content = ft.Row(
                    controls = [
                        # Navigation bar
                        nav_bar,
                        # Container with the title of the daily reports page
                        ft.Container(
                            expand = True,
                            padding = ft.Padding(top = 25, bottom = 25, left = 35, right = 50),
                            alignment = ft.alignment.center,
                            content = ft.Column(
                                controls = [
                                    # Title of the daily reports page
                                    title,
                                    # Daily reports
                                    daily_reports
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )

    return view
