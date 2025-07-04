from playwright.sync_api import Page, expect

def test_estimation_high(page: Page):
    
    # Open page
    page.goto("http://localhost:3000/")
    page.get_by_role("link", name="Connect Data").click()

    # Assert test values
    expect(page.get_by_role("textbox", name="API Endpoint API Endpoint")).to_have_value("http://localhost:8069")
    expect(page.get_by_role("textbox", name="Select date range Select date")).to_have_value("08/02/2024 - 08/02/2024")
    expect(page.get_by_role("slider")).to_contain_text("0.7") # default, no change

    # Import data
    page.get_by_role("button", name="Import Data").click()

    #wait
    page.wait_for_selector("text=Success! Your invoice data has been imported and estimated")

    # Assert success
    expect(page.get_by_role("main")).to_contain_text("Success! Your invoice data has been imported and estimated")

    # Assert results for row 1
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(1)")).to_contain_text("Kenwood KAX 941 PL Getreidemühle AA 25926")
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(2)")).to_contain_text("0.000")
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(3)")).to_contain_text("0.022")

    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(4) > center > .mdi-check-circle")).to_be_visible() # checkmark
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(5) > center > .mdi-check-circle")).to_be_visible() # checkmark
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(6) > center > .mdi-close-circle")).to_be_visible() # failed
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(7) > center > .mdi-close-circle")).to_be_visible() # failed
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(8) > center > .mdi-check-circle")).to_be_visible() # checkmark
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(9) > center > .mdi-check-circle")).to_be_visible() # checkmark
    expect(page.locator("tbody tr:nth-child(1) > td:nth-child(10) > center > .mdi-check-circle")).to_be_visible() # checkmark

    # Assert results for row 2
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(1)")).to_contain_text("Nedis CCGB39800WT15 Sync- & Ladekabel USB-C <-> Lightning, 1.5 Meter")
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(2)")).to_contain_text("0.000")
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(3)")).to_contain_text("0.001")
    
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(4) > center > .mdi-check-circle")).to_be_visible() # checkmark
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(5) > center > .mdi-check-circle")).to_be_visible() # checkmark
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(6) > center > .mdi-close-circle")).to_be_visible() # failed
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(7) > center > .mdi-close-circle")).to_be_visible() # failed
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(8) > center > .mdi-check-circle")).to_be_visible() # checkmark
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(9) > center > .mdi-check-circle")).to_be_visible() # checkmark
    expect(page.locator("tbody tr:nth-child(2) > td:nth-child(10) > center > .mdi-check-circle")).to_be_visible() # checkmark

    # Assert no row 3
    expect(page.locator("tbody tr:nth-child(3)")).not_to_be_visible()