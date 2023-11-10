
import flet as ft

from styles.s_week_reports import SWeekReports


def WeekReports(page: ft.Page) -> ft.Column:
    """
    Week reports page of the app.

    Shows the company name, the title of the page, navigation bar, and the week reports.

    Uses the controls defined in the class :class:`SWeekReports` from the file :file:`s_week_reports.py`

    - Parameters:
        - page (ft.Page): The page to add the week reports page to.

    - Returns:
        - ft.Container: The week reports page.
    """

    # Title of the week reports page
    title: ft.Container = SWeekReports.title()

    # Properties of the week reports page
    view: ft.Column = ft.Column(
        spacing = 10,
        # Composed by:
        # - Title of the week reports page
        # - Week reports
        controls = [
            # Container with the title of the week reports page
            ft.Container(
                expand = True,
                padding = ft.Padding(top = 35, bottom = 35, left = 25, right = 25),
                alignment = ft.alignment.center,
                content = ft.Column(
                    controls = [
                        # Title of the week reports page
                        title
                    ]
                )
            )
        ]
    )

    return view
