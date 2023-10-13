
class Styles:
    """
    Contains the styles for the web app.
    """

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
                "font_family" : "Roboto Bold",
                "color1" : "#3A3E5F",
                "color2" : "#0BA391",
                "size" : 70,
            }
        }

        return home_styles_dict
