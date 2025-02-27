import pytest
from bprinter.exceptions import BPrinterError, ColorError, PlatformError, StyleError

def test_bprinter_error():
    """Тест базового исключения"""
    with pytest.raises(BPrinterError):
        raise BPrinterError("Test error")

def test_color_error():
    """Тест исключения цвета"""
    with pytest.raises(ColorError):
        raise ColorError("Invalid color")
    
    # Проверка наследования
    with pytest.raises(BPrinterError):
        raise ColorError("Color error is a BPrinterError")

def test_platform_error():
    """Тест исключения платформы"""
    with pytest.raises(PlatformError):
        raise PlatformError("Platform not supported")
    
    # Проверка наследования
    with pytest.raises(BPrinterError):
        raise PlatformError("Platform error is a BPrinterError")

def test_style_error():
    """Тест исключения стиля"""
    with pytest.raises(StyleError):
        raise StyleError("Invalid style")
    
    # Проверка наследования
    with pytest.raises(BPrinterError):
        raise StyleError("Style error is a BPrinterError")

def test_error_messages():
    """Тест сообщений об ошибках"""
    error_msg = "Test error message"
    
    try:
        raise BPrinterError(error_msg)
    except BPrinterError as e:
        assert str(e) == error_msg
    
    try:
        raise ColorError(error_msg)
    except ColorError as e:
        assert str(e) == error_msg
    
    try:
        raise PlatformError(error_msg)
    except PlatformError as e:
        assert str(e) == error_msg
    
    try:
        raise StyleError(error_msg)
    except StyleError as e:
        assert str(e) == error_msg 