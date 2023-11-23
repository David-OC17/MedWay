
import flet as ft

from styles.styles import Styles
from other.file_card import FileCard
from other.s3_connection import S3Connection


# Style properties for the week reports page
styles: dict[str] = Styles.monthly_reports_styles()

# Connection to the S3 bucket
s3_connection: S3Connection = S3Connection()


class SMonthReports:
    """
    Properties of the controls used by the function :function:`MonthReports`
    from the :file:`monthly_reports.py` for creating the monthly reports page.
    """

    def title() -> ft.Container:
        """
        Title of the monthly reports page.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`title_content` (ft.Container): Title of the monthly reports page.
        """
        # Title of the monthly reports page
        title: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    ft.Text(
                        "Monthly Reports",
                        font_family = styles["title"]["font"],
                        size = styles["title"]["size"],
                        color = styles["title"]["color"],
                        weight = ft.FontWeight.BOLD,
                        text_align = ft.TextAlign.CENTER
                    )
                ]
            )
        )

        # Container with the title of the monthly reports page
        title_content: ft.Container = ft.Container(
            height = styles["title"]["height"],
            alignment = ft.alignment.center,
            offset = ft.Offset(0, 0.2),
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    # Title of the monthly reports page
                    title
                ]
            )
        )

        return title_content


    def monthly_reports(self, page: ft.Page) -> ft.Container:
        """
        File list containing the monthly reports.

        Parameters:
            - page (ft.Page): Page where the file list is.

        Returns:
            - :return:`monthly_reports_content` (ft.Container): File list of the monthly reports page.
        """

        # List view for the rows of the file list
        _list_view: ft.ListView = ft.ListView(
            spacing = styles["file_list"]["spacing"],
        )

        # Get the files names from the S3 bucket
        files: list[str] = s3_connection.get_file_names("monthly_reports")

        # Cards for the files are added to the list view
        for file in files:
            file_card: ft.Container = FileCard().build_file_card(page, file, "monthly_reports")
            _list_view.controls.append(file_card)

        # The list view is added to a container to create the file list
        monthly_reports_content: ft.Container = ft.Container(
            height = styles["file_list"]["height"],
            expand = True,
            content = _list_view
        )

        return monthly_reports_content
