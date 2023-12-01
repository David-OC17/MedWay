
import flet as ft

from styles.styles import Styles
from other.file_card import FileCard
from other.s3_connection import S3Connection


# Style properties for the week reports page
styles: dict[str] = Styles.daily_reports_styles()

# Connection to the S3 bucket
s3_connection: S3Connection = S3Connection()


class SDailyReports:
    """
    Properties of the controls used by the function :function:`DailyReports`
    from the :file:`daily_reports.py` for creating the week reports page.
    """


    def title() -> ft.Container:
        """
        Title of the week reports page.
        
        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`title_content` (ft.Container): Title of the week reports page.
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

        # Title of the daily reports page
        title: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    ft.Text(
                        "Daily Reports",
                        font_family = styles["title"]["font"],
                        size = styles["title"]["size"],
                        color = styles["title"]["color"],
                        weight = ft.FontWeight.BOLD,
                        text_align = ft.TextAlign.CENTER
                    )
                ]
            )
        )

        # Content for the company name and the title of the daily reports page
        title_content: ft.Container = ft.Container(
            height = styles["title"]["height"],
            alignment = ft.alignment.center,
            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    # Name of the company
                    company_name,
                    # Title of the daily reports page
                    title
                ]
            )
        )

        return title_content


    def daily_reports(self, page: ft.Page) -> ft.Container:
        """
        File grid containing the daily reports.

        Parameters:
            - page (ft.Page): The page where the file grid will be placed.

        Returns:
            - :return:`daily_reports` (ft.Container): File grid containing the daily reports.
        """

        # File counter
        _counter: int = 0

        # List view for the rows of the file grid
        _list_view: ft.ListView = ft.ListView(
            spacing = styles["file_grid"]["spacing"],
            padding = styles["file_grid"]["padding"],
            height = styles["file_grid"]["height"],
        )

        # Get the file names from the S3 bucket
        files: list[str] = s3_connection.get_file_names("daily")

        # Cards for the files are added to the list view
        for row in range((len(files) // 4) + 1):
            list_row: ft.Row = ft.Row(spacing = styles["file_grid"]["row_spacing"])
            for file in range(4):
                # Prevents to raise an error if the the last row isn't complete
                try:
                    file_card: ft.Container = FileCard().build_file_card(page, files[_counter], "daily")
                    list_row.controls.append(file_card)
                    _counter += 1
                except IndexError:
                    break

            _list_view.controls.append(list_row)

        # The list view is added to a container to create the file grid
        daily_reports_content: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = _list_view
        )

        return daily_reports_content
