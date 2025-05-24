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
            color="surface-variant"
            :prepend-icon="card.icon"
            rounded="lg"
            :title="card.title"
            variant="tonal"
          />
        </v-col>
      </v-row>
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
