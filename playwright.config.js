const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './playwright-ui-tests',
  timeout: 30 * 1000,
  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    viewport: { width: 1280, height: 720 },
    launchOptions: {
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    },

    // Automatically take screenshot on failure
    screenshot: 'only-on-failure',

  },

  webServer: {
    command: 'npm run dev --prefix frontend',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 120 * 1000,
  },
});
