
import flet as ft

from styles.s_month_reports import SMonthReports


def MonthReports(page: ft.Page) -> ft.Column:
    """
    Monthly reports page of the app.

    Shows the company name, the title of the page, navigation bar, and the monthly reports.

    Uses the controls defined in the class :class:`SMonthlyReports` from the file :file:`s_monthly_reports.py`

    - Parameters:
        - page (ft.Page): The page to add the monthly reports page to.

    - Returns:
        - ft.Column: The monthly reports page.
    """

    # Title of the monthly reports page
    title: ft.Container = SMonthReports.title()
    # Monthly reports
    monthly_reports: ft.Container = SMonthReports().monthly_reports(page)

    # Properties of the monthly reports
    view: ft.Column = ft.Column(
        # Composed by:
        # - Title of the monthly reports
        # - monthly reports
        controls = [
            ft.Container(
                expand = True,
                padding = ft.Padding(top = 20, bottom = 10, left = 25, right = 25),
                alignment = ft.alignment.center,
                content = ft.Column(
                    controls = [
                        # Title of the monthly reports
                        title,
                        # Monthly reports
                        monthly_reports
                    ]
                )
            )
        ]
    )

    return view