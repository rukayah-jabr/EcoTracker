from playwright.sync_api import Page, expect
from time import time, sleep


def wait_until_enabled(locator, timeout=5):
    end = time() + timeout
    while time() < end:
        enabled = locator.evaluate('el => !el.hasAttribute("disabled") && !el.getAttribute("aria-disabled")')
        if enabled:
            return True
        sleep(0.1)
    raise TimeoutError("Locator was not enabled within timeout")


def test_001_estimation_low(page: Page):
    # Open page
    page.goto("http://localhost:3000/")
    page.wait_for_load_state("networkidle")

    connect_btn = page.get_by_role("link", name="Connect Data")
    # Wait until it is not disabled
    wait_until_enabled(connect_btn, timeout=5)

    page.screenshot(path="before_click_connect_data.png", full_page=True)

    connect_btn.click()

    page.wait_for_load_state("networkidle")

    # Take a screenshot of the 'Connect Data' page
    page.screenshot(path="connect_page.png", full_page=True)

    # Assert test values
    expect(page.get_by_role("textbox", name="API Endpoint API Endpoint")).to_have_value("http://localhost:8069")
    expect(page.get_by_role("textbox", name="Select date range Select date")).to_have_value("08/02/2024 - 08/02/2024")

    # Move confidence slider to 0
    slider = page.locator(".v-slider")  # Adjust selector
    slider.wait_for(state="visible")

    # Get the bounding box of the slider (for pixel positioning)
    box = slider.bounding_box()

    # Drag the thumb to the left edge (value 0)
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)  # move to center first
    page.mouse.down()
    page.mouse.move(box["x"], box["y"] + box["height"] / 2, steps=10)  # drag to far left
    page.mouse.up()

    # Assert confidence level
    expect(page.get_by_role("slider")).to_contain_text("0.0")  # default, no change

    # Import data
    page.get_by_role("button", name="Import Data").click()

    # Wait for success message
    page.wait_for_selector("text=Success! Your invoice data has been imported and estimated")

    # Assert success message
    expect(page.get_by_role("main")).to_contain_text("Success! Your invoice data has been imported and estimated")

    # Assert results for row 1
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(1)")).to_contain_text(
        "Kenwood KAX 941 PL Getreidemühle AA 25926")
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(2)")).to_contain_text("132.987")
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(3)")).to_contain_text("0.022")

    for i in range(4, 11):
        expect(page.locator(f"tbody tr:nth-child(1) > td:nth-child({i}) > center > .mdi-check-circle")).to_be_visible()

    # Assert results for row 2
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(1)")).to_contain_text(
        "Nedis CCGB39800WT15 Sync- & Ladekabel USB-C <-> Lightning, 1.5 Meter")
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(2)")).to_contain_text("1.340")
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(3)")).to_contain_text("0.001")

    for i in range(4, 11):
        expect(page.locator(f"tbody tr:nth-child(2) > td:nth-child({i}) > center > .mdi-check-circle")).to_be_visible()

    # Assert no row 3
    expect(page.locator("tbody tr:nth-child(3)")).not_to_be_visible()
