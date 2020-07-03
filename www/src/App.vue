<template>
  <div id="app">
    <v-app>
      <v-main>
        <graph></graph>
      </v-main>
    </v-app>
  </div>
</template>

<script>
import Graph from "@/components/Graph";

export default {
  components: { Graph },
  name: "App"
};
</script>

<style>
#app {
  font-family: "Roboto Mono", monospace !important;
  font-size: 12px !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

</style>
