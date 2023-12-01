
class Styles:
    """
    Contains the styles for the web app.
    """

    def file_card_styles() -> dict[str]:
        """
        Styles for the file cards.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`file_card_styles_dict` (dict[str]): The styles for the file cards.
        """

        file_card_styles_dict: dict[str] = {
            "card" : {
                "height" : 175,
                "padding" : 25,
                "border_radius" : 25,
                "font" : "Arimo",
                "font_size" : 20,
                "color" : "#000000",
                "bgcolor" : "#70D2D6",
                "border_color" : "#F4FF2B"
            },
            "alert" : {
                "font" : "Arimo",
                "font_color" : "#FFFFFF",
                "link_font_color" : "#0099EB",
                "title_font_size" : 25,
                "content_font_size" : 20,
                "border_radius" : 25,
                "button_width" : 200,
                "bgcolor" : "#3A3E5F",
                "border_color" : "#404040",
                "border_radius" : 15,
            }
        }

        return file_card_styles_dict


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
                "bgcolor" : "#34345F"
            },
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
                "width" : 290,
                "height" : 700,
                "title_size" : 60,
                "text_size" : 30,
            }
        }

        return home_styles_dict


    def daily_reports_styles() -> dict[str]:
        """
        Styles for the daily reports page components.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`daily_reports_styles_dict` (dict[str]): The styles for the daily reports page components.
        """

        daily_reports_styles_dict: dict[str] = {
            "title" : {
                "font" : "Roboto Bold",
                "color" : "#3A3E5F",
                "size" : 40,
                "height" : 100,
            },
            "file_list" : {
                "height" : 500,
                "spacing" : 10,
                "row_spacing" : 10,
            }
        }

        return daily_reports_styles_dict


    def monthly_reports_styles() -> dict[str]:
        """
        Styles for the monthly reports page components.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`monthly_reports_styles_dict` (dict[str]): The styles for the monthly reports page components.
        """

        monthly_reports_styles_dict: dict[str] = {
            "title" : {
                "font" : "Roboto Bold",
                "color" : "#3A3E5F",
                "size" : 40,
                "height" : 100,
            },
            "file_list" : {
                "height" : 500,
                "spacing" : 10,
                "row_spacing" : 10,
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
            "title" : {
                "font" : "Roboto Bold",
                "color" : "#3A3E5F",
                "size" : 40,
                "height" : 100,
            },
            "table" : {
                "max_height" : 600,
                "header_height" : 50,
                "cell_width" : 125,
                "font" : "Arimo",
                "font_size_header" : 25,
                "font_size_content" : 20,
                "color" : "#3A3E5F",
                "bgcolor" : "#FFFFFF",
                "bgcolor_header" : "#8FF0D5",
                "bgcolor_hovered" : "#A7ECF4",
                "border_color" : "#3A3E5F",
                "horizontal_line_color" : "#3A3E5F",
                "border_radius" : 25,
                "border_radius_adjusted" : 20,
            },
            "refresh_button" : {
                "bgcolor" : "#0BA391",
                "icon_color" : "#3A3E5F",
            }
        }

        return analytics_styles_dict
