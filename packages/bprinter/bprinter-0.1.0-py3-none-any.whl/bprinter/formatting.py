import re
from typing import Tuple, Dict, List

from .styles import Style, Color

class TextFormatter:
    """Класс для форматирования текста с поддержкой Markdown-подобного синтаксиса"""
    
    # Регулярные выражения для разных типов форматирования
    PATTERNS = {
        'bold': (r'\*\*(.*?)\*\*', lambda m: f"{Style.BOLD}{m.group(1)}{Style.RESET}"),
        'italic': (r'_(.*?)_', lambda m: f"{Style.ITALIC}{m.group(1)}{Style.RESET}"),
        'underline': (r'__(.*?)__', lambda m: f"{Style.UNDERLINE}{m.group(1)}{Style.RESET}"),
        'strike': (r'~~(.*?)~~', lambda m: f"{Style.STRIKE}{m.group(1)}{Style.RESET}"),
        'link': (r'\[(.*?)\]\((.*?)\)', lambda m: f"{Style.UNDERLINE}{Color.BLUE}{m.group(1)}{Style.RESET} ({Color.CYAN}{m.group(2)}{Style.RESET})"),
        'code': (r'`(.*?)`', lambda m: f"{Style.DIM}{Color.MAGENTA}{m.group(1)}{Style.RESET}"),
        'color': (r'\{(.*?)\|(.*?)\}', lambda m: f"{getattr(Color, m.group(1).upper(), '')}{m.group(2)}{Style.RESET}")
    }
    
    @classmethod
    def format(cls, text: str) -> str:
        """Форматирует текст, применяя все поддерживаемые стили"""
        result = text
        
        # Применяем форматирование в определенном порядке
        order = ['underline', 'bold', 'italic', 'strike', 'link', 'code', 'color']
        for style in order:
            pattern, formatter = cls.PATTERNS[style]
            result = re.sub(pattern, formatter, result)
        
        return result
    
    @classmethod
    def strip_formatting(cls, text: str) -> str:
        """Удаляет все форматирование из текста"""
        result = text
        
        for pattern, _ in cls.PATTERNS.values():
            if pattern == cls.PATTERNS['link'][0]:
                result = re.sub(pattern, r'\1', result)
            elif pattern == cls.PATTERNS['color'][0]:
                result = re.sub(pattern, r'\2', result)
            else:
                result = re.sub(pattern, r'\1', result)
        
        return result 