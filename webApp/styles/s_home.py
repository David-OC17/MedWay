
import flet as ft

from styles.styles import Styles


# Style properties for the home page
styles: dict[str] = Styles.home_styles()


class SHome:
    """
    Properties of the controls used by the function :function:`Home`
    from the :file:`home.py` for creating the home page.
    """

    def title(date_time: ft.Text) -> ft.Container:
        """
        Title of the home page.
        
        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`title_content` (ft.Container): Title of the home page.
        """

        # Title of the home page part 1 - MedWay
        title_part1: ft.Text = ft.Text(
            "MedWay",
            font_family = "Roboto Bold",
            size = styles["logo"]["size"],
            color = styles["logo"]["color1"],
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.CENTER
        )

        # Title of the home page part 2 - Solutions
        title_part2: ft.Text = ft.Text(
            "Solutions",
            font_family = "Roboto Bold",
            size = styles["logo"]["size"],
            color = styles["logo"]["color2"],
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.CENTER
        )

        # Container for the title of the home page
        title_content: ft.Container = ft.Container(
            border = ft.border.all(0, "#FF0000"),
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                spacing = 1,
                controls = [
                    title_part1,
                    title_part2,
                    date_time
                ]
            )
        )

        return title_content
