/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'
import VueApexCharts from "vue3-apexcharts"

// Composables
import { createApp } from 'vue'

// Styles
import 'unfonts.css'

const app = createApp(App)
app.use(VueApexCharts)
registerPlugins(app)

app.component("ApexChart", VueApexCharts)

app.mount('#app')
