<template>
  <v-container max-width="900">
    <!-- Temporary text filler -->
    <div>
      <div class="my-8 text-center">
        <div class="text-body-2 font-weight-light mb-2">Welcome to</div>
        <h1 class="text-h2 font-weight-bold">EcoTracker</h1>
      </div>

      <v-row>
        <v-col v-for="card in cards" :key="card.title" cols="4">
          <v-card
            class="py-4"
            color="success"
            :prepend-icon="card.icon"
            rounded="lg"
            :title="card.title"
            variant="tonal"
          />
        </v-col>
      </v-row>

      <div class="my-8">
        <p class="text-h5 mb-4">The EcoTracker is a prototype for an application which helps companies measure and analyze their carbon footprint.</p>
        <p class="mb-4">The goal is to offer companies a comprehensive and transparent accounting of their CO2 emissions based on their own invoice data.</p>
        <p class="mb-4">EcoTracker automates the calculation of emission estimates and provides instant data insights. The results can enable companies to more quickly assess
          their carbon footprint and make informed decisions about their emissions.</p>
        <p class="text-h6 text-center mt-6 border-t pt-6">EcoTracker Features</p>
        <div class="d-sm-flex my-6 ga-6">
          <p>Automates the collection and cleaning of invoice data to use as a basis for calculating CO2 emissions</p>
          <p>Integrates with Climatiq to derive emission values for products included in the invoice data</p>
          <p>Provides realistic approximations when precise information is missing</p>
          <p>Outputs the results in a dashboard for valuable data insights with data visualizations</p>
        </div>
        <p>The primary advantage of this application for companies is saving a considerable amount of time and resources in analyzing their own carbon footprint. Minimizing the
          burden of carrying out this type of analysis will help companies more quickly and efficiently optimize the environmental impact of their own business processes.</p>
      </div>
    </div>
  </v-container>
</template>

<script setup lang="ts">
  const cards = [
    {
      icon: 'mdi-connection',
      title: 'Connect Your Data',
    },
    {
      icon: 'mdi-calculator',
      title: 'Calculate Emissions',
    },
    {
      icon: 'mdi-chart-bar',
      title: 'Analyze Results',
    }
  ]
</script>
