import pytest
import os
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
from bprinter.platform import PlatformManager
from bprinter import init

@pytest.fixture
def platform_manager():
    """Фикстура для создания нового менеджера платформы"""
    return PlatformManager()

def test_is_windows():
    """Тест определения Windows"""
    with patch('platform.system', return_value='Windows'):
        pm = PlatformManager()
        assert pm.is_windows is True
    
    with patch('platform.system', return_value='Linux'):
        pm = PlatformManager()
        assert pm.is_windows is False

def test_supports_color_no_isatty():
    """Тест поддержки цвета без isatty"""
    with patch('sys.stdout') as mock_stdout:
        del mock_stdout.isatty
        pm = PlatformManager()
        assert pm.supports_color() is False

def test_supports_color_not_terminal():
    """Тест поддержки цвета не в терминале"""
    with patch('sys.stdout') as mock_stdout:
        mock_stdout.isatty.return_value = False
        
        # Без COLORTERM
        with patch.dict(os.environ, {}, clear=True):
            pm = PlatformManager()
            assert pm.supports_color() is False
        
        # С COLORTERM
        with patch.dict(os.environ, {'COLORTERM': 'truecolor'}):
            pm = PlatformManager()
            assert pm.supports_color() is True

def test_supports_color_windows():
    """Тест поддержки цвета в Windows"""
    with patch('platform.system', return_value='Windows'):
        with patch('sys.stdout') as mock_stdout:
            mock_stdout.isatty.return_value = True
            pm = PlatformManager()
            assert pm.supports_color() is True

def test_supports_color_unix_terms():
    """Тест поддержки цвета для разных терминалов Unix"""
    terms = ['xterm', 'xterm-color', 'xterm-256color', 'linux',
            'screen', 'screen-256color', 'ansi']
    
    with patch('sys.stdout') as mock_stdout:
        mock_stdout.isatty.return_value = True
        for term in terms:
            with patch.dict(os.environ, {'TERM': term}):
                pm = PlatformManager()
                assert pm.supports_color() is True

def test_temp_disable():
    """Тест временного отключения вывода"""
    pm = PlatformManager()
    original_stdout = sys.stdout
    
    with pm.temp_disable():
        assert sys.stdout != original_stdout
        assert isinstance(sys.stdout, StringIO)
    
    assert sys.stdout == original_stdout

@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_windows_init():
    """Тест инициализации на Windows"""
    with patch('platform.system', return_value='Windows'):
        with patch('ctypes.windll.kernel32') as mock_kernel32:
            handle = MagicMock()
            mock_kernel32.GetStdHandle.return_value = handle
            
            mode = MagicMock()
            mock_kernel32.GetConsoleMode.return_value = 0
            mock_kernel32.SetConsoleMode.return_value = 1
            
            pm = PlatformManager()
            pm.init()
            
            # Проверяем, что были вызваны нужные функции
            mock_kernel32.GetStdHandle.assert_called_once()
            mock_kernel32.GetConsoleMode.assert_called_once()
            mock_kernel32.SetConsoleMode.assert_called_once()

def test_multiple_init():
    """Тест множественной инициализации"""
    pm = PlatformManager()
    pm.init()  # Первая инициализация
    assert pm.is_initialized is True
    
    # Повторная инициализация не должна менять состояние
    pm.init()
    assert pm.is_initialized is True

def test_init_non_windows():
    """Тест инициализации на не-Windows системах"""
    with patch('platform.system', return_value='Linux'):
        pm = PlatformManager()
        pm.init()
        assert pm.is_initialized is True
        # Повторная инициализация не должна менять состояние
        pm.init()
        assert pm.is_initialized is True

def test_supports_color_with_term_no_isatty():
    """Тест поддержки цвета с TERM но без isatty"""
    with patch('sys.stdout') as mock_stdout:
        mock_stdout.isatty.return_value = False
        with patch.dict(os.environ, {'TERM': 'xterm-256color', 'COLORTERM': ''}):
            pm = PlatformManager()
            assert pm.supports_color() is False

def test_supports_color_with_colorterm_no_isatty():
    """Тест поддержки цвета с COLORTERM но без isatty"""
    with patch('sys.stdout') as mock_stdout:
        mock_stdout.isatty.return_value = False
        with patch.dict(os.environ, {'COLORTERM': 'truecolor'}):
            pm = PlatformManager()
            assert pm.supports_color() is True

def test_temp_disable_nested():
    """Тест вложенного использования temp_disable"""
    pm = PlatformManager()
    original_stdout = sys.stdout
    
    with pm.temp_disable():
        first_temp_stdout = sys.stdout
        assert isinstance(first_temp_stdout, StringIO)
        with pm.temp_disable():
            second_temp_stdout = sys.stdout
            assert isinstance(second_temp_stdout, StringIO)
            assert second_temp_stdout != first_temp_stdout
        assert sys.stdout == first_temp_stdout
    assert sys.stdout == original_stdout

@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_windows_init_with_mock():
    """Тест инициализации на Windows с моками"""
    with patch('platform.system', return_value='Windows'):
        pm = PlatformManager()
        pm.init()
        assert pm.is_initialized is True

def test_supports_color_with_term_and_isatty():
    """Тест поддержки цвета с TERM и isatty"""
    with patch('sys.stdout') as mock_stdout:
        mock_stdout.isatty.return_value = True
        with patch.dict(os.environ, {'TERM': 'xterm-256color'}):
            pm = PlatformManager()
            assert pm.supports_color() is True

def test_supports_color_with_invalid_term():
    """Тест поддержки цвета с некорректным TERM"""
    with patch('sys.stdout') as mock_stdout:
        mock_stdout.isatty.return_value = True
        with patch.dict(os.environ, {'TERM': 'invalid-term', 'COLORTERM': ''}):
            pm = PlatformManager()
            assert pm.supports_color() is False

def test_supports_color_with_no_env():
    """Тест поддержки цвета без переменных окружения"""
    with patch('sys.stdout') as mock_stdout:
        mock_stdout.isatty.return_value = True
        with patch.dict(os.environ, {}, clear=True):
            pm = PlatformManager()
            assert pm.supports_color() is False

def test_init_with_strip():
    """Тест инициализации с отключением цветов"""
    pm = PlatformManager()
    pm.init(strip=True)
    assert pm.strip_colors is True
    assert pm.supports_color() is False

def test_init_with_convert():
    """Тест инициализации с конвертацией новых строк"""
    pm = PlatformManager()
    pm.init(convert=False)
    assert pm.convert_newlines is False

def test_init_multiple_calls():
    """Тест множественных вызовов init"""
    pm = PlatformManager()
    pm.init(strip=True, convert=True)
    assert pm.strip_colors is True
    assert pm.convert_newlines is True
    
    # Второй вызов с другими параметрами
    pm.init(strip=False, convert=False)
    assert pm.strip_colors is False
    assert pm.convert_newlines is False

def test_init_partial_params():
    """Тест инициализации с частичными параметрами"""
    pm = PlatformManager()
    pm.init(strip=True)
    assert pm.strip_colors is True
    assert pm.convert_newlines is True  # Значение по умолчанию
    
    pm.init(convert=False)
    assert pm.strip_colors is True  # Не изменилось
    assert pm.convert_newlines is False

def test_global_init():
    """Тест глобальной функции init"""
    init(strip=True, convert=False, wrap=True)
    from bprinter.platform import platform_manager
    assert platform_manager.strip_colors is True
    assert platform_manager.convert_newlines is False 