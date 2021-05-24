#GUI CONFIGURATION

SIZE = 400
GRID_LEN = 4
GRID_PADDING = 10
SQUARE_SIDE = 100

BACKGROUND_COLOR_APP = '#000000'
#BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_GAME = '#313131'
#BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_CELL_EMPTY = '#d9d9d9'
"""
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e",

                         4096: "#eee4da", 8192: "#edc22e", 16384: "#f2b179",
                         32768: "#f59563", 65536: "#f67c5f", }
"""
BACKGROUND_COLOR_DICT = {2: "#FFFF00", 4: "#FF0000", 8: "#FF00FF",
                         16: "#9900FF", 32: "#f67c5f", 64: "#00FFFF",
                         128: "#00FF00", 256: "#ee8e3b", 512: "#2643ff",
                         1024: "#edc53f", 2048: "#edc22e",
                         #8192 and up are unchanged from original colors

                         4096: "#bef029", 8192: "#edc22e", 16384: "#f2b179",
                         32768: "#f59563", 65536: "#f67c5f", }

"""
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2",
                   256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2",
                   2048: "#f9f6f2",

                   4096: "#776e65", 8192: "#f9f6f2", 16384: "#776e65",
                   32768: "#776e65", 65536: "#f9f6f2", }
"""
CELL_COLOR_DICT = {2: "#000000", 4: "#FFFFFF", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#000000", 64: "#000000", 128: "#000000",
                   256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2",
                   2048: "#f9f6f2",

                   4096: "#776e65", 8192: "#f9f6f2", 16384: "#776e65",
                   32768: "#776e65", 65536: "#f9f6f2", }
FONT = ("Verdana", 30, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"
KEY_BACK = "'b'"

KEY_J = "'j'"
KEY_K = "'k'"
KEY_L = "'l'"
KEY_H = "'h'"

#DFA GUI CONSTANTS
BUTTON_HEIGHT = 2
WIN_SIZE = W = H =  700


import os
import os.path
from pathlib import Path

#file locations
folderPath = os.path.join(Path.home(),"2048Vision")
filePath = os.path.join(folderPath, "data")

#color tracking
color_presets = {
    "orangeLower": (0, 100, 100),
    "orangeUpper": (25, 255, 255),
    "yellowLower": (0, 70, 190),
    "yellowUpper": (85, 255, 255),
    "blueLower": (90,200, 0),
    "blueUpper": (115, 255, 255),
    "magentaLower": (87 ,132,136),
    "magentaUpper":(179,255,255),
    "greenLower":(40, 80, 80),
    "greenUpper":(100, 255, 171),
}