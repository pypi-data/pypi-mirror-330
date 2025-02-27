import pytest
from bprinter.styles import Style, Color, Background
from unittest.mock import patch

def test_style_constants():
    """Тест констант стилей"""
    assert Style.RESET == '\033[0m'
    assert Style.BOLD == '\033[1m'
    assert Style.ITALIC == '\033[3m'
    assert Style.UNDERLINE == '\033[4m'
    assert Style.STRIKE == '\033[9m'

def test_basic_colors():
    """Тест базовых цветов"""
    assert Color.RED.startswith('\033[31m')
    assert Color.GREEN.startswith('\033[32m')
    assert Color.BLUE.startswith('\033[34m')
    assert Color.WHITE.startswith('\033[37m')

def test_bright_colors():
    """Тест ярких цветов"""
    assert Color.BRIGHT_RED.startswith('\033[91m')
    assert Color.BRIGHT_GREEN.startswith('\033[92m')
    assert Color.BRIGHT_BLUE.startswith('\033[94m')
    assert Color.BRIGHT_WHITE.startswith('\033[97m')

def test_background_colors():
    """Тест цветов фона"""
    assert Background.RED.startswith('\033[41m')
    assert Background.GREEN.startswith('\033[42m')
    assert Background.BLUE.startswith('\033[44m')
    assert Background.WHITE.startswith('\033[47m')

def test_bright_background_colors():
    """Тест ярких цветов фона"""
    assert Background.BRIGHT_RED.startswith('\033[101m')
    assert Background.BRIGHT_GREEN.startswith('\033[102m')
    assert Background.BRIGHT_BLUE.startswith('\033[104m')
    assert Background.BRIGHT_WHITE.startswith('\033[107m')

def test_style_context_manager():
    """Тест контекстного менеджера стилей"""
    import sys
    from io import StringIO
    output = StringIO()
    sys.stdout = output
    
    with Style.styled(Style.BOLD, Style.ITALIC):
        print("Test", end='')
    sys.stdout = sys.__stdout__
    
    result = output.getvalue()
    assert Style.BOLD in result
    assert Style.ITALIC in result
    assert Style.RESET in result
    assert "Test" in result

def test_style_context_manager_no_color_support():
    """Тест контекстного менеджера стилей без поддержки цвета"""
    import sys
    from io import StringIO
    output = StringIO()
    sys.stdout = output
    
    with patch('bprinter.platform.platform_manager.supports_color', return_value=False):
        with Style.styled(Style.BOLD, Style.ITALIC):
            print("Test", end='')
    sys.stdout = sys.__stdout__
    
    result = output.getvalue()
    assert Style.BOLD not in result
    assert Style.ITALIC not in result
    assert "Test" in result

def test_color_context_manager():
    """Тест контекстного менеджера цветов"""
    import sys
    from io import StringIO
    output = StringIO()
    sys.stdout = output
    
    with Style.color("red"):
        print("Test", end='')
    sys.stdout = sys.__stdout__
    
    result = output.getvalue()
    assert Color.RED in result
    assert Style.RESET in result
    assert "Test" in result
    
    # Тест с RGB цветом
    output = StringIO()
    sys.stdout = output
    
    with Style.color((255, 128, 0)):
        print("Test", end='')
    sys.stdout = sys.__stdout__
    
    result = output.getvalue()
    assert "\033[38;2;255;128;0m" in result
    assert Style.RESET in result
    assert "Test" in result

def test_color_context_manager_no_color_support():
    """Тест контекстного менеджера цветов без поддержки цвета"""
    import sys
    from io import StringIO
    output = StringIO()
    sys.stdout = output
    
    with patch('bprinter.platform.platform_manager.supports_color', return_value=False):
        with Style.color("red"):
            print("Test", end='')
    sys.stdout = sys.__stdout__
    
    result = output.getvalue()
    assert Color.RED not in result
    assert "Test" in result

def test_invalid_color_name():
    """Тест обработки некорректного имени цвета"""
    with pytest.raises(ValueError) as exc_info:
        with Style.color("invalid_color"):
            print("Test")
    assert "Unknown color: invalid_color" in str(exc_info.value)

def test_rgb_color_methods():
    """Тест методов создания RGB цветов"""
    # Тест для текста
    color = Color.rgb(255, 128, 0)
    assert color == "\033[38;2;255;128;0m"
    
    # Тест для фона
    color = Background.rgb(255, 128, 0)
    assert color == "\033[48;2;255;128;0m"
    
    # Тест некорректных значений
    with pytest.raises(ValueError):
        Color.rgb(300, 0, 0)
    
    with pytest.raises(ValueError):
        Background.rgb(0, -1, 0)

def test_256_color_methods():
    """Тест методов создания 256-цветных кодов"""
    # Тест для текста
    color = Color.code(128)
    assert color == "\033[38;5;128m"
    
    # Тест для фона
    color = Background.code(128)
    assert color == "\033[48;5;128m"
    
    # Тест некорректных значений
    with pytest.raises(ValueError):
        Color.code(300)
    
    with pytest.raises(ValueError):
        Background.code(-1) 