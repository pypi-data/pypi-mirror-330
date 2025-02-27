from typing import Optional, List
import pyfiglet
from .styles import Style, Color, Background

class ASCIIArtGenerator:
    """Класс для генерации ASCII арта из текста"""
    
    @staticmethod
    def get_available_fonts() -> List[str]:
        """Возвращает список доступных шрифтов"""
        return pyfiglet.FigletFont.getFonts()
    
    @staticmethod
    def render(
        text: str,
        font: str = "standard",
        color: Optional[str] = None,
        background: Optional[str] = None,
        width: int = 80
    ) -> str:
        """
        Создает ASCII арт из текста
        
        Args:
            text: Текст для преобразования
            font: Шрифт (используйте get_available_fonts() для списка)
            color: Цвет текста
            background: Цвет фона
            width: Максимальная ширина
            
        Returns:
            str: ASCII арт
        """
        try:
            f = pyfiglet.Figlet(font=font, width=width)
            ascii_art = f.renderText(text)
            
            if color or background:
                style_sequence = ""
                if color:
                    style_sequence += getattr(Color, color.upper(), "")
                if background:
                    style_sequence += getattr(Background, background.upper(), "")
                    
                if style_sequence:
                    ascii_art = style_sequence + ascii_art + Style.RESET
                    
            return ascii_art
            
        except pyfiglet.FigletError as e:
            raise ValueError(f"Ошибка при создании ASCII арта: {str(e)}")
            
    @staticmethod
    def preview_fonts(text: str, fonts: Optional[List[str]] = None) -> str:
        """
        Показывает предпросмотр текста разными шрифтами
        
        Args:
            text: Текст для предпросмотра
            fonts: Список шрифтов (если None, используются популярные шрифты)
            
        Returns:
            str: Предпросмотр текста разными шрифтами
        """
        if fonts is None:
            fonts = ["standard", "banner", "big", "block", "bubble", 
                    "digital", "ivrit", "mini", "script", "shadow"]
            
        result = []
        for font in fonts:
            try:
                art = ASCIIArtGenerator.render(text, font=font)
                result.append(f"Font: {font}\n{art}\n")
            except ValueError:
                continue
                
        return "\n".join(result) 