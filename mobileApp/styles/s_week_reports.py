
import flet as ft

from styles.styles import Styles


# Style properties for the week reports page
styles: dict[str] = Styles.week_reports_styles()


class SWeekReports:
    """
    Properties of the controls used by the function :function:`WeekReports`
    from the :file:`week_reports.py` for creating the week reports page.
    """

    def title() -> ft.Container:
        """
        Title of the week reports page.
        
        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`title_content` (ft.Container): Title of the week reports page.
        """

        # Title of the week reports page
        title: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    ft.Text(
                        "Weekly Reports",
                        font_family = styles["title"]["font"],
                        size = styles["title"]["size"],
                        color = styles["title"]["color"],
                        weight = ft.FontWeight.BOLD,
                        text_align = ft.TextAlign.CENTER
                    )
                ]
            )
        )

        # Content for the company name and the title of the week reports page
        title_content: ft.Container = ft.Container(
            height = styles["title"]["height"],
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    # Title of the week reports page
                    title
                ]
            )
        )

        return title_content
