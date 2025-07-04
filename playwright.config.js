// playwright.config.js
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './playwright-ui-tests',
  timeout: 30 * 1000,
  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    launchOptions: {
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    },
    viewport: { width: 1280, height: 720 },
  },
  webServer: {
    command: 'npm run dev --prefix frontend',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 120 * 1000,
  },
});
