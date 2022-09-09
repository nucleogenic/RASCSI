import pytest
from playwright.sync_api import Playwright, BrowserContext, Page, sync_playwright, expect

from models.index import Index
from models.index_settings import IndexSettings

def test_set_log_level(page: Page) -> None:
    index = Index(page)
    settings = IndexSettings(page)

    # Set log level
    settings.set_log_level("critical")
    expect(page.locator("text=Log level set to critical")).to_be_visible()
    expect(page.locator("table#set-log-level select option:checked")).to_have_text("critical")

    # Cleanup
    settings.set_log_level("debug")


def test_set_language(page: Page) -> None:
    index = Index(page)
    settings = IndexSettings(page)

    # Update language
    settings.set_language("es")
    expect(page.locator("text=Se ha cambiado el lenguaje de la Interfaz Web a español")).to_be_visible()
    # TODO: Should current language setting be selected?
    # expect(page.locator("table#set-language select option:checked")).to_have_text("es - español")

    settings.set_language("en")
    expect(page.locator("text=Changed Web Interface language to English")).to_be_visible()
    # TODO: Should current language setting be selected?
    # expect(page.locator("table#set-language select option:checked")).to_have_text("en - English")
