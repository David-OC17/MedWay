
import flet as ft

from views.home import Home
from views.daily_reports import DailyReports
from views.month_reports import MonthReports
from views.analytics import Analytics


class Router:
    """
    Contains all the methods for redirecting the user to different pages, through
    the app's navigation bar.
    """

    def __init__(self, page: ft.Page, date_time: ft.Text) -> None:
        self.page: ft.Page = page
        self.date_time: ft.Text = date_time
        self.routes: dict[str, ft.Column] = {
            "/" : Home(page, date_time),                # Home page
            "/daily_reports" : DailyReports(page),      # Daily reports page
            "/monthly_reports" : MonthReports(page),    # Monthly reports page
            "/analytics" : Analytics(page),             # Analytics page
        }
        # Default route and page to be displayed
        self.view: ft.Container = ft.Container(
            content = self.routes["/"],
            expand = True
        )


    def route_change(self, route: str) -> None:
        """
        Changes the current view of the app, based on the route passed in.

        - Parameters:
            - route (str): The route to change to.
        
        - Returns:
            - No return value.
        """

        self.view.content = self.routes[route.route]
        self.page.update()


    def redirect_to_page(self, _: ft.ControlEvent, selected_index: int) -> None:
        """
        Redirects the user to the selected page.

        - Parameters:
            - :param:`_` (ft.ControlEvent): The click event.
            - :param:`selected_index` (int): The index of the selected page.

        - Returns:
            - No return value.
        """

        route_indices: dict[int, str] = {
            0 : "/",
            1 : "/daily_reports",
            2 : "/monthly_reports",
            3 : "/analytics"
        }

        self.page.go(route_indices[selected_index])
