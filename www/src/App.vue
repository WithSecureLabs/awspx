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

@font-face {
  font-family: "Material Icons";
  font-style: normal;
  font-weight: 400;
  src: local("Material Icons"), local("MaterialIcons-Regular"),
    url("assets/fonts/MaterialIcons-Regular.woff2") format("woff2"),
    url("assets/fonts/MaterialIcons-Regular.woff") format("woff");
}

.material-icons {
  font-family: "Material Icons";
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
}
#app {
  font-family: "Source Code Pro";
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
