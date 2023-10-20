
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
            width = styles["logo"]["width"],
            font_family = styles["logo"]["title_font"],
            size = styles["logo"]["size"],
            color = styles["logo"]["color1"],
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.CENTER
        )

        # Title of the home page part 2 - Solutions
        title_part2: ft.Text = ft.Text(
            "Solutions",
            width = styles["logo"]["width"],
            font_family = styles["logo"]["title_font"],
            size = styles["logo"]["title_size"],
            color = styles["logo"]["color2"],
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.CENTER,
            offset = ft.Offset(0, -0.3)
        )

        # Title of the home page
        title: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    title_part1,
                    title_part2,
                ]
            )
        ) 

        # Welcome text
        welcome: ft.Container = ft.Container(
            width = 575,
            alignment = ft.alignment.center,
            content = ft.Text(
                "Welcome",
                width = styles["logo"]["width"],
                font_family = styles["logo"]["text_font"],
                size = styles["logo"]["text_size"],
                color = styles["logo"]["color1"],
                weight = ft.FontWeight.BOLD,
                text_align = ft.TextAlign.CENTER,
            )
        )

        # Container for the components of the home page
        title_content: ft.Container = ft.Container(
            width = styles["logo"]["width"],
            height = styles["logo"]["height"],
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    ft.Row(
                        alignment = ft.MainAxisAlignment.CENTER,
                        controls = [
                            title,
                        ]
                    ),
                    ft.Row(
                        alignment = ft.MainAxisAlignment.CENTER,
                        controls = [
                            welcome,
                        ]
                    ),
                    ft.Row(
                        alignment = ft.MainAxisAlignment.CENTER,
                        controls = [
                            ft.Container(
                                alignment = ft.alignment.center,
                                content = date_time
                            ),
                        ]
                    )
                ]
            )
        )

        return title_content
