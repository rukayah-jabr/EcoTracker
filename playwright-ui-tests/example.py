import pytest
from playwright.sync_api import Page, expect

def test_header_shows_title(page: Page):
    page.goto("http://localhost:3000")
    expect(page.locator(".v-toolbar-title__placeholder")).to_have_text("EcoTracker")
