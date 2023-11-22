
class Styles:
    """
    Contains the styles for the web app.
    """

    def nav_bar_styles() -> dict[str]:
        """
        Styles for the navigation bar.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`nav_bar_styles_dict` (dict[str]): The styles for the navigation bar.
        """

        nav_bar_styles_dict: dict[str] = {
            "nav_bar" : {
                "width" : 100,
                "height" : 845,
                "bgcolor" : "#3A3E5F"
            },
            "button" : {
                "width" : 75,
                "height" : 75,
                "border_radius" : 15,
                "bgcolor" : "#3A3E5F",
                "button_color" : "#70D2D6",
                "button_size" : 60,
            }
        }

        return nav_bar_styles_dict


    def home_styles() -> dict[str]:
        """
        Styles for the home page components.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`home_styles_dict` (dict[str]): The styles for the home page components.
        """

        home_styles_dict: dict[str] = {
            "logo" : {
                "title_font" : "Roboto Bold",
                "text_font" : "Arimo",
                "color1" : "#3A3E5F",
                "color2" : "#0BA391",
                "width" : 575,
                "height" : 700,
                "title_size" : 124,
                "text_size" : 75,
            }
        }

        return home_styles_dict


    def daily_reports_styles() -> dict[str]:
        """
        Styles for the daily reports page components.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`week_reports_styles_dict` (dict[str]): The styles for the week reports page components.
        """

        daily_reports_styles_dict: dict[str] = {
            "name": {
                "font" : "Roboto Bold",
                "color1" : "#3A3E5F",
                "color2" : "#0BA391",
                "size" : 70,
            },
            "title" : {
                "font" : "Roboto Bold",
                "color" : "#3A3E5F",
                "size" : 70,
                "height" : 175,
            },
            "file" : {
                "width" : 275,
                "height" : 275,
                "padding" : 25,
                "border_radius" : 25,
                "font" : "Arimo",
                "color" : "#000000",
                "bgcolor" : "#70D2D6",
                "font_size" : 20,
            },
            "file_grid" : {
                "spacing" : 20,
                "row_spacing" : 110,
                "padding" : 15,
                "height" : 600
            }
        }

        return daily_reports_styles_dict


    def monthly_reports_styles() -> dict[str]:
        """
        Styles for the monthly reports page components.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`general_reports_styles_dict` (dict[str]): The styles for the general reports page components.
        """

        monthly_reports_styles_dict: dict[str] = {
            "name": {
                "font" : "Roboto Bold",
                "color1" : "#3A3E5F",
                "color2" : "#0BA391",
                "size" : 70,
            },
            "title" : {
                "font" : "Roboto Bold",
                "color" : "#3A3E5F",
                "size" : 70,
                "height" : 175,
            }
        }

        return monthly_reports_styles_dict


    def analytics_styles() -> dict[str]:
        """
        Styles for the analytics page components.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`analytics_styles_dict` (dict[str]): The styles for the analytics page components.
        """

        analytics_styles_dict: dict[str] = {
            "name": {
                "font" : "Roboto Bold",
                "color1" : "#3A3E5F",
                "color2" : "#0BA391",
                "size" : 70,
            },
            "title" : {
                "font" : "Roboto Bold",
                "color" : "#3A3E5F",
                "size" : 70,
                "height" : 175,
            }
        }

        return analytics_styles_dict


    def analytics_styles() -> dict[str]:
        """
        Styles for the analytics page components.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`analytics_styles_dict` (dict[str]): The styles for the analytics page components.
        """

        analytics_styles_dict: dict[str] = {
            "name": {
                "font" : "Roboto Bold",
                "color1" : "#3A3E5F",
                "color2" : "#0BA391",
                "size" : 70,
            },
            "title" : {
                "font" : "Roboto Bold",
                "color" : "#3A3E5F",
                "size" : 70,
                "height" : 175,
            }
        }

        return analytics_styles_dict
