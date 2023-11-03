
import flet as ft

from styles.styles import Styles


# Style properties for the week reports page
styles: dict[str] = Styles.analytics_styles()


class SAnalytics:
    """
    Properties of the controls used by the function :function:`Analytics`
    from the :file:`analytics.py` for creating the analytics page.
    """

    def title() -> ft.Container:
        """
        Title of the analytics page.
        
        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`title_content` (ft.Container): Title of the analytics page.
        """

        # Name of the company part 1 - MedWay
        company_name_1: ft.Text = ft.Text(
            "MedWay",
            font_family = styles["name"]["font"],
            size = styles["name"]["size"],
            color = styles["name"]["color1"],
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.START
        )

        # Name of the company part 2 - Solutions
        company_name_2: ft.Text = ft.Text(
            "Solutions",
            font_family = styles["name"]["font"],
            size = styles["name"]["size"],
            color = styles["name"]["color2"],
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.START,
            offset = ft.Offset(0, -0.3)
        )

        # Name of the company
        company_name: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.START,
                controls = [
                    company_name_1,
                    company_name_2
                ]
            )
        )

        # Title of the analytics page
        title: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    ft.Text(
                        "Data Analytics",
                        font_family = styles["title"]["font"],
                        size = styles["title"]["size"],
                        color = styles["title"]["color"],
                        weight = ft.FontWeight.BOLD,
                        text_align = ft.TextAlign.CENTER
                    )
                ]
            )
        )

        # Container with the title of the analytics page
        title_content: ft.Container = ft.Container(
            height = styles["title"]["height"],
            alignment = ft.alignment.center,
            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    # Name of the company
                    company_name,
                    # Title of the analytics page
                    title
                ]
            )
        )

        return title_content
