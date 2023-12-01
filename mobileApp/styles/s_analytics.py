
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

    def _refresh_button_on_click(self, _: ft.ControlEvent, page: ft.Page) -> None:
        """
        Refreshes the table with the last data batch from the local database.

        Parameters:
            - :param:`_` (ft.ControlEvent): The event that triggers the function.
            - :param:`page` (ft.Page): The page the data will be refreshed in.

        Returns:
            - Doesn't return anything.
        """

        # Refresh the table with the last data batch from the local database
        page.controls[0].content.controls[0].content.controls[1].content.controls[0] = self.last_data_batch_table()

        # Update the table in the page
        page.update()


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
            animate = ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_OUT),
            alignment = ft.alignment.center,
            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_AROUND,
                controls = [
                    self._cell_creator(cell) for cell in line
                ]
            )
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
            offset = ft.Offset(0, 0.2),
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
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
            - Doesn't take any parameters.

        Returns:
            - :return:`table_content` (ft.Container): Table with the last data batch from the local database.
        """

        # Create the list of the data rows, and ajust the border radius of the last row to avoid rendering issues
        data_rows: list[ft.Container] = [
            self._row_creator(list(line)) for line in local_db_connection.get_last_data_batch()
        ]
        data_rows[-1].border_radius = ft.border_radius.vertical(
            top = 0, bottom = styles["table"]["border_radius_adjusted"]
        )

        # Insert the headers in the table in a container
        _headers: ft.Container = ft.Container(
            height = styles["table"]["header_height"],
            bgcolor = styles["table"]["bgcolor_header"],
            border_radius = ft.border_radius.vertical(
                top = styles["table"]["border_radius_adjusted"], bottom = 0
            ),
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

        # Insert the data rows in the table in a separate list view object
        _table_data: ft.Container = ft.Container(
            expand = True,
            alignment = ft.alignment.top_center,
            content = ft.ListView(
                width = styles["table"]["cell_width"] * 10,
                height = min(
                    # If the table surpasses the maximum height, set the height of the table 
                    # to the maximum height
                    styles["table"]["max_height"],
                    # Otherwise, set the height of the table to depending on the number of rows
                    # in the table
                    len(data_rows) * styles["table"]["header_height"]
                ),
                spacing = 0,
                controls = data_rows
            )
        )

        table_content: ft.Container = ft.Container(
            height = min(
                # If the table surpasses the maximum height, set the height of the table 
                # to the maximum height
                styles["table"]["max_height"],
                # Otherwise, set the height of the table to depending on the number of rows
                # in the table
                len(data_rows) * styles["table"]["header_height"]
            ),
            alignment = ft.alignment.top_center,
            border = ft.border.all(3, styles["table"]["border_color"]),
            border_radius = styles["table"]["border_radius"],
            content = ft.Row(
                scroll = True,
                spacing = 0, 
                controls = [
                    ft.Container(
                        content = ft.Column(
                            spacing = 0,
                            controls = [
                                # Headers of the table
                                _headers,
                                # Data of the table
                                _table_data
                            ]
                        )
                    )
                ]
            )
        )

        return table_content


    def refresh_button(self, page: ft.Page) -> ft.FloatingActionButton:
        """
        Button for refreshing the table with the last data batch from the local database.

        Parameters:
            - :param:`page` (ft.Page): The page the data will be refreshed in.

        Returns:
            - :return:`refresh_button` (ft.FloatingActionButton): Button for refreshing the
            table with the last data batch from the local database.
        """

        # Button for refreshing the table with the last data batch from the local database
        refresh_button: ft.FloatingActionButton = ft.FloatingActionButton(
            icon = ft.icons.REFRESH,
            bgcolor = styles["refresh_button"]["bgcolor"],
            tooltip = "Refresh the table with the last data batch from the local database",
            on_click = lambda _: self._refresh_button_on_click(_, page)
        )

        return refresh_button
