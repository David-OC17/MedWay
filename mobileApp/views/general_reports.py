
import flet as ft

from styles.s_general_reports import SGeneralReports


def GeneralReports(page: ft.Page) -> ft.Column:
    """
    General reports page of the app.

    Shows the company name, the title of the page, navigation bar, and the general reports.

    Uses the controls defined in the class :class:`SGeneralReports` from the file :file:`s_general_reports.py`

    - Parameters:
        - page (ft.Page): The page to add the general reports page to.

    - Returns:
        - ft.Column: The general reports page.
    """

    # Title of the general reports page
    title: ft.Container = SGeneralReports.title()

    # Properties of the general reports page
    view: ft.Column = ft.Column(
        spacing = 25,
        # Composed by:
        # - Title of the general reports page
        # - General reports
        controls = [
            ft.Container(
                expand = True,
                content = ft.Row(
                    controls = [
                        # Container with the title of the general reports page
                        ft.Container(
                            expand = True,
                            padding = ft.Padding(top = 25, bottom = 25, left = 35, right = 50),
                            alignment = ft.alignment.center,
                            content = ft.Column(
                                controls = [
                                    # Title of the general reports page
                                    title
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )

    return view
