from typing import Any, Optional, TextIO, Union, Tuple
import sys
from datetime import datetime

from .platform import platform_manager
from .styles import Style, Color, Background
from .exceptions import StyleError
from .formatting import TextFormatter

class Printer:
    """Базовый класс для печати с поддержкой стилей"""
    
    def __init__(
        self,
        file: TextIO = sys.stdout,
        color: Optional[Union[str, Tuple[int, int, int]]] = None,
        background: Optional[Union[str, Tuple[int, int, int]]] = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        blink: bool = False,
        dim: bool = False,
        prefix: str = "",
        show_time: bool = False,
        style: str = "default",  # default, solid, minimal
        enable_formatting: bool = True
    ):
        self.file = file
        self.color = color
        self.background = background
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.blink = blink
        self.dim = dim
        self.prefix = prefix
        self.show_time = show_time
        self.style = style
        self.enable_formatting = enable_formatting
        
    def _get_color_code(self, color: Union[str, Tuple[int, int, int]], is_background: bool = False) -> str:
        """Получает ANSI-код для цвета"""
        if isinstance(color, str):
            color_class = Background if is_background else Color
            return getattr(color_class, color.upper())
        else:
            r, g, b = color
            if is_background:
                return Background.rgb(r, g, b)
            return Color.rgb(r, g, b)
    
    def _get_style_sequence(self) -> str:
        """Формирует последовательность ANSI-кодов для всех стилей"""
        codes = []
        
        if self.color:
            try:
                codes.append(self._get_color_code(self.color))
            except (AttributeError, ValueError) as e:
                raise StyleError(f"Некорректный цвет текста: {self.color}") from e
                
        if self.background:
            try:
                codes.append(self._get_color_code(self.background, is_background=True))
            except (AttributeError, ValueError) as e:
                raise StyleError(f"Некорректный цвет фона: {self.background}") from e
        
        if self.bold:
            codes.append(Style.BOLD)
        if self.italic:
            codes.append(Style.ITALIC)
        if self.underline:
            codes.append(Style.UNDERLINE)
        if self.blink:
            codes.append(Style.BLINK)
        if self.dim:
            codes.append(Style.DIM)
            
        return ''.join(codes)
    
    def _format_prefix(self, prefix: str) -> str:
        """Форматирует префикс в соответствии с выбранным стилем"""
        if self.style == "solid":
            return f" {prefix} "
        elif self.style == "minimal":
            return f"● {prefix.strip('[]')} ●"
        return prefix
    
    def _format_text(self, text: str) -> str:
        """Применяет форматирование к тексту, если оно включено"""
        if self.enable_formatting:
            return TextFormatter.format(text)
        return text
    
    def __call__(self, *values: Any, sep: str = ' ', end: str = '\n', flush: bool = False, file: Optional[TextIO] = None) -> None:
        """Печатает текст с применением стилей"""
        platform_manager.init()
        
        output_file = file if file is not None else self.file
        
        if not platform_manager.supports_color():
            text = sep.join(str(value) for value in values)
            if self.enable_formatting:
                text = TextFormatter.strip_formatting(text)
            
            if self.prefix:
                time_str = f"[{datetime.now().strftime('%H:%M:%S')}] " if self.show_time else ""
                formatted_prefix = self._format_prefix(self.prefix)
                text = f"{time_str}{formatted_prefix} {text}"
                
            print(text, end=end, file=output_file, flush=flush)
            return
            
        style_sequence = self._get_style_sequence()
        text = sep.join(str(value) for value in values)
        
        # Применяем форматирование к тексту
        text = self._format_text(text)
        
        if self.prefix or self.show_time:
            time_str = f"[{datetime.now().strftime('%H:%M:%S')}] " if self.show_time else ""
            formatted_prefix = self._format_prefix(self.prefix) if self.prefix else ""
            text = f"{time_str}{formatted_prefix} {text}"
            
        if style_sequence:
            print(f"{style_sequence}{text}{Style.RESET}", end=end, file=output_file, flush=flush)
        else:
            print(text, end=end, file=output_file, flush=flush)

class BPrinter:
    """Главный класс для удобного доступа к различным типам вывода"""
    
    def __init__(self, show_time: bool = True, style: str = "default"):
        self.show_time = show_time
        self.style = style
        self._setup_printers()
    
    def _setup_printers(self):
        """Инициализация всех принтеров"""
        self.print = Printer()
        
        # Стандартные принтеры
        self.success = Printer(
            color="white",
            background="green",
            bold=True,
            prefix="[SUCCESS]",
            show_time=self.show_time,
            style=self.style
        )
        
        self.error = Printer(
            color="white",
            background="red",
            bold=True,
            prefix="[ERROR]",
            show_time=self.show_time,
            style=self.style
        )
        
        self.warning = Printer(
            color="black",
            background="yellow",
            bold=True,
            prefix="[WARNING]",
            show_time=self.show_time,
            style=self.style
        )
        
        self.info = Printer(
            color="white",
            background="blue",
            prefix="[INFO]",
            show_time=self.show_time,
            style=self.style
        )
        
        self.debug = Printer(
            color="white",
            background="magenta",
            dim=True,
            prefix="[DEBUG]",
            show_time=self.show_time,
            style=self.style
        )
        
        # Дополнительные принтеры
        self.critical = Printer(
            color="white",
            background="red",
            bold=True,
            blink=True,
            prefix="[CRITICAL]",
            show_time=self.show_time,
            style=self.style
        )
        
        self.system = Printer(
            color="black",
            background="cyan",
            bold=True,
            prefix="[SYSTEM]",
            show_time=self.show_time,
            style=self.style
        )
        
        self.done = Printer(
            color="black",
            background="bright_green",
            bold=True,
            prefix="[DONE]",
            show_time=self.show_time,
            style=self.style
        )
    
    def custom(
        self,
        prefix: str,
        color: Optional[Union[str, Tuple[int, int, int]]] = None,
        background: Optional[Union[str, Tuple[int, int, int]]] = None,
        file: TextIO = sys.stdout,
        **kwargs
    ) -> Printer:
        """Создает пользовательский принтер с указанным префиксом и стилем"""
        return Printer(
            prefix=f"[{prefix.upper()}]",
            color=color,
            background=background,
            file=file,
            show_time=self.show_time,
            style=self.style,
            **kwargs
        )

# Создаем глобальные экземпляры с разными стилями
bprinter = BPrinter(style="default")  # Стандартный стиль: [PREFIX]
bprinter_solid = BPrinter(style="solid")  # Сплошной фон:  PREFIX 
bprinter_minimal = BPrinter(style="minimal")  # Минималистичный: ● PREFIX ● 