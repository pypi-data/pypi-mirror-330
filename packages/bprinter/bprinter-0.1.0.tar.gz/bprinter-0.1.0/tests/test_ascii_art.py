import pytest
from bprinter.ascii_art import ASCIIArtGenerator
from bprinter.styles import Color, Background, Style

def test_get_available_fonts():
    """Тест получения списка доступных шрифтов"""
    fonts = ASCIIArtGenerator.get_available_fonts()
    assert isinstance(fonts, list)
    assert len(fonts) > 0
    assert "standard" in fonts

def test_render_basic():
    """Тест базового рендеринга ASCII арта"""
    text = "Test"
    art = ASCIIArtGenerator.render(text)
    assert isinstance(art, str)
    assert len(art) > 0
    assert art.count("\n") > 0

def test_render_with_color():
    """Тест рендеринга с цветом"""
    text = "Test"
    art = ASCIIArtGenerator.render(text, color="red")
    assert Color.RED in art
    assert Style.RESET in art

def test_render_with_background():
    """Тест рендеринга с фоном"""
    text = "Test"
    art = ASCIIArtGenerator.render(text, background="blue")
    assert Background.BLUE in art
    assert Style.RESET in art

def test_render_with_custom_font():
    """Тест рендеринга с пользовательским шрифтом"""
    text = "Test"
    art = ASCIIArtGenerator.render(text, font="banner")
    assert isinstance(art, str)
    assert len(art) > 0

def test_render_with_invalid_font():
    """Тест обработки некорректного шрифта"""
    with pytest.raises(ValueError):
        ASCIIArtGenerator.render("Test", font="invalid_font")

def test_preview_fonts():
    """Тест предпросмотра шрифтов"""
    text = "Test"
    preview = ASCIIArtGenerator.preview_fonts(text, fonts=["standard", "banner"])
    assert "Font: standard" in preview
    assert "Font: banner" in preview

def test_preview_fonts_default():
    """Тест предпросмотра со шрифтами по умолчанию"""
    text = "Test"
    preview = ASCIIArtGenerator.preview_fonts(text)
    assert "Font: standard" in preview
    assert preview.count("Font:") >= 5  # Проверяем, что показано несколько шрифтов

def test_render_with_width():
    """Тест рендеринга с указанной шириной"""
    text = "Test" * 10
    art = ASCIIArtGenerator.render(text, width=40)
    lines = art.split("\n")
    assert all(len(line) <= 40 for line in lines if line.strip()) 