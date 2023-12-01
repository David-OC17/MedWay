
import flet as ft

from styles.styles import Styles
from other.local_db_connection import LocalDBConnection


# Style properties for the week reports page
styles: dict[str] = Styles.analytics_styles()

# Local database connection
local_db_connection: LocalDBConnection = LocalDBConnection()


class SAnalytics:
    """
    Properties of the controls used by the function :function:`Analytics`
    from the :file:`analytics.py` for creating the analytics page.
    """

    def _row_on_hover(self, _: ft.HoverEvent, row: ft.Container) -> ft.Row:
        """
        Changes the background color of the row when the mouse is passed over it.

        Parameters:
            - :param:`_` (ft.HoverEvent): The event that triggers the function.
            - :param:`row` (ft.Row): The row that will change its background color.

        Returns:
            - Doesn't return anything.
        """

        if _.data == "true":
            row.bgcolor = styles["table"]["bgcolor_hover"]
            row.update()

        else:
            row.bgcolor = styles["table"]["bgcolor"]
            row.update()


    def _header_creator(self, header: str) -> ft.Container:
        """
        Creates a header for the table

        Parameters:
            - :param:`header` (str): The text to be displayed in the header.

        Returns:
            - :return:`header_content` (ft.Container): The header for the table.
        """

        return ft.Container(
            width = styles["table"]["cell_width"],
            alignment = ft.alignment.center,
            content = ft.Text(
                header,
                font_family = styles["table"]["font"],
                size = styles["table"]["font_size_header"],
                color = styles["table"]["color"],
                weight = ft.FontWeight.BOLD,
                text_align = ft.TextAlign.CENTER
            )
        )


    def _cell_creator(self, data: str) -> ft.Container:
        """
        Create a cell for the table

        Parameters:
            - :param:`data` (str): The data to be displayed in the cell.

        Returns:
            - :return:`cell_content` (ft.Container): The cell for the table.
        """

        return ft.Container(
            width = styles["table"]["cell_width"],
            alignment = ft.alignment.center,
            content = ft.Text(
                data,
                font_family = styles["table"]["font"],
                size = styles["table"]["font_size_content"],
                color = styles["table"]["color"],
                weight = ft.FontWeight.W_300,
                text_align = ft.TextAlign.CENTER
            )
        )


    def _row_creator(self, line: list[str]) -> ft.Container:
        """
        Create a row for the table

        Parameters:
            - :param:`line` (list[str]): The line of data to be displayed in the row.

        Returns:
            - :return:`row_content` (ft.Container): The row for the table.
        """

        row: ft.Container = ft.Container(
            border = ft.border.only(
                bottom = ft.BorderSide(1, styles["table"]["border_color"])
            ),
            animate = ft.animation.Animation(250, ft.AnimationCurve.EASE_IN_OUT),
            alignment = ft.alignment.center,
            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                controls = [
                    self._cell_creator(cell) for cell in line
                ]
            ),
            on_hover = lambda _: self._row_on_hover(_, row)
        )

        return row


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


    def last_data_batch_table(self) -> ft.Container:
        """
        Table with the last data batch from the local database.

        Parameters:
            - :param:`page` (ft.Page): The page where the table will be displayed.

        Returns:
            - :return:`table_content` (ft.Container): Table with the last data batch from the local database.
        """

        headers: ft.Container = ft.Container(
            height = styles["table"]["header_height"],
            bgcolor = styles["table"]["bgcolor_header"],
            alignment = ft.alignment.center,
            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                controls = [
                    self._header_creator(header) for header in [
                        "ID", "Batch #", "Device #", "Date", "Time",
                        "X-Coord.", "Y-Coord.", "Temp.", "Humidity", "Light Perc."
                    ]
                ]
            )
        )

        # Get the last data batch from the local database
        batch: list[tuple[str]] = local_db_connection.get_last_data_batch()

        # List of data rows in the table
        data_rows: list[ft.Container] = [
            self._row_creator(list(line)) for line in batch
        ]

        # Table containing the data batch
        table: ft.Container = ft.Container(
            border = ft.border.all(3, styles["table"]["border_color"]),
            border_radius = styles["table"]["border_radius"],
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                spacing = 0,
                controls = [
                    headers,
                    ft.ListView(
                        controls = data_rows
                    )
                ]
            )
        )

        return table
