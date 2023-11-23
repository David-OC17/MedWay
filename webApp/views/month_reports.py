
import flet as ft

from styles.s_month_reports import SMonthReports
from other.nav_bar import NavBar


def MonthReports(page: ft.Page) -> ft.Column:
    """
    Monthly reports page of the app.

    Shows the company name, the title of the page, navigation bar, and the monthly reports.

    Uses the controls defined in the class :class:`SMonthReports` from the file :file:`s_month_reports.py`

    - Parameters:
        - page (ft.Page): The page to add the monthly reports page to.

    - Returns:
        - ft.Column: The monthly reports page.
    """

    # Navigation bar
    nav_bar: ft.Container = NavBar().nav_bar(page)

    # Title of the monthly reports page
    title: ft.Container = SMonthReports.title()
    # Monthly reports
    monthly_reports: ft.Container = SMonthReports().monthly_reports(page)

    # Properties of the monthly reports page
    view: ft.Column = ft.Column(
        spacing = 25,
        # Composed by:
        # - Navigation bar
        # - Title of the monthly reports page
        # - Monthly reports
        controls = [
            ft.Container(
                expand = True,
                content = ft.Row(
                    controls = [
                        # Navigation bar
                        nav_bar,
                        # Container with the title of the monthly reports page
                        ft.Container(
                            expand = True,
                            padding = ft.Padding(top = 25, bottom = 25, left = 35, right = 50),
                            alignment = ft.alignment.center,
                            content = ft.Column(
                                controls = [
                                    # Title of the monthly reports page
                                    title,
                                    # Monthly reports
                                    monthly_reports
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )

    return view
