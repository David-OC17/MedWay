
import flet as ft
from botocore.exceptions import ClientError

from styles.styles import Styles
from other.s3_connection import S3Connection


# Style properties for the file cards
styles: dict[str] = Styles.file_card_styles()

# Connection to the S3 bucket
s3_connection: S3Connection = S3Connection()


class FileCard:
    """
    Properties of the file cards displayed in the daily and monthly reports pages.
    """

    def __init__(self) -> None:
        self.__card = ft.Container()


    def _open_bottom_sheet(self, page: ft.Page, bottom_sheet: ft.BottomSheet) -> None:
        """
        Opens the bottom sheet dialog.

        Parameters:
            - page (ft.Page): Page where the alert is.
            - bottom_sheet (ft.BottomSheet): Bottom sheet to open.

        Returns:
            - Doesn't return anything.
        """

        page.overlay.append(bottom_sheet)
        bottom_sheet.open = True
        page.update()


    def _close_bottom_sheet(self, _: ft.ControlEvent, page: ft.Page, bottom_sheet: ft.BottomSheet, card: ft.Container) -> None:
        """
        Closes the alert dialog.

        Parameters:
            - _: Control event.
            - page (ft.Page): Page where the alert is.
            - bottom_sheet (ft.BottomSheet): Bottom sheet to close.
            - card (ft.Container): Card that was clicked.

        Returns:
            - Doesn't return anything.
        """

        bottom_sheet.open = False
        page.update()

        # Remove the border from the card
        card.border = ft.border.all(0, "#00000000")
        card.update()


    def _card_on_click(self, _: ft.ControlEvent, page: ft.Page, file_name: str, folder: str, card: ft.Container) -> None:
        """
        Downloads the file from the S3 bucket.

        Parameters:
            - page (ft.Page): Page where the alert is.
            - file_name (str): Name of the file to download.
            - folder (str): Name of the folder where the file is in the S3 bucket.
            - card (ft.Container): Card that was clicked.

        Returns:
            - Doesn't return anything.
        """

        # Highlight the card that was clicked
        card.border = ft.border.all(3, styles["card"]["border_color"])
        card.update()

        # Title of the bottom sheet
        _title: ft.Text = ft.Text(
            font_family = styles["alert"]["font"],
            size = styles["alert"]["title_font_size"],
            color = styles["alert"]["font_color"],
            weight = ft.FontWeight.BOLD,
            text_align = ft.TextAlign.CENTER
        )

        # Try to download the file
        try:
            _title.value = "Click on the link below to download the file"
            # Get the download link for the file
            download_link: str = s3_connection.get_download_link(folder, file_name)
            # Content of the bottom sheet
            _content: ft.Text = ft.Text(
                text_align = ft.TextAlign.CENTER,
                spans = [
                    ft.TextSpan(
                        f"Download: {file_name}.pdf",
                        style = ft.TextStyle(
                            font_family = styles["alert"]["font"],
                            size = styles["alert"]["content_font_size"],
                            color = styles["alert"]["link_font_color"],
                            weight = ft.FontWeight.W_300,
                            decoration = ft.TextDecoration.UNDERLINE,
                        ),
                        url = download_link
                    )
                ]
            )

        except ClientError:
            _title.value = "Error"
            # Content of the bottom sheet
            _content: ft.Text = ft.Text(
                "An unexpected error occurred, please try again later.",
                font_family = styles["alert"]["font"],
                size = styles["alert"]["content_font_size"],
                color = styles["alert"]["font_color"],
                weight = ft.FontWeight.W_300,
                text_align = ft.TextAlign.CENTER
            )

        # Bottom sheet to be displayed
        bottom_sheet: ft.BottomSheet = ft.BottomSheet(
            content = ft.Container(
                padding = 10,
                alignment = ft.alignment.center,
                content = ft.Column(
                    tight = True,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    controls = [
                        _title,
                        _content
                    ]
                )
            ),
            on_dismiss = lambda _: self._close_bottom_sheet(_, page, bottom_sheet, card),
        )

        # Open the bottom sheet
        self._open_bottom_sheet(page, bottom_sheet)


    def build_file_card(self, page: ft.Page, file_name: str, folder: str) -> ft.Card:
        """
        Builds a card for a file.

        Parameters:
            - :param:`page` (ft.Page): The page where the card will be placed.
            - :param:`file_name` (str): The name of the file.
            - :param:`folder` (str): The name of the folder where the file is in the S3 bucket.

        Returns:
            - :return:`file_card` (ft.Card): The file card.
        """

        # Name of the file
        file_name_content: ft.Container = ft.Container(
            alignment = ft.alignment.center,
            content = ft.Text(
                file_name,
                font_family = styles["card"]["font"],
                size = styles["card"]["font_size"],
                color = styles["card"]["color"],
                weight = ft.FontWeight.W_300,
                text_align = ft.TextAlign.CENTER
            )
        )

        # Icon for the file
        file_icon: ft.Container = ft.Container(
            expand = True,
            alignment = ft.alignment.center,
            content = ft.Image(
                src = "./images/pdf_icon.png",
                fit = ft.ImageFit.CONTAIN,
            )
        )

        # Card for the file
        self.__card: ft.Container = ft.Container(
            height = styles["card"]["height"],
            padding = styles["card"]["padding"],
            bgcolor = styles["card"]["bgcolor"],
            border_radius = ft.border_radius.all(styles["card"]["border_radius"]),
            alignment = ft.alignment.center,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls = [
                    # Icon for the file
                    file_icon,
                    # Name of the file
                    file_name_content
                ]
            ),
            on_click = lambda _: self._card_on_click(_, page, file_name, folder, self.__card)
        )

        return self.__card
