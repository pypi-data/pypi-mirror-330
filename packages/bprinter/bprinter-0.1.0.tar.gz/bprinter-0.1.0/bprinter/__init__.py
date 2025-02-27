"""
BPrinter - Мощная кросс-платформенная библиотека для стилизации текста в терминале
"""

from typing import Optional

from .styles import Style, Color, Background
from .exceptions import BPrinterError, ColorError, PlatformError, StyleError
from .platform import platform_manager
from .printer import BPrinter, bprinter, bprinter_solid, bprinter_minimal, Printer
from .formatting import TextFormatter
from .ascii_art import ASCIIArtGenerator

__version__ = "0.1.0"

def init(
    strip: Optional[bool] = None,
    convert: Optional[bool] = None,
    wrap: Optional[bool] = None,
    autoreset: bool = False
) -> None:
    """
    Инициализация библиотеки
    
    Args:
        strip: Отключить цветной вывод
        convert: Конвертировать новые строки (CRLF -> LF)
        wrap: Обернуть стандартные потоки
        autoreset: Автоматически сбрасывать стиль после каждого вывода
    """
    platform_manager.init(
        strip=strip,
        convert=convert,
        wrap=wrap,
        autoreset=autoreset
    )

__all__ = [
    'Style',
    'Color',
    'Background',
    'BPrinterError',
    'ColorError',
    'PlatformError',
    'StyleError',
    'BPrinter',
    'bprinter',
    'bprinter_solid',
    'bprinter_minimal',
    'Printer',
    'TextFormatter',
    'ASCIIArtGenerator',
    'init',
]

# Инициализация с настройками по умолчанию
init()
