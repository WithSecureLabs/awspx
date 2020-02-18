<template>
  <div id="app">
    <v-app>
      <v-content>
        <graph></graph>
      </v-content>
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
  font-family: "Source Code Pro";
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
