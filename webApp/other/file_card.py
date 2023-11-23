
import flet as ft
from os.path import expanduser, join
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


    def _card_on_hover(self, _: ft.ControlEvent, card: ft.Container) -> None:
        """
        Illuminates the card's border when the mouse is over it.

        Parameters:
            - _: Control event.
            - card (ft.Container): Card to elevate.

        Returns:
            - Doesn't return anything.
        """

        if _.data == "true":
            card.border = ft.border.all(3, styles["card"]["border_color"])
            card.update()

        else:
            card.border = ft.border.all(0, "#00000000")
            card.update()


    def _card_on_click(self, _: ft.ControlEvent, page: ft.Page, file_name: str, folder: str) -> None:
        """
        Downloads the file from the S3 bucket.

        Parameters:
            - page (ft.Page): Page where the alert is.
            - file_name (str): Name of the file to download.
            - folder (str): Name of the folder where the file is in the S3 bucket.

        Returns:
            - Doesn't return anything.
        """

        alert: ft.AlertDialog = ft.AlertDialog(
            # Alert's dialog
            title = ft.Text(
                font_family = styles["alert"]["font"],
                size = styles["alert"]["title_font_size"],
                color = styles["alert"]["font_color"],
                weight = ft.FontWeight.W_500,
                text_align = ft.TextAlign.CENTER,
            ),
            # Alert's content
            content = ft.Text(
                font_family = styles["alert"]["font"],
                size = styles["alert"]["content_font_size"],
                color = styles["alert"]["font_color"],
                weight = ft.FontWeight.W_300,
                text_align = ft.TextAlign.CENTER,
            ),
            # Button for closing the alert
            actions = [
                ft.Container(
                    width = styles["alert"]["button_width"],
                    border = ft.border.all(1, styles["alert"]["border_color"]),
                    border_radius = ft.border_radius.all(styles["alert"]["border_radius"]),
                    alignment = ft.alignment.center,
                    content = ft.Text(
                        "Close",
                        font_family = styles["alert"]["font"],
                        size = styles["alert"]["content_font_size"],
                        color = styles["alert"]["font_color"],
                        weight = ft.FontWeight.W_300,
                        text_align = ft.TextAlign.CENTER,
                    ),
                    # Close the alert
                    on_click = lambda _: self._close_alert(_, page, alert)
                )
            ],
            # Alignment of the alert's button
            actions_alignment = ft.MainAxisAlignment.CENTER
        )

        # Try downloading the file from the S3 bucket
        try:
            # Get the path to the desktop
            home: str = expanduser("~")
            desktop: str = join(home, "Desktop")
            # Download the file from the S3 bucket
            s3_connection.download(folder, desktop, file_name)
            # Show an alert with the success message
            alert.title.value = "Success"
            alert.content.value = "The file was downloaded successfully to your desktop."
            self._open_alert(page, alert)

        except ClientError as error:
            # Show an alert with the error message
            alert.title.value = "Error"
            alert.content.value = "An unexpected error occurred. Please try again later."
            self._open_alert(page, alert)
            print(error)


    def _open_alert(self, page: ft.Page, alert: ft.AlertDialog) -> None:
        """
        Opens the alert dialog.

        Parameters:
            - _: Control event.
            - page (ft.Page): Page where the alert is.
            - alert (ft.AlertDialog): Alert to open.

        Returns:
            - Doesn't return anything.
        """

        page.dialog = alert
        alert.open = True
        page.update()


    def _close_alert(self, _: ft.ControlEvent, page: ft.Page, alert: ft.AlertDialog) -> None:
        """
        Closes the alert dialog.

        Parameters:
            - _: Control event.
            - page (ft.Page): Page where the alert is.
            - alert (ft.AlertDialog): Alert to close.

        Returns:
            - Doesn't return anything.
        """

        alert.open = False
        page.update()


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
                src = "images/pdf_icon.png",
                fit = ft.ImageFit.CONTAIN,
            )
        )

        # Card for the file
        self.__card: ft.Container = ft.Container(
            width = styles["card"]["width"],
            height = styles["card"]["height"],
            padding = styles["card"]["padding"],
            bgcolor = styles["card"]["bgcolor"],
            animate = ft.animation.Animation(250, ft.AnimationCurve.EASE_IN_OUT),
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
            on_hover = lambda _: self._card_on_hover(_, self.__card),
            on_click = lambda _: self._card_on_click(_, page, file_name, folder)
        )

        return self.__card
