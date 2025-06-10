<template>
  <v-layout>
    <v-app-bar title="EcoTracker"></v-app-bar>

    <v-navigation-drawer>
      <v-list nav>
        <v-list-item title="Connect Data" link to="/connect"></v-list-item>
        <v-list-item title="Data Dashboard" link to="/dashboard"></v-list-item>
        <v-list-item title="Product Details" link to="/productdetails"></v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main class="mx-10 my-7">
      <router-view />
    </v-main>
  </v-layout>

  <!-- <AppFooter /> -->
</template>

<script lang="ts" setup>
  //
</script>
