/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify, type ThemeDefinition } from 'vuetify'
import { VDateInput } from 'vuetify/labs/VDateInput'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const brandedThemeLight: ThemeDefinition = {
  dark: true,
  colors: {
    background: '#FFFFFF',
    surface: '#f3f4f6',
    primary: '#7c207e',
    secondary: '#f9fafb',
    error: '#ef4444',
    info: '#2196F3',
    success: '#2a9d90',
    warning: '#e76e50',
  },
}

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'brandedThemeLight',
    themes: {
      brandedThemeLight
    }
  },
  components: {
    VDateInput,
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})
