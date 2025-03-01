"""
ABSFUYU CLI
-----------
Color

Version: 5.0.0
Date updated: 22/02/2025 (dd/mm/yyyy)
"""

# Module Package
# ---------------------------------------------------------------------------
__all__ = ["COLOR"]


# Library
# ---------------------------------------------------------------------------
import colorama

# Color
# ---------------------------------------------------------------------------
COLOR = {
    "green": colorama.Fore.LIGHTGREEN_EX,
    "GREEN": colorama.Fore.GREEN,
    "blue": colorama.Fore.LIGHTCYAN_EX,
    "BLUE": colorama.Fore.CYAN,
    "red": colorama.Fore.LIGHTRED_EX,
    "RED": colorama.Fore.RED,
    "yellow": colorama.Fore.LIGHTYELLOW_EX,
    "YELLOW": colorama.Fore.YELLOW,
    "reset": colorama.Fore.RESET,
}
