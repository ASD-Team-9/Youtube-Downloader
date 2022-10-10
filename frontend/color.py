#Dictionary of the project's colour palette.
THEME = "Default"
COLOURS: dict[str, dict[str, (str, str)]] = {
    "Mode": { #DO NOT USE BUT FOLLOW.
        "Example": ("#LightMode", "#DarkMode"),
    },

    "Default": {
        "Normal": "#33363B",
        "Normal2": "#292b2f",
        "Dark": "#202225",
        "ButtonNormal": "#36393f",
        "ButtonHover": "#5865f2",
        "ButtonHover2": "#3ba55d",
        "Text": "#b9bbbe",
    },
}
def get_colour(palette_name: str):
    "Simplifies the process of getting the colour."
    return COLOURS[THEME][palette_name]