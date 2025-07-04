const { test, expect } = require('@playwright/test');

test('Header zeigt richtigen Titel', async ({ page }) => {
  await page.goto('http://localhost:3000');

  const titleLocator = page.locator('header .v-toolbar-title__placeholder');
  await expect(titleLocator).toHaveText('EcoTracker');
});
