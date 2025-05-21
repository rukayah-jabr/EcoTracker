<template>
  <v-layout>
    <v-app-bar title="EcoTracker"></v-app-bar>

    <v-navigation-drawer>
      <v-list nav>
        <v-list-item title="Connect Data" link></v-list-item>
        <v-list-item title="Data Dashboard" link></v-list-item>
        <v-list-item title="Product Details" link></v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-layout>

  <!-- <AppFooter /> -->
</template>

<script lang="ts" setup>
  //
</script>
