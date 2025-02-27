class BPrinterError(Exception):
    """Базовый класс для всех исключений библиотеки"""
    pass

class ColorError(BPrinterError):
    """Исключение при некорректных цветовых значениях"""
    pass

class PlatformError(BPrinterError):
    """Исключение при проблемах с платформой"""
    pass

class StyleError(BPrinterError):
    """Исключение при некорректном использовании стилей"""
    pass 