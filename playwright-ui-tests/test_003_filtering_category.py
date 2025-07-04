from playwright.sync_api import Page, expect

def test_filtering_category(page: Page):
    
    # Open page
    page.goto("http://localhost:3000/")
    page.get_by_role("link", name="Connect Data").click()

    # Assert test values
    expect(page.get_by_role("textbox", name="API Endpoint API Endpoint")).to_have_value("http://localhost:8069")
    expect(page.get_by_role("textbox", name="Select date range Select date")).to_have_value("08/02/2024 - 08/02/2024")

    # Move confidence slider to 0
    slider = page.locator(".v-slider")  # Adjust selector

    # Get the bounding box of the slider (for pixel positioning)
    box = slider.bounding_box()

    # Drag the thumb to the left edge (value 0)
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)  # move to center first
    page.mouse.down()
    page.mouse.move(box["x"], box["y"] + box["height"] / 2, steps=10)  # drag to far left
    page.mouse.up()

    # Assert confidence level
    expect(page.get_by_role("slider")).to_contain_text("0.0") # default, no change

    # Import data
    page.get_by_role("button", name="Import Data").click()

    # Go to dashbaord
    page.get_by_role("link", name="Data Dashboard").click()

    # Assert initial state (no selections)
    expect(page.get_by_role("combobox").locator("div").filter(has_text="Filter categoryFilter category"))

    # Assert list of categories
    page.get_by_role("combobox").locator("div").filter(has_text="Filter categoryFilter category").locator("div").click()
    expect(page.get_by_label("Filter category-list")).to_contain_text("Elektronik")
    expect(page.get_by_label("Filter category-list")).to_contain_text("Kuechengeraete")

    # Filter on first category
    page.get_by_label("Filter category-list").get_by_text("Elektronik").click()
    expect(page.locator('path.apexcharts-pie-slice-5').nth(0)).to_have_attribute("data:angle", "360") # 100% of first pie chart
    expect(page.locator('path.apexcharts-pie-slice-5').nth(1)).to_have_attribute("data:angle", "360") # 100% of second pie chart

    # Filter on second category
    page.get_by_label("Filter category-list").get_by_text("Elektronik").click()
    page.get_by_label("Filter category-list").get_by_text("Kuechengeraete").click()
    expect(page.locator('path.apexcharts-pie-slice-9').nth(0)).to_have_attribute("data:angle", "360") # 100% of first pie chart
    expect(page.locator('path.apexcharts-pie-slice-9').nth(1)).to_have_attribute("data:angle", "360") # 100% of second pie chart