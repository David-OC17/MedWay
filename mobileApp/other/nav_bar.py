
import flet as ft

from styles.styles import Styles
from views.router import Router


# Style properties for the navigation bar
styles: dict[str] = Styles.nav_bar_styles()


class NavBar:
    """
    Properties of navigation bar used in the application.
    """

    def navigation_bar(router: Router) -> ft.NavigationBar:
        """
        Navigation bar of the application.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`navigation_bar` (ft.NavigationBar): Navigation bar of the application.
        """

        navigation_bar: ft.NavigationBar = ft.NavigationBar(
            bgcolor = styles["nav_bar"]["bgcolor"],
            destinations = [
                # Home page button
                ft.NavigationDestination(
                    label = "Home",
                    icon = ft.icons.HOME_OUTLINED,
                    selected_icon = ft.icons.HOME,
                ),
                # Daily reports page button
                ft.NavigationDestination(
                    label = "Daily Rep.",
                    icon = ft.icons.DESCRIPTION_OUTLINED,
                    selected_icon = ft.icons.DESCRIPTION,
                ),
                # Monthly reports page button
                ft.NavigationDestination(
                    label = "Monthly Rep.",
                    icon = ft.icons.COLLECTIONS_BOOKMARK_OUTLINED,
                    selected_icon = ft.icons.COLLECTIONS_BOOKMARK,
                ),
                # Analytics page button
                ft.NavigationDestination(
                    label = "Analytics",
                    icon = ft.icons.QUERY_STATS,
                ),
            ],
            on_change = lambda _: router.redirect_to_page(_, _.control.selected_index)
        )

        return navigation_bar
