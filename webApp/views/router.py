
import flet as ft

from views.home import Home
# from views.week_reports import WeekReports
# from views.general_reports import GeneralReports


class Router:
    """
    Contains all the methods for redirecting the user to different pages, through
    the app's navigation bar.
    """

    def __init__(self, page: ft.Page, date_time: ft.Text) -> None:
        self.page: ft.Page = page
        self.date_time: ft.Text = date_time
        self.routes: dict[str, ft.Column] = {
            "/" : Home(page, date_time),
            # "/week_reports" : WeekReports(page),
            # "/general_reports" : GeneralReports(page),
        }
        # Default route and page to be displayed
        self.view: ft.Container = ft.Container(
            border = ft.border.all(1, "#FF0000"),
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
