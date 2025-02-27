import os
import sys
import platform
from contextlib import contextmanager
from typing import Optional, Generator
from io import StringIO

class PlatformManager:
    """Управление платформо-зависимым поведением"""
    
    def __init__(self):
        self._is_windows = platform.system().lower() == 'windows'
        self._original_stdout = None
        self._temp_stdout = None
        self._initialized = False
        self._strip_colors = False
        self._convert_newlines = True
        self._wrap_stdout = True
        self._wrap_stderr = True
    
    @property
    def is_windows(self) -> bool:
        return self._is_windows
    
    @property
    def is_initialized(self) -> bool:
        return self._initialized
        
    @property
    def strip_colors(self) -> bool:
        return self._strip_colors
        
    @property
    def convert_newlines(self) -> bool:
        return self._convert_newlines
        
    def init(
        self,
        strip: Optional[bool] = None,
        convert: Optional[bool] = None,
        wrap: Optional[bool] = None,
        autoreset: bool = False
    ) -> None:
        """
        Инициализация платформо-зависимых настроек
        
        Args:
            strip: Отключить цветной вывод
            convert: Конвертировать новые строки (CRLF -> LF)
            wrap: Обернуть стандартные потоки
            autoreset: Автоматически сбрасывать стиль после каждого вывода
        """
        if self._initialized and strip is None and convert is None and wrap is None:
            return
            
        # Применяем настройки
        if strip is not None:
            self._strip_colors = strip
        if convert is not None:
            self._convert_newlines = convert
        if wrap is not None:
            self._wrap_stdout = wrap
            self._wrap_stderr = wrap
            
        if self.is_windows:
            # Включаем ANSI на Windows
            import ctypes
            kernel32 = ctypes.windll.kernel32
            
            # Получаем handle консоли
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            
            # Получаем текущий режим
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            
            # Включаем VIRTUAL_TERMINAL_PROCESSING
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
            
            # Устанавливаем новый режим
            kernel32.SetConsoleMode(handle, mode)
        
        self._initialized = True
    
    def supports_color(self) -> bool:
        """Проверяет поддержку цвета в текущем терминале"""
        if self._strip_colors:
            return False
            
        if not hasattr(sys.stdout, 'isatty'):
            return False
        
        if not sys.stdout.isatty():
            return bool(os.environ.get('COLORTERM'))
            
        if self.is_windows:
            return True  # После Windows 10 build 14931
            
        if bool(os.environ.get('COLORTERM')):
            return True
            
        term = os.environ.get('TERM', '').lower()
        supported_terms = ('xterm', 'xterm-color', 'xterm-256color', 'linux',
                          'screen', 'screen-256color', 'ansi')
        return term in supported_terms
    
    @contextmanager
    def temp_disable(self) -> Generator[None, None, None]:
        """Временно отключает вывод в консоль"""
        previous_stdout = sys.stdout
        temp_stdout = StringIO()
        sys.stdout = temp_stdout
        try:
            yield
        finally:
            sys.stdout = previous_stdout

# Глобальный экземпляр для использования во всей библиотеке
platform_manager = PlatformManager() 