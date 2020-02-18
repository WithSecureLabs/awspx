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
import graph from "@/components/graph";

export default {
  components: { graph },
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
