<template>
  <v-layout>
    <v-app-bar :elevation="2">
      <template v-slot:prepend>
        <v-app-bar-nav-icon color="success" icon="mdi-sprout-outline" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      </template>

      <v-app-bar-title>EcoTracker</v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer">
      <v-list nav>
        <v-list-subheader>MENU</v-list-subheader>
        <v-list-item link to="/connect" color="primary">
          <template v-slot:prepend>
              <v-icon icon="mdi-connection"></v-icon>
            </template>
            <v-list-item-title>Connect Data</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/dashboard" color="primary">
          <template v-slot:prepend>
              <v-icon icon="mdi-chart-bar"></v-icon>
            </template>
            <v-list-item-title>Data Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/productdetails" color="primary">
          <template v-slot:prepend>
              <v-icon icon="mdi-invoice-list-outline"></v-icon>
            </template>
            <v-list-item-title>Product Details</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main class="mx-10 my-7">
      <div class="border border-primary pa-7 rounded-lg">
        <router-view />
      </div>
    </v-main>
  </v-layout>

  <!-- <AppFooter /> -->
</template>

<script lang="ts" setup>

const drawer = ref(true)

</script>
