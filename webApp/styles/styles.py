
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
