import os

os.system("")
"""_A tiny terminal text color-er._
"""

def clear() -> None:
    """_Clears the screen._"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


B = "\033[30m"  # Black text.
R = "\033[31m"  # Red text.
G = "\033[32m"  # Green text.
Y = "\033[33m"  # Yellow text.
B = "\033[34m"  # Blue text.
M = "\033[35m"  # Magenta text.
C = "\033[36m"  # Cyan text.
W = "\033[37m"  # White text.
UNDERLINE = "\033[4m"  # Underlines.
DOUBLE_UNDERLINE = "\033[21m"  # Double underlines.
CURLY_UNDERLINE = "\033[4:3m"  # Curly underlines.
BLINK = "\033[5m"  # Blinks the text.
REVERSE = "\033[7m"  # Reverses the text.
HIDDEN = "\033[8m"  # Hides the text.
STRIKETHROUGH = "\033[9m"  # Strikes the text through.
OVERLINE = "\033[53m"  # Overlines the text.
BOLD = "\033[1m"  # Bolds.
DIM = "\033[2m"  # Dims.
ITALIC = "\033[3m"  # Italicizes.
RESET = "\033[0m"  # Resets the formatting.
