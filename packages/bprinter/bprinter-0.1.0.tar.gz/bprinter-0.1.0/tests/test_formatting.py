import pytest
from bprinter.formatting import TextFormatter
from bprinter.styles import Style, Color

def test_bold_formatting():
    """Тест форматирования жирного текста"""
    text = "This is **bold** text"
    formatted = TextFormatter.format(text)
    assert Style.BOLD in formatted
    assert Style.RESET in formatted

def test_italic_formatting():
    """Тест форматирования курсивного текста"""
    text = "This is _italic_ text"
    formatted = TextFormatter.format(text)
    assert Style.ITALIC in formatted
    assert Style.RESET in formatted

def test_underline_formatting():
    """Тест форматирования подчеркнутого текста"""
    text = "This is __underlined__ text"
    formatted = TextFormatter.format(text)
    assert Style.UNDERLINE in formatted
    assert Style.RESET in formatted

def test_strike_formatting():
    """Тест форматирования зачеркнутого текста"""
    text = "This is ~~striked~~ text"
    formatted = TextFormatter.format(text)
    assert Style.STRIKE in formatted
    assert Style.RESET in formatted

def test_link_formatting():
    """Тест форматирования ссылок"""
    text = "Visit [our site](https://example.com)"
    formatted = TextFormatter.format(text)
    assert Style.UNDERLINE in formatted
    assert Color.BLUE in formatted
    assert Color.CYAN in formatted
    assert "our site" in formatted
    assert "https://example.com" in formatted

def test_code_formatting():
    """Тест форматирования кода"""
    text = "Use `pip install` command"
    formatted = TextFormatter.format(text)
    assert Style.DIM in formatted
    assert Color.MAGENTA in formatted
    assert "pip install" in formatted

def test_color_formatting():
    """Тест форматирования цветного текста"""
    text = "This is {red|colored} text"
    formatted = TextFormatter.format(text)
    assert Color.RED in formatted
    assert "colored" in formatted

def test_combined_formatting():
    """Тест комбинированного форматирования"""
    text = "**Bold _and italic_** with `code` and {green|color}"
    formatted = TextFormatter.format(text)
    assert Style.BOLD in formatted
    assert Style.ITALIC in formatted
    assert Style.DIM in formatted
    assert Color.MAGENTA in formatted
    assert Color.GREEN in formatted

def test_strip_formatting():
    """Тест удаления форматирования"""
    text = "**Bold** _italic_ ~~strike~~ `code` {red|color} [link](url)"
    stripped = TextFormatter.strip_formatting(text)
    assert "**" not in stripped
    assert "_" not in stripped
    assert "~~" not in stripped
    assert "`" not in stripped
    assert "{red|" not in stripped
    assert "[link]" not in stripped
    assert "(url)" not in stripped
    assert "Bold italic strike code color link" == stripped.strip()

def test_invalid_color():
    """Тест обработки некорректного цвета"""
    text = "{invalid_color|text}"
    formatted = TextFormatter.format(text)
    assert "text" in formatted  # Текст должен остаться, даже если цвет некорректный

def test_nested_formatting():
    """Тест вложенного форматирования"""
    text = "**Bold _italic_ text**"
    formatted = TextFormatter.format(text)
    assert Style.BOLD in formatted
    assert Style.ITALIC in formatted
    assert formatted.count(Style.RESET) >= 2  # Должно быть как минимум 2 сброса стиля 