import pyglet, os, sys

BACKGROUND_COLOR = "#D9D9D9"
WHITE_COLOUR = "#FFFFFF"
RED_COLOUR = "#CD2E3A"
BLUE_COLOUR = "#0047A0"
BLACK_COLOUR = "#000000"
ENGLISH_FONT = "Noto Sans"
KOREAN_FONT = "Noto Sans Korean"

# ---------------------------- RESOURCE PATH ------------------------------- #
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ---------------------------- FONT ------------------------------- #
pyglet.options["win32_gdi_font"] = True
english_font_path = resource_path("assets/fonts/NotoSans-VariableFont_wdth,wght.ttf")
korean_font_path = resource_path("assets/fonts/NotoSansKR-VariableFont_wght.ttf")
pyglet.font.add_file(english_font_path)
pyglet.font.add_file(korean_font_path)