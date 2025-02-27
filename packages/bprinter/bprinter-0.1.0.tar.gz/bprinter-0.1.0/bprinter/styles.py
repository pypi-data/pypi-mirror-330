from contextlib import contextmanager
from typing import Generator, Union, Tuple

from .constants import AnsiCodes, BasicColors, get_256_color, get_rgb_color
from .platform import platform_manager

class Style:
    """Основной класс для стилизации текста"""
    
    # Статические свойства для базовых стилей
    RESET = AnsiCodes.RESET.value
    BOLD = AnsiCodes.BOLD.value
    DIM = AnsiCodes.DIM.value
    ITALIC = AnsiCodes.ITALIC.value
    UNDERLINE = AnsiCodes.UNDERLINE.value
    BLINK = AnsiCodes.BLINK.value
    REVERSE = AnsiCodes.REVERSE.value
    HIDDEN = AnsiCodes.HIDDEN.value
    STRIKE = AnsiCodes.STRIKE.value
    
    @classmethod
    @contextmanager
    def styled(cls, *styles: str) -> Generator[None, None, None]:
        """Контекстный менеджер для применения нескольких стилей"""
        platform_manager.init()
        if not platform_manager.supports_color():
            yield
            return
            
        print(''.join(styles), end='')
        yield
        print(cls.RESET, end='')
    
    @classmethod
    @contextmanager
    def color(cls, color: Union[str, Tuple[int, int, int]]) -> Generator[None, None, None]:
        """Контекстный менеджер для применения цвета"""
        platform_manager.init()
        if not platform_manager.supports_color():
            yield
            return
            
        if isinstance(color, str):
            # Используем предопределенный цвет
            color_code = getattr(Color, color.upper(), None)
            if color_code is None:
                raise ValueError(f"Unknown color: {color}")
            print(color_code, end='')
        else:
            # Используем RGB
            r, g, b = color
            print(get_rgb_color(r, g, b), end='')
            
        yield
        print(cls.RESET, end='')

class Color:
    """Класс для работы с цветами текста"""
    
    # Базовые цвета
    BLACK = BasicColors.BLACK.foreground
    RED = BasicColors.RED.foreground
    GREEN = BasicColors.GREEN.foreground
    YELLOW = BasicColors.YELLOW.foreground
    BLUE = BasicColors.BLUE.foreground
    MAGENTA = BasicColors.MAGENTA.foreground
    CYAN = BasicColors.CYAN.foreground
    WHITE = BasicColors.WHITE.foreground
    
    # Яркие цвета
    BRIGHT_BLACK = BasicColors.BRIGHT_BLACK.foreground
    BRIGHT_RED = BasicColors.BRIGHT_RED.foreground
    BRIGHT_GREEN = BasicColors.BRIGHT_GREEN.foreground
    BRIGHT_YELLOW = BasicColors.BRIGHT_YELLOW.foreground
    BRIGHT_BLUE = BasicColors.BRIGHT_BLUE.foreground
    BRIGHT_MAGENTA = BasicColors.BRIGHT_MAGENTA.foreground
    BRIGHT_CYAN = BasicColors.BRIGHT_CYAN.foreground
    BRIGHT_WHITE = BasicColors.BRIGHT_WHITE.foreground
    
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """Создает цвет из RGB значений"""
        return get_rgb_color(r, g, b)
    
    @staticmethod
    def code(n: int) -> str:
        """Создает цвет из 256-цветной палитры"""
        return get_256_color(n)

class Background:
    """Класс для работы с цветами фона"""
    
    # Базовые цвета фона
    BLACK = BasicColors.BLACK.background
    RED = BasicColors.RED.background
    GREEN = BasicColors.GREEN.background
    YELLOW = BasicColors.YELLOW.background
    BLUE = BasicColors.BLUE.background
    MAGENTA = BasicColors.MAGENTA.background
    CYAN = BasicColors.CYAN.background
    WHITE = BasicColors.WHITE.background
    
    # Яркие цвета фона
    BRIGHT_BLACK = BasicColors.BRIGHT_BLACK.background
    BRIGHT_RED = BasicColors.BRIGHT_RED.background
    BRIGHT_GREEN = BasicColors.BRIGHT_GREEN.background
    BRIGHT_YELLOW = BasicColors.BRIGHT_YELLOW.background
    BRIGHT_BLUE = BasicColors.BRIGHT_BLUE.background
    BRIGHT_MAGENTA = BasicColors.BRIGHT_MAGENTA.background
    BRIGHT_CYAN = BasicColors.BRIGHT_CYAN.background
    BRIGHT_WHITE = BasicColors.BRIGHT_WHITE.background
    
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """Создает цвет фона из RGB значений"""
        return get_rgb_color(r, g, b, background=True)
    
    @staticmethod
    def code(n: int) -> str:
        """Создает цвет фона из 256-цветной палитры"""
        return get_256_color(n, background=True) 