from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional

class AnsiCodes(Enum):
    """ANSI escape codes for text styling"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKE = '\033[9m'

@dataclass
class ColorCode:
    foreground: str
    background: str

class BasicColors:
    """Basic 8-bit colors"""
    BLACK = ColorCode('\033[30m', '\033[40m')
    RED = ColorCode('\033[31m', '\033[41m')
    GREEN = ColorCode('\033[32m', '\033[42m')
    YELLOW = ColorCode('\033[33m', '\033[43m')
    BLUE = ColorCode('\033[34m', '\033[44m')
    MAGENTA = ColorCode('\033[35m', '\033[45m')
    CYAN = ColorCode('\033[36m', '\033[46m')
    WHITE = ColorCode('\033[37m', '\033[47m')
    
    # Bright variants
    BRIGHT_BLACK = ColorCode('\033[90m', '\033[100m')
    BRIGHT_RED = ColorCode('\033[91m', '\033[101m')
    BRIGHT_GREEN = ColorCode('\033[92m', '\033[102m')
    BRIGHT_YELLOW = ColorCode('\033[93m', '\033[103m')
    BRIGHT_BLUE = ColorCode('\033[94m', '\033[104m')
    BRIGHT_MAGENTA = ColorCode('\033[95m', '\033[105m')
    BRIGHT_CYAN = ColorCode('\033[96m', '\033[106m')
    BRIGHT_WHITE = ColorCode('\033[97m', '\033[107m')

def get_256_color(code: int, background: bool = False) -> str:
    """Generate ANSI code for 256-color mode"""
    if not 0 <= code <= 255:
        raise ValueError("Color code must be between 0 and 255")
    return f'\033[{48 if background else 38};5;{code}m'

def get_rgb_color(r: int, g: int, b: int, background: bool = False) -> str:
    """Generate ANSI code for RGB color"""
    if not all(0 <= x <= 255 for x in (r, g, b)):
        raise ValueError("RGB values must be between 0 and 255")
    return f'\033[{48 if background else 38};2;{r};{g};{b}m' 