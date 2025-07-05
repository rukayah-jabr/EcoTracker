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

    # Try to wait for navigation to /connect explicitly
    try:
        with page.expect_navigation(url="**/connect", timeout=5000):
            connect_btn.click(force=True)
    except Exception:
        # If navigation doesn't happen, click without waiting and try to wait for URL manually
        connect_btn.click(force=True)
        page.wait_for_url("**/connect", timeout=5000)

    print("Current URL after click:", page.url)
    page.screenshot(path="after_click_connect_data.png", full_page=True)

    # Now check for the textbox input with expected value
    txtbox = page.get_by_role("textbox", name="API Endpoint API Endpoint")
    expect(txtbox).to_have_value("http://localhost:8069", timeout=5000)

    daterange = page.get_by_role("textbox", name="Select date range Select date")
    expect(daterange).to_have_value("08/02/2024 - 08/02/2024")

    # Move confidence slider to 0
    slider = page.locator(".v-slider")  # Adjust selector if needed
    slider.wait_for(state="visible")

    box = slider.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)  # center of slider
    page.mouse.down()
    page.mouse.move(box["x"], box["y"] + box["height"] / 2, steps=10)  # drag to left edge
    page.mouse.up()

    expect(page.get_by_role("slider")).to_contain_text("0.0")

    # Import data
    page.get_by_role("button", name="Import Data").click()

    # Wait for success message
    page.wait_for_selector("text=Success! Your invoice data has been imported and estimated")

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

