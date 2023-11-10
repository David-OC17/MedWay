
import flet as ft

from styles.styles import Styles


# Style properties for the week reports page
styles: dict[str] = Styles.general_reports_styles()


class SGeneralReports:
    """
    Properties of the controls used by the function :function:`GeneralReports`
    from the :file:`general_reports.py` for creating the general reports page.
    """

    def title() -> ft.Container:
        """
        Title of the general reports page.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`title_content` (ft.Container): Title of the general reports page.
        """
        # Title of the general reports page
        title: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    ft.Text(
                        "General Reports",
                        font_family = styles["title"]["font"],
                        size = styles["title"]["size"],
                        color = styles["title"]["color"],
                        weight = ft.FontWeight.BOLD,
                        text_align = ft.TextAlign.CENTER
                    )
                ]
            )
        )

        # Container with the title of the general reports page
        title_content: ft.Container = ft.Container(
            height = styles["title"]["height"],
            alignment = ft.alignment.center,
            offset = ft.Offset(0,-0.1),
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    # Title of the general reports page
                    title
                ]
            )
        )

        return title_content
