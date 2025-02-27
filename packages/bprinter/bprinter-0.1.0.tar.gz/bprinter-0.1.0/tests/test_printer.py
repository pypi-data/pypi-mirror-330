import pytest
from io import StringIO
from datetime import datetime
from bprinter.printer import Printer, BPrinter
from bprinter.styles import Style, Color, Background
from bprinter.exceptions import StyleError
from bprinter.platform import platform_manager
from unittest.mock import patch

@pytest.fixture
def string_output():
    """Фикстура для перехвата вывода"""
    return StringIO()

def test_basic_printer(string_output):
    """Тест базового принтера"""
    printer = Printer(file=string_output)
    printer("Hello, World!")
    assert "Hello, World!" in string_output.getvalue()

def test_colored_printer(string_output):
    """Тест цветного принтера"""
    printer = Printer(file=string_output, color="red")
    printer("Error message")
    output = string_output.getvalue()
    assert Color.RED in output
    assert Style.RESET in output
    assert "Error message" in output

def test_styled_printer(string_output):
    """Тест стилизованного принтера"""
    printer = Printer(
        file=string_output,
        color="blue",
        background="white",
        bold=True,
        italic=True
    )
    printer("Styled text")
    output = string_output.getvalue()
    assert Color.BLUE in output
    assert Background.WHITE in output
    assert Style.BOLD in output
    assert Style.ITALIC in output
    assert "Styled text" in output

def test_printer_with_prefix(string_output):
    """Тест принтера с префиксом"""
    printer = Printer(file=string_output, prefix="[TEST]")
    printer("Message")
    assert "[TEST]" in string_output.getvalue()

def test_printer_with_time(string_output):
    """Тест принтера с временной меткой"""
    printer = Printer(file=string_output, show_time=True)
    printer("Message")
    current_hour = datetime.now().strftime("%H")
    assert current_hour in string_output.getvalue()

def test_printer_styles(string_output):
    """Тест разных стилей принтера"""
    # Стандартный стиль
    printer = Printer(file=string_output, prefix="[TEST]", style="default")
    printer("Default")
    assert "[TEST]" in string_output.getvalue()
    
    string_output.seek(0)
    string_output.truncate()
    
    # Сплошной стиль
    printer = Printer(file=string_output, prefix="TEST", style="solid")
    printer("Solid")
    assert " TEST " in string_output.getvalue()
    
    string_output.seek(0)
    string_output.truncate()
    
    # Минималистичный стиль
    printer = Printer(file=string_output, prefix="[TEST]", style="minimal")
    printer("Minimal")
    assert "● TEST ●" in string_output.getvalue()

def test_bprinter_initialization():
    """Тест инициализации BPrinter"""
    bp = BPrinter(show_time=True)
    assert isinstance(bp.success, Printer)
    assert isinstance(bp.error, Printer)
    assert isinstance(bp.warning, Printer)
    assert isinstance(bp.info, Printer)
    assert isinstance(bp.debug, Printer)
    assert isinstance(bp.critical, Printer)
    assert isinstance(bp.system, Printer)
    assert isinstance(bp.done, Printer)

def test_bprinter_custom(string_output):
    """Тест создания пользовательского принтера"""
    bp = BPrinter()
    custom = bp.custom(
        "TEST",
        color="cyan",
        background="white",
        bold=True
    )
    custom("Custom message", file=string_output)
    output = string_output.getvalue()
    assert "[TEST]" in output
    assert Color.CYAN in output
    assert Background.WHITE in output
    assert Style.BOLD in output

def test_printer_with_formatting(string_output):
    """Тест принтера с форматированием текста"""
    printer = Printer(file=string_output, enable_formatting=True)
    printer("This is **bold** and _italic_ text")
    output = string_output.getvalue()
    assert Style.BOLD in output
    assert Style.ITALIC in output
    assert Style.RESET in output

def test_printer_without_formatting(string_output):
    """Тест принтера без форматирования текста"""
    printer = Printer(file=string_output, enable_formatting=False)
    printer("This is **bold** and _italic_ text")
    output = string_output.getvalue()
    assert "**bold**" in output  # Маркеры форматирования должны остаться как есть
    assert "_italic_" in output

def test_printer_multiple_values(string_output):
    """Тест принтера с несколькими значениями"""
    printer = Printer(file=string_output)
    printer("One", "Two", "Three", sep=", ")
    assert "One, Two, Three" in string_output.getvalue()

def test_printer_custom_end(string_output):
    """Тест принтера с пользовательским окончанием строки"""
    printer = Printer(file=string_output)
    printer("No newline", end="")
    printer("Same line")
    assert "No newlineSame line" in string_output.getvalue()

def test_rgb_color_printer(string_output):
    """Тест принтера с RGB цветами"""
    printer = Printer(
        file=string_output,
        color=(255, 128, 0)  # Оранжевый
    )
    printer("RGB colored text")
    output = string_output.getvalue()
    assert "\033[38;2;255;128;0m" in output
    assert "RGB colored text" in output

def test_error_handling(string_output):
    """Тест обработки ошибок"""
    with pytest.raises(StyleError) as exc_info:
        printer = Printer(file=string_output, color=(300, 0, 0))  # Некорректное значение RGB
        printer("This should raise an error")
    assert "Некорректный цвет текста" in str(exc_info.value)
    
    with pytest.raises(StyleError) as exc_info:
        printer = Printer(file=string_output, background=(0, 300, 0))  # Некорректное значение RGB
        printer("This should raise an error")
    assert "Некорректный цвет фона" in str(exc_info.value)

def test_printer_no_color_support(string_output):
    """Тест принтера без поддержки цвета"""
    # Временно отключаем поддержку цвета
    original_supports_color = platform_manager.supports_color
    platform_manager.supports_color = lambda: False
    
    try:
        printer = Printer(
            file=string_output,
            color="red",
            background="white",
            bold=True,
            prefix="[TEST]",
            show_time=True
        )
        printer("Test message")
        output = string_output.getvalue()
        
        # Проверяем, что форматирование не применилось
        assert Color.RED not in output
        assert Background.WHITE not in output
        assert Style.BOLD not in output
        assert "[TEST]" in output
        assert "Test message" in output
    finally:
        # Восстанавливаем оригинальную функцию
        platform_manager.supports_color = original_supports_color

def test_printer_with_different_styles(string_output):
    """Тест принтера с разными стилями оформления"""
    # Тест стиля по умолчанию
    printer = Printer(prefix="TEST", style="default")
    printer("Default style", file=string_output)
    assert "TEST" in string_output.getvalue()
    
    string_output.seek(0)
    string_output.truncate()
    
    # Тест сплошного стиля
    printer = Printer(prefix="TEST", style="solid")
    printer("Solid style", file=string_output)
    assert " TEST " in string_output.getvalue()
    
    string_output.seek(0)
    string_output.truncate()
    
    # Тест минималистичного стиля
    printer = Printer(prefix="TEST", style="minimal")
    printer("Minimal style", file=string_output)
    assert "● TEST ●" in string_output.getvalue()

def test_printer_with_custom_file():
    """Тест принтера с пользовательским файлом вывода"""
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w+') as temp_file:
        printer = Printer()
        printer("Test to file", file=temp_file)
        
        # Перемещаем указатель в начало файла для чтения
        temp_file.seek(0)
        content = temp_file.read()
        assert "Test to file\n" in content 

def test_printer_with_invalid_style(string_output):
    """Тест принтера с некорректным стилем"""
    printer = Printer(prefix="TEST", style="invalid")
    printer("Test message", file=string_output)
    assert "TEST" in string_output.getvalue()

def test_printer_with_empty_prefix(string_output):
    """Тест принтера с пустым префиксом"""
    printer = Printer(prefix="", show_time=True)
    printer("Test message", file=string_output)
    current_hour = datetime.now().strftime("%H")
    assert current_hour in string_output.getvalue()
    assert "Test message" in string_output.getvalue()

def test_printer_with_no_color_support_and_formatting(string_output):
    """Тест принтера без поддержки цвета и с форматированием"""
    with patch('bprinter.platform.platform_manager.supports_color', return_value=False):
        printer = Printer(
            color="red",
            background="white",
            bold=True,
            prefix="[TEST]",
            show_time=True,
            enable_formatting=True
        )
        printer("**Bold** and _italic_", file=string_output)
        output = string_output.getvalue()
        assert "Bold" in output
        assert "italic" in output
        assert Color.RED not in output
        assert Background.WHITE not in output
        assert Style.BOLD not in output 

def test_printer_with_custom_style():
    """Тест принтера с пользовательским стилем"""
    output = StringIO()
    printer = Printer(prefix="TEST", style="custom")
    printer("Test message", file=output)
    assert "TEST" in output.getvalue()

def test_printer_with_no_color_support_and_prefix():
    """Тест принтера без поддержки цвета и с префиксом"""
    output = StringIO()
    with patch('bprinter.platform.platform_manager.supports_color', return_value=False):
        printer = Printer(prefix="[TEST]", show_time=True)
        printer("Test message", file=output)
        result = output.getvalue()
        assert "[TEST]" in result
        assert "Test message" in result
        assert datetime.now().strftime('%H:%M') in result

def test_printer_with_color_support_and_prefix():
    """Тест принтера с поддержкой цвета и с префиксом"""
    output = StringIO()
    with patch('bprinter.platform.platform_manager.supports_color', return_value=True):
        printer = Printer(prefix="[TEST]", show_time=True)
        printer("Test message", file=output)
        result = output.getvalue()
        assert "[TEST]" in result
        assert "Test message" in result
        assert datetime.now().strftime('%H:%M') in result 